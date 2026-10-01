import json

# Mock LLM and TigerGraph client for demonstration purposes
class MockLLM:
    def generate(self, prompt):
        print(f"[LLM] Received prompt: {prompt}")
        # Simulate LLM generating a response based on retrieved context
        if "What is the capital of France?" in prompt:
            return "The capital of France is Paris."
        elif "Who is the CEO of Google?" in prompt:
            return "The CEO of Google is Sundar Pichai."
        else:
            return "I don't have enough information."

class MockTigerGraphClient:
    def query(self, gsql_query):
        print(f"[TigerGraph] Executing GSQL: {gsql_query}")
        # Simulate retrieving data from a knowledge graph
        if "MATCH (c:City)-[:IS_CAPITAL_OF]->(co:Country {name: \"France\"}) RETURN c.name" in gsql_query:
            return {"results": [{"c.name": "Paris"}]}
        elif "MATCH (p:Person)-[:IS_CEO_OF]->(co:Company {name: \"Google\"}) RETURN p.name" in gsql_query:
            return {"results": [{"p.name": "Sundar Pichai"}]}
        else:
            return {"results": []}

class GraphProbeAI:
    def __init__(self, llm, tigergraph_client):
        self.llm = llm
        self.tigergraph_client = tigergraph_client

    def ask(self, question):
        # 1. Retrieve relevant information from TigerGraph based on the question
        # This is a simplified retrieval step. In a real system, this would involve
        # more sophisticated GSQL queries or graph traversal logic.
        retrieved_context = ""
        if "capital of France" in question.lower():
            gsql_query = "USE GRAPH my_graph\nMATCH (c:City)-[:IS_CAPITAL_OF]->(co:Country {name: \"France\"}) RETURN c.name AS city_name"
            result = self.tigergraph_client.query(gsql_query)
            if result["results"]:
                retrieved_context = f"The capital is {result['results'][0]['city_name']}."
        elif "CEO of Google" in question.lower():
            gsql_query = "USE GRAPH my_graph\nMATCH (p:Person)-[:IS_CEO_OF]->(co:Company {name: \"Google\"}) RETURN p.name AS person_name"
            result = self.tigergraph_client.query(gsql_query)
            if result["results"]:
                retrieved_context = f"The CEO is {result['results'][0]['person_name']}."

        # 2. Augment the LLM prompt with the retrieved context
        augmented_prompt = f"Context: {retrieved_context}\nQuestion: {question}\nAnswer:"

        # 3. Generate the final answer using the LLM
        response = self.llm.generate(augmented_prompt)
        return response

if __name__ == "__main__":
    # Initialize mock components
    mock_llm = MockLLM()
    mock_tigergraph = MockTigerGraphClient()

    # Initialize GraphProbeAI system
    graph_rag_system = GraphProbeAI(llm=mock_llm, tigergraph_client=mock_tigergraph)

    # Example usage
    question1 = "What is the capital of France?"
    answer1 = graph_rag_system.ask(question1)
    print(f"Question: {question1}\nAnswer: {answer1}\n")

    question2 = "Who is the CEO of Google?"
    answer2 = graph_rag_system.ask(question2)
    print(f"Question: {question2}\nAnswer: {answer2}\n")

    question3 = "What is the population of Tokyo?" # This will not find context in mocks
    answer3 = graph_rag_system.ask(question3)
    print(f"Question: {question3}\nAnswer: {answer3}\n")
