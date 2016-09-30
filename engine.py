#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import jsonschema


class Engine:
    def __init__(self, input):
        self.model_file = "model/struct.json"
        self.__afn = input

    def read_schema(self):
        with open(self.model_file) as data_file:
            return json.load(data_file)

    def check_syntax(self):
        try:
            jsonschema.Draft4Validator(self.read_schema()).validate(self.__afn)
            return True
        except jsonschema.exceptions.ValidationError as error:
            return error.message.replace("u'", "'")
