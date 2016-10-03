#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import xml
import xmltodict
import jsonschema


class Model(object):
    def __init__(self):
        self.model_file = "models/json/struct.json"
        self.entry = None
        self.output = None
        self.states = None
        self.transitions = None
        self.__message = None

    def alerts(self):
        return self.__message

    def create_alert(self, msg):
        self.__message = str(msg)

    def read_schema(self):
        try:
            with open(self.model_file, "r") as data_file:
                return json.load(data_file)
        except IOError:
            self.create_alert("Erro ler modelo de I/O!")
            return None

    def check_syntax(self, automaton):
        try:
            jsonschema.Draft4Validator(self.read_schema()).validate(automaton)
            return True
        except jsonschema.exceptions.ValidationError as error:
            self.create_alert(
                "Erro de sintaxe: " +
                error.message.replace("u'", "'") +
                "\nPor favor, revise seu autômato conforme as definições dispostas na Documentação."
            )

        return False

    def load_base_struct(self):
        self.states = self.entry["structure"]["automaton"]["state"]
        self.transitions = self.entry["structure"]["automaton"]["transition"]

    def sort_object(self):
        self.states = sorted(self.states, key=lambda x: int(x["@id"]))
        self.transitions = sorted(self.transitions, key=lambda x: int(x["from"]))


class Jflap(Model):
    def __init__(self):
        super(Jflap, self).__init__()

    def __fix_values_types(self):
        for i in self.states:
            i["@id"] = int(i["@id"])
            i.pop("x")
            i.pop("y")
            try:
                i["initial"] = True if i["initial"] is None else True
            except KeyError:
                pass
            try:
                i["final"] = True if i["final"] is None else True
            except KeyError:
                pass
            try:
                i.pop("label")
            except KeyError:
                pass

        for i in self.transitions:
            i["from"] = int(i["from"])
            i["to"] = int(i["to"])

    def jff2json(self):
        try:
            self.entry = json.loads(json.dumps(xmltodict.parse(self.entry)))
            self.load_base_struct()
            self.__fix_values_types()
            self.sort_object()
        except xml.parsers.expat.ExpatError as error:
            self.create_alert("Impossível realizar conversão do arquivo .jff!\n" + error.message)
            print self.alerts()

    def make_jff(self):
        if self.check_syntax(self.output) is not True:
            print self.alerts()
        else:
            xmltodict.unparse(self.output, pretty=True)


class Translator(Jflap):
    def __init__(self, entry):
        super(Translator, self).__init__()
        self.entry = entry
        self.initial_state = None
        self.final_state = []

    def __get_alphabet(self):
        alphabet = [str(item["read"]) for item in self.transitions]
        return sorted(list(set(alphabet)))

    def __get_az_states(self):
        for i in self.states:
            try:
                if i["initial"] is None or True:
                    self.initial_state = i
            except KeyError:
                pass

            try:
                if i["final"] is None or True:
                    self.final_state.append(i)
            except KeyError:
                pass

        self.final_state = sorted(self.final_state, key=lambda x: int(x["@id"]))

    def __get_last_state_id(self):
        return self.states[-1]["@id"]

    def __get_state(self, state_id):
        return [item for item in self.states if item["@id"] == state_id][0]

    def __get_transitions(self, from_id, reading):
        return [item["to"] for item in self.transitions if item["from"] == from_id and item["read"] == reading]

    def __pop_states(self, state_id):
        if isinstance(state_id, list):
            self.states = [item for item in self.states if item["@id"] in state_id]
        else:
            self.states = [item for item in self.states if item["@id"] is state_id]

    def __pop_transitions(self, to_id, reading):
        if isinstance(to_id, list):
            self.transitions = [item for item in self.transitions if item["to"] in to_id and item["read"] != reading]
        else:
            self.transitions = [item for item in self.transitions if item["to"] is to_id and item["read"] != reading]

    def __is_initial_state(self, state_id):
            return True if self.initial_state["@id"] is state_id else False

    def __is_final_state(self, states_id):
        for item in self.final_state:
            for state in states_id:
                if item["@id"] == state:
                    return True
        return False

    @staticmethod
    def __set_name_tuple(symbols, n_id=None):
        name = ""
        if isinstance(symbols, list):
            for i in symbols:
                name += "q"+str(i)
            return name
        else:
            name = "q" + str(n_id)
        return name

    def __new_transition(self, from_id, to_id, reading):
        transition = {}
        transition.update({u"from": from_id})
        transition.update({u"to": to_id})
        transition.update({u"read": reading})
        self.transitions.append(transition)

    def __new_state(self, is_initial, is_final, name=None):
        this_id = self.__get_last_state_id() + 1
        state = {}
        state.update({u"@id": this_id})
        state.update({u"@name": self.__set_name_tuple(name, n_id=this_id)})
        state.update({u"initial": True}) if is_initial is True else None
        state.update({u"final": True}) if is_final is True else None
        self.states.append(state)
        return this_id

    def __show_automaton(self):
        for state in self.states:
            for symbol in self.__get_alphabet():
                print "q{0}*{1} = {2}".format(state["@id"], symbol, self.__get_transitions(state["@id"], symbol))

    def __new_connection(self, state_id, transitions):
        for symbol in self.__get_alphabet():
            '''
                    for id_s in to_states:
                        transitions = self.__get_transitions(id_s, symbol)
                        if transitions == to_states:
                            new_transitions.append(new_state)
                        else:
                            new_transitions += [item for item in transitions]

                    self.__pop_transitions(to_states, symbol)

                    for i in new_transitions:
                        self.__new_transition(new_state, i, symbol)
            '''
            print "q{0}*{1} = {2}".format(state_id, symbol, self.__get_transitions(state_id, symbol))

    def __create_afd_by_afn(self):
        self.load_base_struct()
        self.__get_az_states()

        for state in self.states:
            for symbol in self.__get_alphabet():
                transitions = self.__get_transitions(state["@id"], symbol)

                if len(transitions) > 1:
                    new_state = self.__new_state(False, self.__is_final_state(transitions), name=transitions)
                    self.__pop_transitions(state["@id"], symbol)
                    self.__new_transition(state["@id"], new_state, symbol)
                    self.__new_connection(new_state, transitions)
                    continue

        print "\n"
        self.__show_automaton()

    def convert(self):
        if isinstance(self.entry, dict) is not True:
            self.entry = json.loads(self.entry)

        if self.check_syntax(self.entry) is not True:
            print self.alerts()
        else:
            self.__create_afd_by_afn()
