import menu

class ContextManager:
    def __init__(self, messages:list=[]):
        self.messages = messages

    def append_to_context(self, addition:dict):
        self.messages.append(addition)
        return
    
    def clear_context(self):
        self.messages = []
        return
    
    def view_context(self):
        if not self.messages:
            print("ERR: CONTEXT IS EMPTY")
            return
        for i, msg in enumerate(self.messages):
            print(f"{i}. Role: {msg['role']}, Content: {msg['content']}")
        return
    
    def delete_message(self):
        if not self.messages:
            print("ERR: CONTEXT IS EMPTY")
            return
        msg_num=int(input("Please select context message to delete based off number (Enter -1 to exit):"))
        if msg_num == -1:
            print("No message deleted, exiting.")
            return
        else:
            try:
                del self.messages[msg_num]
                print(f"Message {msg_num} deleted.")
            except IndexError:
                print("ERR: MESSAGE NUMBER OUT OF RANGE")
        return

    def modify_context(self):
        exit_menu=False
        m=menu.Menu(items=["View Context","Delete Messages", "Return"], actions=[self.view_context, self.delete_message, lambda:True])
        while not exit_menu:
            print(m.display_menu())
            exit_menu=m.select(user_choice=int(input("Select option: ")))
        return

if __name__ == "__main__":
    pass