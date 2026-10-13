// ============================================================================
// KRISTIANSAND KOMMUNE - POWER QUERY M FUNCTION: fxOpenAI_RAG
// Purpose: On-demand, Human-Triggered Glass-Box AI Analysis with RAG Context
// Standard: Governed, Non-Blackbox, Auditable Municipal EPM Workflow
// ============================================================================

(
    ApiKey as text, 
    EndpointUrl as text, 
    DataRowContext as record, 
    RetrievedRulesText as text
) as record =>

let
    // 1. Serialize Data Context and RAG Rules into Structured JSON Prompt
    SerializedData = Text.FromBinary(Json.FromValue(DataRowContext)),
    
    SystemMessage = "You are a municipal financial advisor for Kristiansand kommune. " & 
                    "You MUST ground your answer strictly in the provided RAG rules and KOSTRA guidelines. " & 
                    "Provide a step-by-step reasoning chain and a confidence score. " & 
                    "Respond strictly in JSON format with keys: 'anomaly_summary', 'reasoning_chain', 'governance_reference', 'confidence_score', 'recommended_action'.",
    
    UserMessage = "DATA CONTEXT: " & SerializedData & "#(lf)#(lf)" & 
                  "RETRIEVED RAG RULES & KOSTRA GUIDELINES: " & RetrievedRulesText,

    // 2. Build Open API Payload with JSON Schema / JSON Mode Enforcement
    RequestBody = Json.FromValue([
        messages = {
            [role = "system", content = SystemMessage],
            [role = "user", content = UserMessage]
        },
        temperature = 0.1,
        response_format = [type = "json_object"]
    ]),

    // 3. Execute HTTP POST Request to Azure OpenAI Endpoint
    Response = Web.Contents(
        EndpointUrl,
        [
            Headers = [
                #"Content-Type" = "application/json",
                #"api-key" = ApiKey
            ],
            Content = RequestBody,
            ManualStatusHandling = {400, 401, 403, 500}
        ]
    ),

    // 4. Parse Response JSON Body
    JsonResponse = Json.Document(Response),
    
    // 5. Extract Structured Output
    Choices = JsonResponse[choices]{0}[message][content],
    ParsedContent = Json.Document(Choices),
    
    // 6. Return Clean M Record for Excel / Power BI
    ResultRecord = [
        AnomalySummary = ParsedContent[anomaly_summary],
        ReasoningChain = Text.Combine(ParsedContent[reasoning_chain], "#(lf)"),
        GovernanceReference = ParsedContent[governance_reference],
        ConfidenceScore = ParsedContent[confidence_score],
        RecommendedAction = ParsedContent[recommended_action],
        Timestamp = DateTime.LocalNow()
    ]
in
    ResultRecord
