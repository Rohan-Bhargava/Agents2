import Agents2

a=Agents2.Agent("Model here","http://127.0.0.1:8080/v1/chat/completions",temperature=0.7,max_tokens=4096)
for chunk in a.agent_generate_stream("How are you?"):
    print(chunk, end="", flush=True)