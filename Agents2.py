'''

Simple Agent handler that is a client for llama.cpp servers
Made by Rohan Bhargava

'''

import json
import sys
import time
from typing import Generator
import requests
import RAG

class Agent:
    def __init__(self, model, server, name:str="", system_prompt:str="", temperature:float=0.7, top_p:float=1.0, max_tokens:int=512, top_k:int=25, ):
        self.model = model
        self.server = server
        self.name = name
        self.temperature = temperature
        self.top_p = top_p
        self.max_tokens = max_tokens
        self.top_k = top_k
        self.system_prompt = system_prompt


    # Helper function: a tiny generator that yields partial JSON objects from a stream.
    def json_lines_from_stream(self, response: requests.Response) -> Generator[str, None, None]:
        buffer = ""
        for chunk in response.iter_content(chunk_size=1024, decode_unicode=True):
            if not chunk:
                break
            buffer += chunk
            # Split on new‑lines – each line should be a complete JSON object.
            # Empty lines are ignored (they can appear at the very end).
            lines = buffer.split("\n")
            buffer = lines.pop()  # keep the incomplete tail for the next iteration
            for line in lines:
                if line.strip():
                    yield line.strip()
        # Yield any trailing line that might not have been terminated by a newline.
        if buffer.strip():
            yield buffer.strip()

    #Streaming generation method - this function is VERY IMPORTANT and is the backbone of the entire Agents2 framework.
    def agent_generate_stream(self, messages:list, timeout:int=300, rag_db:RAG.RAGdb=None, use_entire_context_for_RAG:bool=False, RAG_top_k:int=1, RAG_system_prompt:str="", RAG_cutoff:float=0.50) -> Generator[str, None, None]:
        if rag_db is not None:
            # Perform RAG retrieval
            if use_entire_context_for_RAG:
                #use the entire context for RAG
                query_contents = [msg["content"] for msg in messages]
            else:
                #use only the latest message for RAG, usually the latest user prompt
                query_contents = [messages[-1]["content"]]
            retrieved_data = rag_db.inference(queries=query_contents, top_k=RAG_top_k, cutoff=RAG_cutoff)
            if retrieved_data is not None:
                messages.append({"role": "user", "content": f"{RAG_system_prompt}: {retrieved_data}"})

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "max_tokens": self.max_tokens,
            "top_k": self.top_k,
            "stream": True,
        }

        headers = {"Content-Type": "application/json"}

        try:
            with requests.post(self.server, json=payload, headers=headers, stream=True, timeout=timeout) as resp:
                resp.raise_for_status()

                for line in self.json_lines_from_stream(resp):
                    # 1. Filter out keep-alive comments or empty lines
                    if not line or line.startswith(":"):
                        continue

                    # 2. Strip the "data: " prefix (standard for SSE/llama.cpp)
                    if line.startswith("data: "):
                        line = line[6:]

                    # 3. Handle the [DONE] signal
                    if line.strip() == "[DONE]":
                        break

                    try:
                        data = json.loads(line)
                        token = ""

                        # Extract content based on API format (OpenAI compatible vs standard)
                        if "choices" in data and len(data["choices"]) > 0:
                            choice = data["choices"][0]
                            if "delta" in choice and "content" in choice["delta"]:
                                token = choice["delta"]["content"]
                            elif "text" in choice:
                                token = choice["text"]
                        
                        # Yield the token immediately for streaming
                        if token:
                            yield token

                    except json.JSONDecodeError:
                        continue
        #Will improve error handling
        except requests.exceptions.RequestException as exc:
            sys.stderr.write(f"[ERROR] HTTP request failed: {exc}\n")
            print(exc)
    
    #Non-streaming generation method - this function is VERY IMPORTANT and is the backbone of the entire Agents2 framework.
    def agent_generate(self, messages:list, timeout:int=300) -> str:
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "max_tokens": self.max_tokens,
            "top_k": self.top_k,
            "stream": False, 
        }

        headers = {"Content-Type": "application/json"}

        try:
            with requests.post(self.server, json=payload, headers=headers, timeout=timeout) as resp:
                resp.raise_for_status()
                
                # Parse the entire JSON response at once
                data = resp.json()
                
                # Extract text based on standard OpenAI/llama-cpp format
                if "choices" in data and len(data["choices"]) > 0:
                    choice = data["choices"][0]
                    
                    # Check for Chat Completion format (message.content)
                    if "message" in choice and "content" in choice["message"]:
                        return choice["message"]["content"]
                    
                    # Check for Legacy/Text Completion format (text)
                    elif "text" in choice:
                        return choice["text"]
                
        #error handling
        except requests.exceptions.RequestException as exc:
            sys.stderr.write(f"[ERROR] HTTP request failed: {exc}\n")
            print(exc)
            return "" #May add error code or forward HTTP error code

if __name__ == "__main__":
    pass