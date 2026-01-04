'''
Demo file for RAG using single agent chat from Agents2 framework.
'''

import RAG
import Agents2
import Interaction
import ContextManager

model_path = "ibm-granite/granite-embedding-30m-english"

data_for_RAG = [
    "The user's favrite color is blue.",
    "Most cars are red."
    ]

rag_db = RAG.RAGdb(model_path=model_path, data=data_for_RAG)

mycontext=ContextManager.ContextManager(messages=[{"role":"system","content":"You are a helpful assistant."}])
a=Agents2.Agent("model here","http://127.0.0.1:8080/v1/chat/completions",temperature=0.7,max_tokens=4096)
chat=Interaction.SingleAgentChat(agent=a,username="User",machinename="AI",context=mycontext,stream=True,rag_db=rag_db)
chat.chat()