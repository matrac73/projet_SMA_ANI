import sys
sys.path.append("C:/Users/mathi/Bureau/projet_SMA_ANI")
sys.path.append("C:/Users/killi/desktop/sma")

from mesa import Model
from mesa.time import RandomActivation

import random
from communication import preferences

from communication.agent.CommunicatingAgent import CommunicatingAgent
from communication.message.MessageService import MessageService
from communication.message.Message import Message
from communication.message.MessagePerformative import MessagePerformative

from communication.preferences.Preferences import Preferences
from communication.preferences.CriterionName import CriterionName
from communication.preferences.CriterionValue import CriterionValue
from communication.preferences.Item import Item
from communication.preferences.Value import Value

class ArgumentAgent (CommunicatingAgent) :
    """ ArgumentAgent which inherit from CommunicatingAgent .
    """
    def __init__(self, unique_id, model, name):
        super().__init__(unique_id, model, name)
        self.preference = None
        self.accepted_item = None


    def step (self) :
        super().step()
        list_messages = self.get_new_messages()
        for message in list_messages:
            print(message)
            if message.get_performative() == MessagePerformative.PROPOSE:
                if self.get_preference().is_item_among_top_10_percent(message.get_content(), argument_model.item_list):
                    self.send_message(Message(self.get_name(), message.get_exp(), MessagePerformative.ACCEPT, message.get_content()))
            
            if message.get_performative() == MessagePerformative.ASK_WHY:
                #self.send_message(Message(self.get_name(), message.get_exp(), MessagePerformative.ASK_WHY, self.__v))
                pass
            
            if message.get_performative() == MessagePerformative.COMMIT:
                #self.send_message(Message(self.get_name(), message.get_exp(), MessagePerformative.ASK_WHY, self.__v))
                pass
                

    def get_preference(self):
        return self.preference

    def generate_preferences(self, item_list):
        pref = Preferences()
        pref.set_criterion_name_list([crit_name for crit_name in CriterionName])
        for item in item_list:
            for crit_name in CriterionName:
                crit_val = random.choice(list(Value))
                pref.add_criterion_value(CriterionValue(item, crit_name, crit_val))
                
                
        self.preference = pref

    def print_preferences(self):
        preferences = self.get_preference()
        for crit in preferences.get_criterion_value_list():
            print(f"{crit.get_item()}, {crit.get_criterion_name()}, {crit.get_value()}")

class ArgumentModel(Model):
    """ ArgumentModel which inherit from Model .
    """
    def __init__(self, item_list):
        super().__init__()
        self.schedule = RandomActivation(self)
        self.__messages_service = MessageService(self.schedule)
        self.item_list = item_list
        a1 = ArgumentAgent(self.next_id(), self, "A1")
        a1.generate_preferences(item_list=item_list)
        a2 = ArgumentAgent(self.next_id(), self, "A2")
        a2.generate_preferences(item_list=item_list)

        # a1.print_preferences()
        # a2.print_preferences()

        self.schedule.add(a1)
        self.schedule.add(a2)

        self.running = True

    def step(self):
        self.__messages_service.dispatch_messages()
        self.schedule.step()

    
if __name__ == "__main__":
    diesel_engine = Item("Diesel Engine", "A super cool diesel engine")
    electric_engine = Item("Electric Engine", "A very quiet engine")

    argument_model = ArgumentModel([electric_engine, diesel_engine])

    Alice =argument_model.schedule.agents[0]
    Bob = argument_model.schedule.agents[1]
    assert(Alice.get_name() == "A1")
    assert(Bob.get_name() == "A2")
    print("*     get_name() => OK")

    Alice.send_message(Message("A1", "A2", MessagePerformative.PROPOSE, electric_engine))
    

    #Alice.send_message(message_1)
    messages_bob = Bob.get_new_messages()
    print(messages_bob[0])
    if Bob.get_preference().is_item_among_top_10_percent(messages_bob[0].get_content(), argument_model.item_list):
        Bob.send_message(Message("A2", "A1", MessagePerformative.ACCEPT, messages_bob[0].get_content()))
    else:
        Bob.send_message(Message("A2", "A1", MessagePerformative.ASK_WHY, messages_bob[0].get_content()))
    


    messages_alice= Alice.get_new_messages()
    print(messages_alice[0])
    
    
    

