class ContextManager:
    def __init__(self, messages:list=[]):
        self.messages = messages

    def append_to_context(self, addition:dict):
        self.messages.append(addition)
        return

if __name__ == "__main__":
    pass