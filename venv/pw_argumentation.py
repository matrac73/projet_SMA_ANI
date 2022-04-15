import sys
sys.path.append("C:/Users/mathi/Bureau/projet_SMA_ANI")
sys.path.append("C:/Users/killi/desktop/projet_SMA_ANI")

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

from communication.arguments.CoupleValue import CoupleValue
from communication.arguments.Comparison import Comparison
from communication.arguments.Argument import Argument

class ArgumentAgent (CommunicatingAgent) :
    """ ArgumentAgent which inherit from CommunicatingAgent .
    """
    def __init__(self, unique_id, model, name):
        super().__init__(unique_id, model, name)
        self.preference = None
        
        
        self.item_left_to_propose = []

        self.arguments_in_motion = []
        
        self.has_commit = False
        self.has_accepted = False
        self.choosen_item = None
        self.pro_arguments = dict()
        self.con_arguments = dict()

    def step (self) :
        super().step()
        
        #print(self.get_name())
        list_messages = self.get_new_messages()
        
        for message in list_messages:
            print(self.get_name())
            print(message)
            if message.get_performative() == MessagePerformative.PROPOSE:
                self.item_left_to_propose.remove(message.get_content())
                if self.get_preference().is_item_among_top_10_percent(message.get_content(), argument_model.item_list):# or (len(self.item_left_to_propose) == 0 and ):
                    self.has_accepted = True
                    self.send_message(Message(self.get_name(), message.get_exp(), MessagePerformative.ACCEPT, message.get_content()))
                    #self.send_message(Message(self.get_name(), message.get_exp(), MessagePerformative.COMMIT, message.get_content()))
                else:
                    self.construct_counter_arguments(message.get_content())
                    self.send_message(Message(self.get_name(), message.get_exp(), MessagePerformative.ASK_WHY, message.get_content()))
            elif message.get_performative() == MessagePerformative.ASK_WHY:
                support_argument = self.support_proposal(message.get_content())
                if support_argument != None:
                    self.send_message(Message(self.get_name(), message.get_exp(), MessagePerformative.ARGUE, support_argument))
                else:
                    if len(self.arguments_in_motion) > 0:
                        #print("ddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd")
                        old_argument = self.arguments_in_motion.pop()
                        _,old_item,_,_ = self.argument_parsing(old_argument)
                        attack = self.attack_argument(old_argument)
                        if attack == None: # no counter argument # we can't counter the presented object, that mean we accept it
                            self.has_accepted = True
                            self.send_message(Message(self.get_name(), message.get_exp(), MessagePerformative.ACCEPT, old_item))
                        else:
                            _,attack_item,_,_ = self.argument_parsing(attack)
                            if attack_item != old_item:
                                # we are counter proposing, need to put the argumentation on the current object on the argument still in motion list
                                self.arguments_in_motion.append(old_argument)
                                #print("after", [item.get_name() for item in self.item_left_to_propose])
                                self.item_left_to_propose.remove(attack_item)
                                #print("afterafter", [item.get_name() for item in self.item_left_to_propose])
                                self.construct_support_arguments(attack_item)
                                self.send_message(Message(self.get_name(), message.get_exp(), MessagePerformative.PROPOSE, attack_item))
                            else:
                                self.send_message(Message(self.get_name(), message.get_exp(), MessagePerformative.ARGUE, attack))
                    else: 
                        if len(self.item_left_to_propose) > 0:
                            self.send_proposal(message.get_exp())
                        else:
                            # technically we are out of items and all of them were rejected by one of the party, so we could say that no items were selected.
                            # Instead we just accept whatever item was in talk now
                            self.has_accepted = True
                            self.send_message(Message(self.get_name(), message.get_exp(), MessagePerformative.ACCEPT, message.get_content()))
                            #self.send_message(Message(self.get_name(), message.get_exp(), MessagePerformative.ACCEPT, old_item))
            
            elif message.get_performative() == MessagePerformative.COMMIT:
                if not self.has_commit:
                    self.send_message(Message(self.get_name(), message.get_exp(), MessagePerformative.COMMIT, message.get_content()))
                    self.choosen_item = message.get_content()
                    self.has_commit = True

            elif message.get_performative() == MessagePerformative.ARGUE:
                decision, item, couple, comparison = self.argument_parsing(message.get_content())
                if decision:                     
                    attack = self.attack_argument(message.get_content())
                    if attack == None: # no counter argument # we can't counter the presented object, that mean we accept it
                        self.has_accepted = True
                        self.send_message(Message(self.get_name(), message.get_exp(), MessagePerformative.ACCEPT, item))
                    else:
                        _,attack_item,_,_ = self.argument_parsing(attack)
                        if attack_item != item:
                            # we are counter proposing, need to put the argumentation on the current object on the argument still in motion list
                            self.arguments_in_motion.append(message.get_content())
                            #print("after", [item.get_name() for item in self.item_left_to_propose])
                            self.item_left_to_propose.remove(attack_item)
                            
                            #print("afterafter", [item.get_name() for item in self.item_left_to_propose])
                            self.construct_support_arguments(attack_item)
                            self.send_message(Message(self.get_name(), message.get_exp(), MessagePerformative.PROPOSE, attack_item))
                        else:
                            self.send_message(Message(self.get_name(), message.get_exp(), MessagePerformative.ARGUE, attack))
                else:
                    counter_attack = self.counter_attack_argument(message.get_content())
                    if counter_attack == None: # no counter counter argument # we can't counter the counter argument, So we switch to another object. If we left an argument earlier (by counter proposing), we return (respond another way, else we fold and accept it) to it, else we propose the next one we have
                        if len(self.arguments_in_motion) > 0:
                            #print("RECONNECT ARGUE AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
                            old_argument = self.arguments_in_motion.pop()
                            _,old_item,_,_ = self.argument_parsing(old_argument)
                            #print("old argument", old_argument)
                            attack = self.attack_argument(old_argument)
                            if attack == None: # no counter argument # we can't counter the presented object, that mean we accept it
                                self.has_accepted = True
                                self.send_message(Message(self.get_name(), message.get_exp(), MessagePerformative.ACCEPT, old_item))
                            else:
                                _,attack_item,_,_ = self.argument_parsing(attack)
                                if attack_item != old_item:
                                    # we are counter proposing, need to put the argumentation on the current object on the argument still in motion list
                                    self.arguments_in_motion.append(old_argument)
                                    
                                    #print("after", [item.get_name() for item in self.item_left_to_propose])
                                    self.item_left_to_propose.remove(attack_item)
                                    #print("afterafter", [item.get_name() for item in self.item_left_to_propose])
                                    self.construct_support_arguments(attack_item)
                                    self.send_message(Message(self.get_name(), message.get_exp(), MessagePerformative.PROPOSE, attack_item))
                                else:
                                    #print(attack, [str(it) for it in self.item_left_to_propose])
                                    self.send_message(Message(self.get_name(), message.get_exp(), MessagePerformative.ARGUE, attack))
                        else: 
                            if len(self.item_left_to_propose) > 0:
                                self.send_proposal(message.get_exp())
                            else:
                                # technically we are out of items and all of them were rejected by one of the party, so we could say that no items were selected.
                                # Instead we just accept whatever item was in talk now
                                self.has_accepted = True
                                self.send_message(Message(self.get_name(), message.get_exp(), MessagePerformative.ACCEPT, item))
                    else:
                        self.send_message(Message(self.get_name(), message.get_exp(), MessagePerformative.ARGUE, counter_attack))

            elif message.get_performative() == MessagePerformative.ACCEPT:
                self.send_message(Message(self.get_name(), message.get_exp(), MessagePerformative.COMMIT, message.get_content()))
                self.choosen_item = message.get_content()
                self.has_commit = True
                
                
    def send_proposal(self, to_agent_name):
        favorite_item = self.preference.most_preferred(self.item_left_to_propose)
        self.item_left_to_propose.remove(favorite_item)
        self.construct_support_arguments(favorite_item)
        self.send_message(Message(self.get_name(), to_agent_name, MessagePerformative.PROPOSE,favorite_item))


    def get_preference(self):
        return self.preference

    def generate_preferences(self, item_list):
        pref = Preferences()
        crit_list = [crit_name for crit_name in CriterionName]
        random.shuffle(crit_list)
        pref.set_criterion_name_list(crit_list)
        for item in item_list:
            for crit_name in CriterionName:
                crit_val = random.choice(list(Value))
                pref.add_criterion_value(CriterionValue(item, crit_name, crit_val))
        self.preference = pref

    def print_preferences(self):
        preferences = self.get_preference()
        print(preferences.get_criterion_name_list())
        
        for crit in preferences.get_criterion_value_list():
            print(f"{crit.get_item()}, {crit.get_criterion_name()}, {crit.get_value()}")


    def list_supporting_proposal(self, item):
        """ Generate a list of premisses which can be used to support an item
        return : list of all premisses PRO an item ( sorted by order of importance based on agent 's preferences )
        """
        preference = self.get_preference()
        positive_premisses = []
        best_to_worst_criterion = preference.get_criterion_name_list()
        for i in range(len(best_to_worst_criterion)):
            criterion_name = best_to_worst_criterion[i]
            if preference.get_value(item, criterion_name) == Value.VERY_GOOD or preference.get_value(item, criterion_name) == Value.GOOD:
                argument = Argument(True, item)
                argument.add_premiss_couple_values(criterion_name, preference.get_value(item, criterion_name))
                positive_premisses.append(argument)
                for j in range(i+1, len(best_to_worst_criterion)):
                    worst_criterion_name = best_to_worst_criterion[j]
                    argument = Argument(True, item)
                    argument.add_premiss_couple_values(criterion_name, preference.get_value(item, criterion_name))
                    argument.add_premiss_comparison(criterion_name, worst_criterion_name)
                    positive_premisses.append(argument)
                # comparison
        return positive_premisses



    def list_attacking_proposal(self, item):
        """ Generate a list of premisses which can be used to attack an item
        return : list of all premisses CON an item ( sorted by order of importance based on preferences )
        """
        preference = self.get_preference()
        negative_premisses = []
        best_to_worst_criterion = preference.get_criterion_name_list()
        
        item_list = [item for item in self.item_left_to_propose]

        sorted_item_list = []
        while len(item_list) > 0:
            best = self.preference.most_preferred(item_list)
            item_list.remove(best)
            sorted_item_list.append(best)
        

        for i in range(len(best_to_worst_criterion)):
            criterion_name = best_to_worst_criterion[i]
            if preference.get_value(item, criterion_name) == Value.VERY_BAD or preference.get_value(item, criterion_name) == Value.BAD:
                # counter proposal
                for counter_item in sorted_item_list:
                    if preference.get_value(counter_item, criterion_name) == Value.VERY_GOOD or preference.get_value(counter_item, criterion_name) == Value.GOOD:
                        argument = Argument(True, counter_item)
                        argument.add_premiss_couple_values(criterion_name, preference.get_value(counter_item, criterion_name))
                        negative_premisses.append(argument)
                
                argument = Argument(False, item)
                argument.add_premiss_couple_values(criterion_name, preference.get_value(item, criterion_name))
                negative_premisses.append(argument)
                for j in range(i+1, len(best_to_worst_criterion)):
                    worst_criterion_name = best_to_worst_criterion[j]
                    argument = Argument(False, item)
                    argument.add_premiss_couple_values(criterion_name, preference.get_value(item, criterion_name))
                    argument.add_premiss_comparison(criterion_name, worst_criterion_name)
                    negative_premisses.append(argument)
                

        return negative_premisses

    def construct_support_arguments(self, item):
        self.pro_arguments[item.get_name()] = self.list_supporting_proposal(item)
    
    def construct_counter_arguments(self, item):
        self.con_arguments[item.get_name()] = self.list_attacking_proposal(item)
    
    def support_proposal(self, item):
        if len(self.pro_arguments[item.get_name()]) > 0:
            argument = self.pro_arguments[item.get_name()][0]
            _, item, _, _ = self.argument_parsing(self.pro_arguments[item.get_name()][0])
            self.remove_unusable_pro_arguments(item, self.pro_arguments[item.get_name()][0])
            return argument
        return None


    def argument_parsing(self, argument : Argument):
        if len(argument._couple_values_list) > 0:
            couple = argument._couple_values_list[0]
        else: 
            couple = None
        if len(argument._comparison_list) > 0:
            comparison = argument._comparison_list[0]
        else: 
            comparison = None
        
        return argument._decision, argument._item, couple, comparison

    def attack_argument(self, argument : Argument):
        decision, item, couple, comparison = self.argument_parsing(argument)
        c_i = couple._criterion_name
        #print(decision, item, [str(arg) for arg in self.con_arguments[item.get_name()]])
        if comparison == None:
            for attack in self.con_arguments[item.get_name()]:
                #print("consider attack", attack)
                counter_decision, counter_item, attack_couple, attack_comparison = self.argument_parsing(attack)
                
                if counter_item != item:
                    if counter_item in self.item_left_to_propose:
                        c_l = attack_couple._criterion_name
                        if c_l != c_i:
                            continue
                        
                        print("before",  [item.get_name() for item in self.item_left_to_propose])
                        # we can counter propose
                        self.remove_unusable_con_arguments(item, attack)
                        return attack
                    else:
                        continue
                if attack_comparison != None:
                    c_j, c_l = attack_comparison._best_criterion_name, attack_comparison._worst_criterion_name
                    if c_l != c_i:
                        continue
                    # attack on the weakness over a prefered criterion
                    self.remove_unusable_con_arguments(item, attack)
                    return attack
                else:
                    c_l = attack_couple._criterion_name
                    if c_l != c_i:
                        continue
                    # attack on the weakness over the current criterion
                    self.remove_unusable_con_arguments(item, attack)
                    return attack
        else:
            for attack in self.con_arguments[item.get_name()]:
                #print("consider attack", attack)
                counter_decision, counter_item, attack_couple, attack_comparison = self.argument_parsing(attack)
                if counter_item != item:
                    if counter_item in self.item_left_to_propose:
                        c_l = attack_couple._criterion_name
                        if c_l != c_i:
                            continue
                        
                        print("before",  [item.get_name() for item in self.item_left_to_propose])
                        # we can counter propose
                        self.remove_unusable_con_arguments(item, attack)
                        return attack
                    else:
                        continue
                if attack_comparison != None:
                    c_j, c_l = attack_comparison._best_criterion_name, attack_comparison._worst_criterion_name
                    if c_l != c_i:
                        continue
                    # can attack on the weakness of a prefered criterion
                    #self.con_arguments[item.get_name()].remove(attack)
                    self.remove_unusable_con_arguments(item, attack)
                    return attack
        return None

    def counter_attack_argument(self, counter_argument : Argument):
        decision, item, couple, comparison = self.argument_parsing(counter_argument)
        c_i = couple._criterion_name
        
        if comparison == None:
            # since this agent always pick from the top most to down criterion (according to its own order), we have no way to construct a counter argument at this stage
            # So instead we try to promote another criterion. Thankfully by construction it should the topmost of our list of pro arguments about the item
            return self.support_proposal(item)
        else:
            for counter_attack in self.pro_arguments[item.get_name()]:
                _, _, attack_couple, attack_comparison = self.argument_parsing(counter_attack)
                if attack_comparison != None:
                    c_j, c_l = attack_comparison._best_criterion_name, attack_comparison._worst_criterion_name
                    if c_l != c_i:
                        continue
                    # can attack on the strength of a prefered criterion
                    self.remove_unusable_pro_arguments(item, counter_attack)
                    #self.pro_arguments[item.get_name()].remove(counter_attack)
                    return counter_attack
        return None
        
    def remove_unusable_pro_arguments(self, item, argument):
        """we remove all the arguments that we can no longer use to defend/attack. 
           we remove all the arguments that use the same criterion"""
        to_remove = []
        decision, item, couple, comparison = self.argument_parsing(argument)
        criterion_name = couple._criterion_name
        for arg_id in range(len(self.pro_arguments[item.get_name()])):
            _, _, couple2, _ = self.argument_parsing(self.pro_arguments[item.get_name()][arg_id])
            if criterion_name == couple2._criterion_name:
                to_remove.append(arg_id)
        
        self.pro_arguments[item.get_name()] = [self.pro_arguments[item.get_name()][arg_id] for arg_id in range(len(self.pro_arguments[item.get_name()])) if arg_id not in to_remove]

    def remove_unusable_con_arguments(self, item, argument):
        """we remove all the arguments that we can no longer use to defend/attack. 
           we remove all the arguments that use the same criterion"""
        to_remove = []
        decision, arg_item, couple, comparison = self.argument_parsing(argument)
        if arg_item == item: 
            criterion_name = couple._criterion_name
            for arg_id in range(len(self.con_arguments[item.get_name()])):
                _, _, couple2, _ = self.argument_parsing(self.con_arguments[item.get_name()][arg_id])
                if criterion_name == couple2._criterion_name:
                    to_remove.append(arg_id)
            self.con_arguments[item.get_name()] = [self.con_arguments[item.get_name()][arg_id] for arg_id in range(len(self.con_arguments[item.get_name()])) if arg_id not in to_remove]
        else:

            for arg_id in range(len(self.con_arguments[item.get_name()])):
                decision, other_item, couple2, _ = self.argument_parsing(self.con_arguments[item.get_name()][arg_id])
                if other_item == arg_item:
                    to_remove.append(arg_id)
            self.con_arguments[item.get_name()] = [self.con_arguments[item.get_name()][arg_id] for arg_id in range(len(self.con_arguments[item.get_name()])) if arg_id not in to_remove]
        

            

class ArgumentModel(Model):
    """ ArgumentModel which inherit from Model .
    """
    def __init__(self, item_list, n_agent):
        super().__init__()
        self.schedule = RandomActivation(self)
        self.__messages_service = MessageService(self.schedule)
        self.item_list = item_list
        self.n_agent = n_agent
        for a in range(n_agent):
            agent = ArgumentAgent(self.next_id(), self, "A" + str(a+1))
            agent.generate_preferences(item_list=item_list)
            self.schedule.add(agent)
            #agent.print_preferences()
        

        self.running = True

    def step(self):
        self.__messages_service.dispatch_messages()
        self.schedule.step()


    def make_duel(self, agent_1, agent_2):
        step = 0

        agent_1.has_commit = False
        agent_2.has_commit = False
        agent_1.item_left_to_propose = [item for item in self.item_list]
        agent_2.item_left_to_propose = [item for item in self.item_list]
        agent_1.arguments_in_motion = []
        agent_2.arguments_in_motion = []
        agent_1.pro_arguments = dict()
        agent_1.con_arguments = dict()
        agent_2.pro_arguments = dict()
        agent_2.con_arguments = dict()
        agent_1.has_accepted = False
        agent_2.has_accepted = False
        if random.random() < 0.5: #randomly pick who starts the argument    
            agent_1.send_proposal(agent_2.get_name())
        else:
            agent_2.send_proposal(agent_1.get_name())

        

        while not agent_1.has_commit or not agent_2.has_commit:
            self.step()
            step+=1

            if step == 100:
                print("step_break",agent_1.get_name(), agent_2.get_name())
                break
        self.step()
        step += 1

        if agent_1.has_accepted:
            agent_1_winner = True
        elif agent_2.has_accepted:
            agent_1_winner = False
                
        return agent_1_winner, agent_1.choosen_item
        

    def do_all_duels(self):
        number_of_wins = [0]*self.n_agent
        choosen_items = []
        for i in range(self.n_agent):
            for j in range(i+1, self.n_agent):
                print(self.schedule.agents[i].get_name(), "vs",self.schedule.agents[j].get_name() )
                first_agent_win, choosen_item = self.make_duel(self.schedule.agents[i], self.schedule.agents[j])
                choosen_items.append(str(choosen_item))
                if first_agent_win:
                    number_of_wins[i]+=1
                else:
                    number_of_wins[j]+=1
                print()

        print(number_of_wins)
        print(choosen_items)



if __name__ == "__main__":
    items = []
    items.append(Item("Diesel Engine", "A super cool diesel engine"))
    items.append(Item("Electric Engine", "A very quiet engine"))
    items.append(Item("Nitrous Oxide", "I don't know what this is"))
    items.append(Item("Hydrogen Engine", "Only produce water waste"))

    n_agent = 3
    
    argument_model = ArgumentModel(items, n_agent)


    argument_model.do_all_duels()
