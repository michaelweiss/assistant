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
            "content": """You are a helpful assistant. Give a concise answer. Start with 'Yes' or 'No'. If you don't know the answer say 'Sorry, I don't have the answer to that'."""})

    def handle_request(self, request):
        """
        Handle the request.
        """
        self.messages.append({"role": "user", "content": request})
        self.prune_messages()
        response = self.client.chat.completions.create(
            model=self.model,
            temperature=0, # low to reduce randomness
            messages=self.messages
        )
        response = response.choices[0].message.content
        self.messages.append({"role": "assistant", "content": response})
        return response

    def prune_messages(self, M=3, N=2):
        """
        Prune the messages.
        Keep the last M user and N assistant messages.
        """
        user_count = 0
        assistant_count = 0
        new_messages = []
        # Read messages from the end of the message history
        # Add the last M user and N assistant messages to the new history
        for message in reversed(self.messages):
            if message["role"] == "user" and user_count < M:
                new_messages.insert(0, message)
                user_count += 1
            elif message["role"] == "assistant" and assistant_count < N:
                new_messages.insert(0, message)
                assistant_count += 1
            elif message["role"] == "system":
                new_messages.insert(0, message)
        self.messages = new_messages