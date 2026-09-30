package com.example.a3_1mod2casestudy2.utils

class PromptGenerator {

    /**
     * Strategy 1: Zero-Shot Prompting
     * Provides direct instruction without background context or response examples.
     */
    fun generateZeroShotPrompt(topic: String): String {
        return "Perform the following task: $topic. Provide a complete output."
    }

    /**
     * Strategy 2: Few-Shot Prompting
     * Provides few-shot exemplar input-output pairs to guide format, style, and tone.
     */
    fun generateFewShotPrompt(topic: String): String {
        return """
            Task: Analyze the topic or input and summarize key points with structured key-value format.
            
            Example 1:
            Input: Quantum Computing Applications
            Output:
            - Overview: Uses qubits to process complex data exponentially faster.
            - Key Benefit: Accelerates cryptography, drug discovery, and optimization problems.
            - Challenge: High error rates and hardware decoherence.

            Example 2:
            Input: Renewable Energy Adoption
            Output:
            - Overview: Transition to solar, wind, and hydro energy sources.
            - Key Benefit: Lowers carbon emissions and creates sustainable energy grids.
            - Challenge: Intermittency and grid infrastructure storage limitations.

            Now complete the following task:
            Input: $topic
            Output:
        """.trimIndent()
    }

    /**
     * Strategy 3: Structured Prompting
     * Defines Role, Context, Task Specification, Output Schema, and Strict Constraints.
     */
    fun generateStructuredPrompt(topic: String): String {
        return """
            [SYSTEM ROLE]
            You are an expert AI Domain Specialist and Technical Evaluator.

            [CONTEXT]
            The user requires a precise, production-grade analysis of the given topic without unnecessary fluff or hallucinated facts.

            [TASK]
            Analyze the target topic and generate a structured response adhering strictly to the JSON schema below.

            [INPUT PAYLOAD]
            Topic: "$topic"

            [CONSTRAINTS]
            1. Output MUST be valid JSON only. Do NOT include markdown code block formatting like ```json.
            2. Do NOT hallucinate unverified statistical claims.
            3. Tone must be technical, objective, and analytical.

            [OUTPUT SCHEMA]
            {
              "topic": "String",
              "executive_summary": "String (max 50 words)",
              "core_pillars": ["String", "String", "String"],
              "risk_assessment": {
                "level": "Low | Medium | High",
                "primary_risk": "String"
              },
              "recommended_action": "String"
            }
        """.trimIndent()
    }
}
