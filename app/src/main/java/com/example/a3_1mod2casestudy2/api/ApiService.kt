package com.example.a3_1mod2casestudy2.api

import com.example.a3_1mod2casestudy2.models.PromptRequest
import com.example.a3_1mod2casestudy2.models.PromptResponse
import retrofit2.Response
import retrofit2.http.Body
import retrofit2.http.POST

interface ApiService {
    @POST("v1/chat/completions")
    suspend fun getPromptResponse(
        @Body request: PromptRequest
    ): Response<PromptResponse>
}
