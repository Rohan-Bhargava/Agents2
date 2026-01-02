'''
Helper class to create and manage a menu system with selectable items and associated actions.
'''

class Menu:
    def __init__(self, items:list=[], actions:list=[]):
        self.items=items
        self.actions=actions
    
    # Select an action based on user input
    def select(self, user_choice:str):
        try:
            return self.actions[int(user_choice)]()
        except (IndexError, ValueError):
            print("ERR: ITEM DOES NOT HAVE ACTION")

    # Display the menu with various formatting options and return the menu as a string
    def display_menu(self, flags="", custom_phrase="", prependix="", appendix=""):
        menu_string=f""
        match flags:
            case "custom":
                if custom_phrase:
                    menu_string+=prependix
                    for i in range(len(self.items)):
                        menu_string+=custom_phrase
                    menu_string+=appendix
                    return menu_string
                else:
                    return "ERR: no custom string supplied"
            case "show actions":
                pass
            case _:
                menu_string = [f"{i}. {item}" for i, item in enumerate(self.items)]
                menu_string.append("Please select an option: ")
                return "\n".join(menu_string)
        
if __name__ == "__main__":
    pass