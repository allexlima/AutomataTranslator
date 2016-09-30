#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import jsonschema



class Model(object):
    def __init__(self, entry):
        self.model_file = "models/json/struct.json"
        self.entry = entry
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

    def check_syntax(self):
        try:
            jsonschema.Draft4Validator(self.read_schema()).validate(self.entry)
            return True
        except jsonschema.exceptions.ValidationError as error:
            self.create_alert(
                "Erro de sintaxe: " +
                error.message.replace("u'", "'") +
                "\nPor favor, revise seu autômato conforme as definições dispostas na Documentação."
            )
        except AttributeError:
            self.create_alert("Erro ao definir estrutura dos autômatos para validação!")
        return False


class Translator(Model):
    def __init__(self, entry):
        super(Translator, self).__init__(entry)

    def __create_afd_by_afn(self):
        pass

    def convert(self):
        if self.check_syntax() is not True:
            print self.alerts()
        else:
            self.__create_afd_by_afn()
