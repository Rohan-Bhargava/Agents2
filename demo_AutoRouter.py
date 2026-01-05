'''
Demo file for AutoRouter.
'''

import RAG
import Agents2
import AutoRouter
import ContextManager

embedding_model = "ibm-granite/granite-embedding-30m-english"

mycontext=ContextManager.ContextManager(messages=[{"role":"system","content":"You are a helpful assistant."}])
a=Agents2.Agent("model here","http://127.0.0.1:8080/v1/chat/completions",temperature=0.7,max_tokens=4096, system_prompt="You are an expert in geography.")
b=Agents2.Agent("model here","http://127.0.0.1:8080/v1/chat/completions",temperature=0.7,max_tokens=4096, system_prompt="You are an expert in history.")
c=Agents2.Agent("model here","http://127.0.0.1:8080/v1/chat/completions",temperature=0.7,max_tokens=4096, system_prompt="You are an expert in science.")

route=AutoRouter.AutoRouter(agents_list=[a,b,c], embedding_model_path=embedding_model)
selected_agent=route.route_query(query="What is the capital of France?", RAG_cutoff=0.50)
print(f"Routed to agent with system prompt: {selected_agent.system_prompt}")