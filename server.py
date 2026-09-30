"""
Prompt Strategy Comparison - Local LLM Proxy & Mock Server
Supports testing Zero-Shot, Few-Shot, and Structured Prompt strategy responses.
Run using: python server.py
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import time
import re

class PromptRequestHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        if self.path in ["/v1/chat/completions", "/api/prompt"]:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            
            try:
                request_json = json.loads(post_data.decode('utf-8'))
                messages = request_json.get('messages', [])
                prompt_content = messages[-1].get('content', '') if messages else ''
                
                # Detect prompt strategy type based on content markers
                response_text = self.generate_completion_response(prompt_content)
                
                response_data = {
                    "id": f"chatcmpl-{int(time.time())}",
                    "object": "chat.completion",
                    "created": int(time.time()),
                    "model": request_json.get("model", "mock-grok-beta"),
                    "choices": [
                        {
                            "index": 0,
                            "message": {
                                "role": "assistant",
                                "content": response_text
                            },
                            "finish_reason": "stop"
                        }
                    ]
                }

                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(response_data).encode('utf-8'))

            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                error_response = {"error": str(e)}
                self.wfile.write(json.dumps(error_response).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

    def generate_completion_response(self, prompt: str) -> str:
        # Check if Structured Prompt
        if "[SYSTEM ROLE]" in prompt and "[OUTPUT SCHEMA]" in prompt:
            # Extract topic
            topic_match = re.search(r'Topic:\s*"(.*?)"', prompt)
            topic = topic_match.group(1) if topic_match else "Target Domain"
            
            return json.dumps({
                "topic": topic,
                "executive_summary": f"Comprehensive technical analysis of {topic} focusing on core architectural trade-offs.",
                "core_pillars": [
                    f"Scalable {topic} Architecture",
                    "Data Integrity & Real-time Processing",
                    "Security & Compliance Protocols"
                ],
                "risk_assessment": {
                    "level": "Medium",
                    "primary_risk": f"Latency bottlenecks during peak execution in {topic} pipelines."
                },
                "recommended_action": f"Implement modular asynchronous queues and strict input schema validation for {topic}."
            }, indent=2)

        # Check if Few-Shot Prompt
        elif "Example 1:" in prompt or "Example 2:" in prompt:
            # Extract topic after Input:
            input_matches = re.findall(r'Input:\s*(.*)', prompt)
            topic = input_matches[-1].strip() if input_matches else "Target Domain"
            
            return f"""- Overview: Enterprise deployment of {topic} focusing on operational efficiency.
- Key Benefit: Increases automated workflow throughput and reduces manual intervention error rates.
- Challenge: System migration overhead and initial model calibration complexity."""

        # Default Zero-Shot Prompt
        else:
            # Simple direct response
            clean_prompt = prompt.replace("Perform the following task:", "").strip()
            return f"""Here is an overview of {clean_prompt}:
{clean_prompt} plays a significant role in modern software and technology systems. It encompasses various methodologies, tools, and practices designed to optimize efficiency, security, and performance. 

Key aspects include foundational setup, workflow integration, performance monitoring, and domain maintenance. Implementing best practices ensures robust long-term outcomes."""

def run(server_class=HTTPServer, handler_class=PromptRequestHandler, port=5000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"🚀 Prompt Evaluation Server running on port {port}...")
    print(f"📲 Android Emulator can connect via http://10.0.2.2:{port}/v1/chat/completions")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")

if __name__ == '__main__':
    run()
