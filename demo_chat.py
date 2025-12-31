'''
Demo file for single agent chat using Agents2 framework.
'''

import Agents2
import Interaction
import ContextManager

mycontext=ContextManager.ContextManager(messages=[{"role":"system","content":"You are a helpful assistant."}])
a=Agents2.Agent("model here","http://127.0.0.1:8080/v1/chat/completions",temperature=0.7,max_tokens=4096)
chat=Interaction.SingleAgentChat(agent=a,username="User",machinename="AI",context=mycontext,stream=True,summarizer_agent=[None,""],summarizer_mode=0)
chat.chat()