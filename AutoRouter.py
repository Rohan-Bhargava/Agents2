import RAG
import Agents2

class AutoRouter:
    def __init__(self, agents_list: list, embedding_model_path: str):
        self.agents = agents_list
        self.embedding_model_path = embedding_model_path

    def route_query(self, query: str, use_entire_context_for_RAG:bool=False, RAG_top_k:int=1, RAG_system_prompt:str="", RAG_cutoff:float=0.50) -> str:
        # Create a RAG database with agent descriptions
        agent_descriptions = [agent.system_prompt for agent in self.agents]
        rag_db = RAG.RAGdb(model_path=self.embedding_model_path, data=agent_descriptions)

        # Perform RAG retrieval to find the most relevant agent
        retrieved_agents = rag_db.inference(queries=[query], top_k=1, cutoff=RAG_cutoff)
        if retrieved_agents:
            selected_agent_description = retrieved_agents[0]
            # Find the corresponding agent
            for agent in self.agents:
                if agent.system_prompt == selected_agent_description:
                    return agent
        return None