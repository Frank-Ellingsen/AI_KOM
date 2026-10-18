# User Testing & Pre-Deployment Simulation Blueprint

A comprehensive, production-ready guide to simulating user interactions, identifying UX friction points, and automating evaluation gates before deploying AI applications.

---

## 1. Overview & Strategy

Simulating user tests before deploying an application allows engineering and product teams to detect usability bottlenecks, navigation loops, edge-case failures, and safety issues before real users encounter them.

This blueprint combines four complementary testing vectors:
1. **Synthetic Persona Testing**: Automated LLM agents navigating UI workflows via headless browser automation.
2. **Unmoderated Quantitative Testing**: Prototype task analytics (clickmaps, drop-off rates, time-on-task).
3. **AI-Moderated Qualitative Probing**: Real-time natural language follow-up interviews upon detecting user hesitation.
4. **CI/CD Golden Dataset Evaluation Gates**: Regression testing against curated failure traces.

---

## 2. Phase 1: Synthetic Persona Simulation

Synthetic AI User Personas interact with the web application through browser automation frameworks (e.g., Playwright, Puppeteer).

### Persona Matrix

| Persona ID | Role / Profile | Behavior Pattern | Target Validation Focus |
| :--- | :--- | :--- | :--- |
| `P1_NOVICE` | Novice / Non-Technical User | Skips instructions, clicks primary buttons, expects 1-click results. | Onboarding flow, clear labeling, error messages. |
| `P2_POWER` | Power User / Analyst | Uses complex filters, keyboard navigation, rapid sequence actions. | Performance, multi-tab state persistence, bulk exports. |
| `P3_CHAOS` | Adversarial / Chaos Tester | Injects invalid strings, triggers out-of-order steps, rapid double clicks. | Input validation, error boundary handling, resilience. |

### Persona Prompt Template (`P1_NOVICE`)

```markdown
You are simulating a first-time user of the application.
- Technical Literacy: Low
- Goal: Complete the variance analysis report for Department 202.
- Rules:
  1. Do not read help documentation unless blocked twice.
  2. If an error occurs, try clicking the most obvious button on screen.
  3. Log your step-by-step thinking and any points of confusion in JSON format.
```

---

## 3. Phase 2: Unmoderated Prototype Testing

When testing with human cohorts or unmoderated testing tools (e.g., Maze, Useberry, UXtweak), track quantitative UX metrics:

* **Task Success Rate (TSR)**: Percentage of users completing the goal without critical errors.
* **Direct Success vs. Indirect Success**: Percentage of users taking the optimal path vs. exploring workarounds.
* **Misclick Rate**: Percentage of clicks on non-interactive UI elements.
* **System Usability Scale (SUS)**: Post-test 10-item questionnaire benchmark (target score > 68).

---

## 4. Phase 3: AI-Moderated Qualitative Probing

Deploy an AI Interview Moderator during live or recorded user sessions:

```
[User Interaction Stream]
         │
         ▼
[Hesitation Detector] ──(Pause > 5s or > 3 Misclicks)──► [AI Probing Prompt]
                                                                  │
                                                                  ▼
                                                      "I noticed you paused here.
                                                       What were you expecting
                                                       this button to do?"
```

---

## 5. Phase 4: Small-Batch Human Validation (The 5-User Rule)

According to Nielsen Norman Group research, **5 representative human users uncover ~85% of core usability issues**.

### Protocol:
1. Recruit 5 participants matching target user roles.
2. Instruct them to **think aloud** while completing 3 key scenario tasks.
3. Record screen, audio, and UI click events.
4. Categorize issues into:
   * **Blockers** (Unable to complete task)
   * **Major Friction** (Significant delay or frustration)
   * **Minor Polish** (Visual alignment, label phrasing)

---

## 6. Phase 5: CI/CD Golden Dataset & Pre-Deployment Gates

Convert user test failure traces into a permanent **Golden Dataset** for automated regression testing.

### Automated Quality Gate Matrix

```yaml
quality_gates:
  min_task_completion_rate: 0.95
  max_allowed_error_rate: 0.02
  evaluation_metrics:
    - name: "factual_consistency"
      min_score: 0.90
    - name: "answer_relevance"
      min_score: 0.85
    - name: "ui_schema_compliance"
      min_score: 1.00
  block_deployment_on_failure: true
```

---

## 7. Execution Checklist Before Deployment

- [ ] Run synthetic agent test suite (`P1_NOVICE`, `P2_POWER`, `P3_CHAOS`) via Playwright.
- [ ] Fix all identified blocker and major friction UI bugs.
- [ ] Ingest new edge-case failure traces into the Golden Dataset.
- [ ] Verify CI/CD pre-deployment evaluation gates pass (`score >= 0.90`).
- [ ] Conduct final 5-user human verification session.
- [ ] Obtain sign-off and deploy to production.
