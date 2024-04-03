from chatbot import Chatbot
from embeddings_utils import get_embedding

class KnowledgeChatbot(Chatbot):
    def __init__(self, client, model, database, threshold=.45):
        """
        Initialize the chatbot.
        """
        super().__init__(client, model)
        # Database for answering questions
        self.database = database
        # Threshold for the similarity score
        self.threshold = threshold

    def handle_request(self, request):
        """
        Handle the request.
        """
        try:
            # Get the best matching results from the database
            results = self.database.query(get_embedding(request))
            # Check if the confidence score between the user input and the document meets the threshold
            context = [result[0] for result in results if result[1] >= self.threshold]
            context = "\n".join(context)
            # Add the best matching results to the prompt
            prompt = self.cot_prompt(context, request)
            return super().handle_request(prompt)
        except Exception as e:
            return "Server error. Please try again later."
        
    """
    The following prompt templates (simple, CoT, and comprehensive) are based on Mao et al. (2024).
    FIT-RAG: Black-Box RAG with Factual Information and Token Reduction.
    """

    def simple_prompt(self, context, request):
        """
        Create a simple prompt.
        """
        return f"""Refer to the passages below and answer the following question.
            Passages: {context}
            Question: {request}
            The answer is
            """
    
    def cot_prompt(self, context, request):
        """
        Create a CoT prompt.
        """
        return f"""Refer to the passages below and answer the following question.
            Passages: {context}
            Question: {request}
            Let's think step by step.
            The answer is
            """
    
    def comprehensive_prompt(self, context, request):
        """
        Create a comprehensive prompt.
        """
        return f"""Refer to the passages below and answer the following question.
            Make sure you fully understand the meaning of the question and passages.
            Then give the answer and explain why you choose this answer.
            Passages: {context}
            Question: {request}
            The answer is 
            """