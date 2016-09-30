#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import jsonschema


class Engine:
    def __init__(self, input):
        self.model_file = "models/json/struct.json"
        self.__message = None
        self.__afn = input

    def alerts(self):
        return self.__message

    def read_schema(self):
        try:
            with open(self.model_file, "r") as data_file:
                return json.load(data_file)
        except IOError as error:
            self.__message = "Erro ler modelo de I/O!"
            return None

    def check_syntax(self):
        try:
            jsonschema.Draft4Validator(self.read_schema()).validate(self.__afn)
            return True
        except jsonschema.exceptions.ValidationError as error:
            self.message = error.message.replace("u'", "'")
        except AttributeError:
            self.__message = "Erro ao definir estrutura dos autômatos para validação!"
        return False

    def main(self):
        pass


