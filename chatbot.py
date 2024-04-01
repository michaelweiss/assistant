class Chatbot():
    def __init__(self, client, model):
        """
        Initialize the chatbot.
        """
        self.client = client
        self.model = model
        self.reset()

    def reset(self):
        """
        Reset the chatbot.
        """
        self.messages = []
        self.messages.append({"role": "system", 
            "content": "You are a helpful assistant. Carefully follow the user's instructions."})

    def handle_request(self, request):
        """
        Handle the request.
        """
        self.messages.append({"role": "user", "content": request})
        response = self.client.chat.completions.create(
            model=self.model,
            temperature=0, # low to reduce randomness
            messages=self.messages
        )
        response = response.choices[0].message.content
        return response
