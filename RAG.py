'''

Simple RAG engine
Made by Rohan Bhargava

'''

from sentence_transformers import SentenceTransformer, util
import torch

class RAGdb():
    def __init__(self, model_path: str, data: list):
        self.model = SentenceTransformer(model_path)
        self.data = data

    def add_data(self, new_data: list):
        try:
            self.data.extend(new_data)
        except Exception as e:
            return f"Error adding data: {e}"

    def inference(self, queries: list, top_k: int=1, debug: bool=False, cutoff:float=0.50):
        try:
            # encode queries and passages
            query_embeddings = self.model.encode(queries)
            data_embeddings = self.model.encode(self.data)

            # calculate cosine similarity and get top_k results and indices
            values, indices = torch.topk(input=util.cos_sim(query_embeddings, data_embeddings), k=top_k, dim=1)
            retrieved_data = [self.data[int(i)] for i in indices[0].tolist()]
            if min(values[0]).item() < cutoff:
                return None
            else:
                if debug:
                    return retrieved_data, values.tolist()
                else:
                    return retrieved_data
        except Exception as e:
            return f"Error during inference: {e}"