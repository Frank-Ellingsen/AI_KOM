# Evaluator-Optimizer Loop Specification: Ollama (Local LLMs)

This document provides a production specification and implementation blueprint for building an **Evaluator-Optimizer (Generator-Critic)** loop powered by **Ollama** running open-weight local models (such as Llama 3.3, Qwen 2.5, or Mistral).

---

## 1. Architectural Overview

Running Evaluator-Optimizer loops on local hardware requires managing context windows, model loading overhead, and schema enforcement. The architecture pairs a fast local **Generator model** with a high-parameter **Evaluator model** (or uses a single model with dual temperature/system prompt configurations to prevent VRAM swapping).

```
                      ┌─────────────────────────────────┐
                      │        User Task Prompt         │
                      └────────────────┬────────────────┘
                                       │
                                       ▼
                      ┌─────────────────────────────────┐
                      │    Generator: Qwen2.5-14B       │◄──────────┐
                      │    (Temp=0.7, Creative/Fast)    │           │
                      └────────────────┬────────────────┘           │
                                       │                            │
                                       ▼                            │ Refinement:
                      ┌─────────────────────────────────┐           │ Previous Draft +
                      │    Evaluator: Qwen2.5-14B/32B   │           │ Missing Elements +
                      │    (Temp=0.0, GBNF Grammar)     │           │ Actionable Critique
                      └────────────────┬────────────────┘           │
                                       │                            │
                            Passes Quality Gates?                   │
                            (Score >= Pass Threshold)               │
                            ┌──────────┴──────────┐                 │
                      Yes   │                     │   No            │
                            ▼                     └─────────────────┘
                   [Accepted Output]
```

---

## 2. Ollama-Specific Engineering Considerations

1. **Native Pydantic Schema via GBNF (`format=CritiqueSchema.model_json_schema()`)**:
   - Modern Ollama (v0.5+) supports passing a raw JSON schema dictionary directly to `format`.
   - Under the hood, this converts the JSON Schema into a GBNF (Grammar-Based Context-Free) grammar, enforcing schema conformance at token-generation time rather than relying on loose post-hoc regex or string parsing.
2. **Preserving Loop State (Previous Draft + Critique)**:
   - In multi-turn optimization loops, the Generator **must receive both its previous draft and the Evaluator's critique**. Without the previous draft, the Generator cannot perform targeted corrections or preserve already-valid code/text.
3. **Context Window Configuration (`num_ctx`)**:
   - Open-source models often default to a 2048 or 4096 context window in Ollama. Set `num_ctx: 8192` or `16384` in model options to avoid truncating draft history and critique context during iterative feedback cycles.
4. **Deterministic Evaluation Parameters**:
   - For the Evaluator, set `temperature: 0.0` and `top_p: 0.1` to enforce repeatable, strict rubric scoring across runs.
5. **Local VRAM & Model Swap Optimization**:
   - On a single GPU with limited VRAM (e.g. 12–16GB), running two different large models (e.g., `14b` and `32b`) causes Ollama to reload model weights off the SSD on every turn, adding 15–30 seconds of latency per iteration.
   - **Recommended Pattern**: Use the same model instance (e.g., `qwen2.5:14b` or `qwen2.5:32b`) for both generator and evaluator roles, differentiating behavior strictly via system instructions and temperature settings.

---

## 3. Prompts & JSON Schema Specification

### System Prompt for Local Evaluator
```text
You are an expert system auditor, code reviewer, and quality evaluator.
Your job is to objectively evaluate a candidate solution against the task requirement.

Evaluate strictly against:
1. Accuracy and correctness
2. Completeness and edge-case coverage
3. Clarity and adherence to instructions

You must return valid JSON matching the requested schema.
Be demanding: do not award passing scores (>= 0.85) to flawed, partial, or unverified outputs.
```

### JSON Schema (Pydantic Model)
```json
{
  "score": "<float between 0.0 and 1.0>",
  "passed": "<boolean, true only if score >= pass_threshold>",
  "missing_elements": ["<string describing missing requirement>", "..."],
  "actionable_critique": "<string detailing specific, concrete fixes required>"
}
```

---

## 4. Production Python Implementation (`ollama` SDK)

```python
import json
import logging
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field, ValidationError
import ollama

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


# 1. Pydantic Model for Constrained Output
class CritiqueSchema(BaseModel):
    score: float = Field(ge=0.0, le=1.0, description="Score from 0.0 (unusable) to 1.0 (perfect)")
    passed: bool = Field(description="True if score >= pass_threshold")
    missing_elements: List[str] = Field(
        default_factory=list,
        description="List of specific components, edge cases, or requirements missing from draft"
    )
    actionable_critique: str = Field(
        description="Direct instructions for the generator on how to fix deficiencies"
    )


class OllamaEvaluatorOptimizer:
    def __init__(
        self,
        generator_model: str = "qwen2.5:14b",
        evaluator_model: str = "qwen2.5:14b",  # Defaulting to same model avoids VRAM weight swap latency
        pass_threshold: float = 0.85,
        max_iterations: int = 4,
        num_ctx: int = 8192,
        host: Optional[str] = None,
    ):
        self.client = ollama.Client(host=host)
        self.generator_model = generator_model
        self.evaluator_model = evaluator_model
        self.pass_threshold = pass_threshold
        self.max_iterations = max_iterations
        self.num_ctx = num_ctx

    def run(self, task_prompt: str) -> Dict[str, Any]:
        candidate_output = ""
        latest_critique: Optional[CritiqueSchema] = None
        iteration_history = []

        for iteration in range(1, self.max_iterations + 1):
            logging.info(f"--- Iteration {iteration}/{self.max_iterations} ---")

            # Step A: Generation / Revision
            if iteration == 1:
                gen_prompt = (
                    f"Task Requirement:\n{task_prompt}\n\n"
                    "Provide a complete, production-ready, and accurate solution."
                )
            else:
                missing_str = "\n".join(f"- {item}" for item in latest_critique.missing_elements)
                gen_prompt = (
                    f"Task Requirement:\n{task_prompt}\n\n"
                    f"Previous Candidate Solution (Attempt {iteration - 1}):\n"
                    f"--- BEGIN PREVIOUS DRAFT ---\n{candidate_output}\n--- END PREVIOUS DRAFT ---\n\n"
                    f"Deficiencies Identified by Evaluator:\n{missing_str}\n\n"
                    f"Actionable Critique:\n{latest_critique.actionable_critique}\n\n"
                    "Produce an improved and complete revised solution. Address all critique points "
                    "while preserving correct logic from the previous attempt."
                )

            logging.info(f"Generating candidate via [{self.generator_model}] (Iteration {iteration})...")
            gen_response = self.client.chat(
                model=self.generator_model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert solution generator. Deliver thorough, accurate, and high-quality answers.",
                    },
                    {"role": "user", "content": gen_prompt},
                ],
                options={"temperature": 0.7, "num_ctx": self.num_ctx},
            )
            candidate_output = gen_response["message"]["content"]

            # Step B: Evaluation with GBNF Constrained Grammar
            eval_system_prompt = (
                "You are an expert Quality Evaluator and System Auditor.\n"
                "Evaluate the candidate solution against the task requirement.\n"
                f"Pass threshold is {self.pass_threshold}. Be strict and objective."
            )

            eval_user_prompt = (
                f"Task Requirement:\n{task_prompt}\n\n"
                f"Candidate Solution:\n[BEGIN CANDIDATE]\n{candidate_output}\n[END CANDIDATE]\n\n"
                "Evaluate accuracy, completeness, and safety. Return structured assessment."
            )

            logging.info(f"Evaluating candidate via [{self.evaluator_model}]...")
            eval_response = self.client.chat(
                model=self.evaluator_model,
                format=CritiqueSchema.model_json_schema(),  # Native JSON Schema constraint in Ollama v0.5+
                messages=[
                    {"role": "system", "content": eval_system_prompt},
                    {"role": "user", "content": eval_user_prompt},
                ],
                options={"temperature": 0.0, "top_p": 0.1, "num_ctx": self.num_ctx},
            )

            # Step C: Parse & Validate Structured Critique
            raw_eval_json = eval_response["message"]["content"]
            try:
                eval_data = json.loads(raw_eval_json)
                latest_critique = CritiqueSchema(**eval_data)
            except (json.JSONDecodeError, ValidationError) as e:
                logging.error(f"Failed to parse Evaluator JSON: {e}. Raw content: {raw_eval_json}")
                latest_critique = CritiqueSchema(
                    score=0.0,
                    passed=False,
                    missing_elements=["Malformed evaluator output"],
                    actionable_critique="Ensure valid syntax and complete implementation addressing all core tasks.",
                )

            logging.info(
                f"Evaluator Score: {latest_critique.score:.2f} | "
                f"Passed Flag: {latest_critique.passed} | "
                f"Missing Items: {len(latest_critique.missing_elements)}"
            )

            iteration_history.append({
                "iteration": iteration,
                "score": latest_critique.score,
                "passed": latest_critique.passed,
                "missing_elements": latest_critique.missing_elements,
                "actionable_critique": latest_critique.actionable_critique,
            })

            # Step D: Strict Quality Gate Check
            if latest_critique.score >= self.pass_threshold:
                logging.info(f"✅ Quality threshold ({self.pass_threshold}) reached at iteration {iteration}!")
                return {
                    "status": "success",
                    "iterations": iteration,
                    "final_score": latest_critique.score,
                    "output": candidate_output,
                    "history": iteration_history,
                }

            logging.warning(
                f"⚠️ Iteration {iteration} failed quality gate (Score {latest_critique.score:.2f} < {self.pass_threshold}). "
                f"Critique: {latest_critique.actionable_critique}"
            )

        logging.warning("Reached maximum iterations without reaching pass threshold. Returning latest candidate output.")
        return {
            "status": "max_iterations_reached",
            "iterations": self.max_iterations,
            "final_score": latest_critique.score if latest_critique else 0.0,
            "output": candidate_output,
            "history": iteration_history,
        }


# Example Usage
if __name__ == "__main__":
    # Ensure Ollama is running locally: `ollama serve`
    harness = OllamaEvaluatorOptimizer(
        generator_model="qwen2.5:14b",
        evaluator_model="qwen2.5:14b",
        pass_threshold=0.85,
        max_iterations=3,
    )
    # result = harness.run("Write a Python script to perform binary search on a sorted list with edge case handling.")
    # print(f"Result Status: {result['status']}, Final Score: {result['final_score']}")
```
