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
            i["x"] = int(float(i["x"]))
            i["y"] = int(float(i["y"]))

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

    def __create_afd_by_afn(self):
        self.load_base_struct()
        self.__get_az_states()

        print self.states
        # print self.initial_state
        # print self.final_state

    def convert(self):
        if isinstance(self.entry, dict) is not True:
            self.entry = json.loads(self.entry)

        if self.check_syntax(self.entry) is not True:
            print self.alerts()
        else:
            self.__create_afd_by_afn()


