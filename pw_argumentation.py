from mesa import Model
from mesa.time import RandomActivation

import random
from communication import preferences

from communication.agent.CommunicatingAgent import CommunicatingAgent
from communication.message.MessageService import MessageService

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

    def step (self) :
        super().step()

    def get_preference(self):
        return self.preference

    def generate_preferences(self, item_list):
        pref = Preferences()
        for item in item_list:
            for crit_name in CriterionName:
                crit_val = random.choice(list(Value))
                pref.add_criterion_value(CriterionValue(item, crit_name, crit_val))

        self.preference = pref

    def print_preferences(self):
        preferences = self.get_preference()
        for name, value in zip(preferences.get_criterion_name_list(), preferences.get_criterion_value_list()):
            print(f"{name}:{value}")

class ArgumentModel(Model):
    """ ArgumentModel which inherit from Model .
    """
    def __init__(self, item_list):
        super().__init__()
        self.schedule = RandomActivation(self)
        self.__messages_service = MessageService(self.schedule)
        # To be completed
        #
        # a = ArgumentAgent (id , " agent_name ")
        # a. generate_preferences ( preferences )
        # self . schedule .add(a)
        # ...

        a1 = ArgumentAgent(self.next_id(), self, "A1")
        a1.generate_preferences(item_list=item_list)
        a2 = ArgumentAgent(self.next_id(), self, "A2")
        a2.generate_preferences(item_list=item_list)

        a1.print_preferences() # marche pas
        a2.print_preferences()

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
# To be completed

