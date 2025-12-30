from multiprocessing import context
import Agents2
import ContextManager

'''
Single agent chat function. Allows user to interact with one sub-agent at a time.
'''

class SingleAgentChat:

    def __init__(self, agent:Agents2.Agent, username="User", machinename="AI", context:ContextManager.ContextManager=None, stream:bool=True, summarizer_agent=[Agents2.Agent, str], summarizer_mode:int=0):
        self.agent=agent
        self.username=username
        self.machinename=machinename
        self.context=context
        self.stream=stream
        self.summarizer_agent=summarizer_agent
        self.summarizer_mode=summarizer_mode

    def chat(self):
        while True:
            try:
                user_cmd=input("Prompt>>>")
                self.context.append_to_context({"role":"user","content":user_cmd})
                if self.stream:
                    print(f"{self.machinename}: ", end="", flush=True)
                    response = ""
                    for chunk in self.agent.agent_generate_stream(messages=self.context.messages, stream_timeout=300):
                        print(chunk, end="", flush=True)
                        response += chunk
                    self.context.append_to_context({"role":"assistant","content":response})
                    print("")  # Newline after streaming is done
                else:
                    response=self.agent.agent_generate(messages=self.context.messages, stream_timeout=300)
                    self.context.append_to_context({"role":"assistant","content":response})
                    print(f"{self.machinename}: {response}")
            except KeyboardInterrupt as k:
                print(f"\nSTOPPED GENERATION FOR {self.agent} BY USER INTERRUPT!")
            except Exception as e:
                print(f"Error: {e} occured.")
                break