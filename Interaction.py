from multiprocessing import context
import Agents2
import ContextManager

'''
Single agent chat function. Allows user to interact with one agent at a time.
'''
class SingleAgentChat:

    def __init__(self, agent:Agents2.Agent, username="User", machinename="AI", context:ContextManager.ContextManager=None, stream:bool=True, summarizer_agent=[Agents2.Agent, str], summarizer_mode:int=0):
        self.agent=agent
        self.username=username
        self.machinename=machinename
        self.context=context
        self.stream=stream
        #Summarizer agents will make a return in future iterations. Leaving this in for now.
        self.summarizer_agent=summarizer_agent
        self.summarizer_mode=summarizer_mode

    def chat(self):
        while True:
            try:
                #Getting user input
                user_cmd=input("Prompt>>>")
                self.context.append_to_context({"role":"user","content":user_cmd})
                #Calling the agent to generate a response and accounting for streaming or non-streaming modes.
                if self.stream:
                    print(f"{self.machinename}: ", end="", flush=True)
                    response = ""
                    for chunk in self.agent.agent_generate_stream(messages=self.context.messages, timeout=300):
                        print(chunk, end="", flush=True)
                        response += chunk
                    self.context.append_to_context({"role":"assistant","content":response})
                    print("")  # Newline after streaming is done
                else:
                    response=self.agent.agent_generate(messages=self.context.messages, timeout=300)
                    self.context.append_to_context({"role":"assistant","content":response})
                    print(f"{self.machinename}: {response}")
            #Allow user to stop generation
            except KeyboardInterrupt as k:
                print(f"\nSTOPPED GENERATION FOR {self.agent} BY USER INTERRUPT!")
            #Catch all for any other exceptions
            except Exception as e:
                print(f"Error: {e} occured.")
                break

'''
Multi agent chat function. Allows multiple agents to respond to user prompts in sequence.
'''
class MultiAgentChat:

    def __init__(self, roster:list, username="User", context:ContextManager.ContextManager=None, stream:bool=True, summarizer_agent=[Agents2.Agent, str], summarizer_mode:int=0):
        self.roster=roster
        self.username=username
        self.context=context
        self.stream=stream
        self.summarizer_agent=summarizer_agent
        self.summarizer_mode=summarizer_mode

    def chat(self):
        while True:
            try:
                #Debug feature which will be used differently in future versions
                user_cmd=input("Prompt>>>")
                if user_cmd == "PRINT":
                    print("Current Context Messages:")
                    for msg in self.context.messages:
                        print(msg)
                else:
                    #Getting user input
                    self.context.append_to_context({"role":"user","content":user_cmd})
                    '''
                    responses=[] will temporary hold each agents' response
                    This prevents agents' later down in the roster being influenced by earlier agents' responses in the same round.
                    After all agents have responded for the current prompt, all the responses are appended to context together.
                    '''
                    responses=[]
                    for agent in self.roster:
                        try:
                            self.context.messages[0]={"role":"system","content":agent.system_prompt} #Set system prompt for each agent
                            print(f"\n{agent.name} is responding...\n") #Inform user which agent is responding and helpful for debugging
                            #Calling the agent to generate a response and accounting for streaming or non-streaming modes.
                            if self.stream:
                                print(f"{agent.name}: ", end="", flush=True)
                                response = ""
                                for chunk in agent.agent_generate_stream(messages=self.context.messages, timeout=300):
                                    print(chunk, end="", flush=True)
                                    response += chunk
                                responses.append(response)
                                print("")  # Newline after streaming is done
                            else:
                                response=agent.agent_generate(messages=self.context.messages, timeout=300)
                                responses.append(response)
                                print(f"{agent.name}: {response}")
                        except KeyboardInterrupt as k:
                            print(f"\nSTOPPED GENERATION FOR {agent.name} BY USER INTERRUPT!")

                    '''
                    Append responses list to the context in the two lines below.
                    The for loop variables and zip() work nicely here to pair each agent with their respective response.
                    '''
                    for agent, resp in zip(self.roster, responses):
                        self.context.append_to_context({"role":"assistant","content":f"{agent.name}: {resp}"})
            except Exception as e:
                print(f"Error: {e} occured.")
                break

'''
Allows agents to debate/discuss a prompt in a roundtable format for a specified number of turns.
Set the temperature of all agents in the roster higher than usual (above 0.7) to prevent an eventual collapse into repetitive or similar responses.
'''
class RoundTable:
    def __init__(self, roster:list, username="User", context:ContextManager.ContextManager=None, stream:bool=True, summarizer_agent=[Agents2.Agent, str], summarizer_mode:int=0):
        self.roster=roster
        self.username=username
        self.context=context
        self.stream=stream
        self.summarizer_agent=summarizer_agent
        self.summarizer_mode=summarizer_mode
    
    '''
    Send one prompt and have agents discuss it for N turns.
    '''
    def auto_debate(self, prompt:str, turns:int=3, stream:bool=True):
        i=0                 
        self.context.append_to_context({"role":"user","content":prompt})
        '''
        This is a "two-layer" loop function or nested loop.
        The outer loop runs for the number of turns specified.
        The inner loop iterates through each agent in the roster for each turn.
        '''
        while i<turns:
            '''
            responses=[] will temporary hold each agents' response
            This prevents agents' later down in the roster being influenced by earlier agents' responses in the same round.
            After all agents have responded for the current prompt, all the responses are appended to context together.
            '''
            responses=[]
            for agent in self.roster:
                try:
                    self.context.messages[0]={"role":"system","content":agent.system_prompt}
                    print(f"\n{agent.name} is responding...\n")
                    if stream:
                        print(f"{agent.name}: ", end="", flush=True)
                        response = ""
                        for chunk in agent.agent_generate_stream(messages=self.context.messages, timeout=300):
                            print(chunk, end="", flush=True)
                            response += chunk
                        responses.append(response)
                        print("")  # Newline after streaming is done
                    else:
                        response=agent.agent_generate(messages=self.context.messages, timeout=300)
                        responses.append(response)
                        print(f"{agent.name}: {response}")
                except KeyboardInterrupt as k:
                    print(f"\nSTOPPED GENERATION FOR {agent.name} BY USER INTERRUPT!")

            '''
            Append responses list to the context in the two lines below.
            The for loop variables and zip() work nicely here to pair each agent with their respective response.
            '''
            for agent, resp in zip(self.roster, responses):
                self.context.append_to_context({"role":"assistant","content":f"{agent.name}: {resp}"})
            self.context.append_to_context({"role":"user","content":""})#Required to append blank user context to avoid 400 error.
            i+=1

    '''
    Send one prompt and have agents discuss it for N turns and then continue the process in a chat style.
    '''
    def council_chat(self, turns:int=3, stream:bool=True):
        while True:
            try:
                #Debug feature which will be used differently in future versions
                user_cmd=input("Prompt>>>")
                if user_cmd == "PRINT":
                    print("Current Context Messages:")
                    for msg in self.context.messages:
                        print(msg)
                else:
                    '''
                    This is a nested try-except.
                    The outer try-except allows the user to skip an entire round of discussion.
                    The inner try-except allows the user to stop generation for individual agents.
                    '''
                    try:
                        self.context.append_to_context({"role":"user","content":user_cmd})
                        i=0
                        '''
                        This is a "two-layer" loop function or nested loop.
                        The outer loop runs for the number of turns specified.
                        The inner loop iterates through each agent in the roster for each turn.
                        '''
                        while i<turns:
                            responses=[]
                            for agent in self.roster:
                                try:
                                    self.context.messages[0]={"role":"system","content":agent.system_prompt}
                                    print(f"\n{agent.name} is responding...\n")
                                    if stream:
                                        print(f"{agent.name}: ", end="", flush=True)
                                        response = ""
                                        for chunk in agent.agent_generate_stream(messages=self.context.messages, timeout=300):
                                            print(chunk, end="", flush=True)
                                            response += chunk
                                        responses.append(response)
                                        print("")  # Newline after streaming is done
                                    else:
                                        response=agent.agent_generate(messages=self.context.messages, timeout=300)
                                        responses.append(response)
                                        print(f"{agent.name}: {response}")
                                except KeyboardInterrupt as k:
                                    print(f"\nSTOPPED GENERATION FOR {agent.name} BY USER INTERRUPT!")
                            for agent, resp in zip(self.roster, responses):
                                self.context.append_to_context({"role":"assistant","content":f"{agent.name}: {resp}"})
                            self.context.append_to_context({"role":"user","content":""})#Required to append blank user context to avoid 400 error.
                            i+=1
                    except KeyboardInterrupt as k:
                        print(f"\nSTOPPED AND SKIPPING ROUND {i+1} BY USER INTERRUPT!")
            except Exception as e:
                print(f"Error: {e} occured.")
                break

if __name__ == "__main__":
    pass