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

    def prepare_layout_jff(self, content):
        try:
            if not content["type"]:
                content.update({u"type": u"fa"})
        except KeyError:
            pass
        return content

    def make_jff(self, content):
        temp = json.loads(content)
        temp = self.prepare_layout_jff(temp)
        return xmltodict.unparse(temp, pretty=True)


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

    def __pop_transitions(self, state_id, reading):
        state_transitions = [item for item in self.transitions if item["from"] == state_id and item["read"] == reading]
        for i in state_transitions:
            self.transitions.remove(i)

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

    def show_automaton(self):
        output = "\n"
        for state in self.states:
            for symbol in self.__get_alphabet():
                output += "q{0} * {1} → {2}\n".format(state["@id"], symbol, ['q'+str(i) for i in self.__get_transitions(state["@id"], symbol)]).replace("u'", "'").replace("['", "").replace("']", "").replace("'", "").replace("'", "").replace("[]", "λ")
        return output

    def __get_new_transitions(self, transitions, symbol, new_state):
        new_state_transitions = []
        for i in transitions:
            new_state_transitions.append(self.__get_transitions(i, symbol))
        new_state_transitions = [item for sublist in new_state_transitions for item in sublist]
        if new_state_transitions == transitions:
            return [new_state]
        else:
            return new_state_transitions

    def __create_afd_by_afn(self):
        self.load_base_struct()
        self.__get_az_states()

        for state in self.states:
            for symbol in self.__get_alphabet():
                actual_transitions = self.__get_transitions(state["@id"], symbol)
                if len(actual_transitions) > 1:
                    new_state = self.__new_state(False, self.__is_final_state(actual_transitions), name=actual_transitions)
                    new_transitions = self.__get_new_transitions(actual_transitions, symbol, new_state)

                    for symbol_b in self.__get_alphabet():
                        if symbol_b == symbol:
                            for node in new_transitions:
                                self.__new_transition(new_state, node, symbol)

    def convert(self):
        if isinstance(self.entry, dict) is not True:
            try:
                self.entry = json.loads(self.entry)
            except ValueError as error:
                self.create_alert(error)

        if self.check_syntax(self.entry):
            self.__create_afd_by_afn()
