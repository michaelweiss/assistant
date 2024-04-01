class Chatbot():
    def __init__(self, client, model):
        """
        Initialize the chatbot.
        """
        self.client = client
        self.model = model

    def handle_request(self, request):
        """
        Handle the request.
        """
        messages = [
            {"role": "system", "content": "You are a helpful assistant. Carefully follow the user's instructions."},
            {"role": "user", "content": request}
        ]
        response = self.client.chat.completions.create(
            model=self.model,
            temperature=0, # low to reduce randomness
            messages=messages
        )
        response = response.choices[0].message.content
        return response
