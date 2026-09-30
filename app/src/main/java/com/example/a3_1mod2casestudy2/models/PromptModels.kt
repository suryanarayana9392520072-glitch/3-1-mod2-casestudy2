package com.example.a3_1mod2casestudy2.models

import com.google.gson.annotations.SerializedName

data class PromptRequest(
    @SerializedName("messages") val messages: List<Map<String, String>>,
    @SerializedName("model") val model: String = "grok-beta",
    @SerializedName("temperature") val temperature: Double = 0.7
)

data class PromptResponse(
    @SerializedName("id") val id: String? = null,
    @SerializedName("choices") val choices: List<Choice>? = null
)

data class Choice(
    @SerializedName("index") val index: Int = 0,
    @SerializedName("message") val message: Message? = null
)

data class Message(
    @SerializedName("role") val role: String? = null,
    @SerializedName("content") val content: String? = null
)

data class EvaluationMetrics(
    val promptType: String,
    val wordCount: Int,
    val hasStructuredFormat: Boolean,
    val clarityScore: Int,
    val hallucinationRisk: String
)
