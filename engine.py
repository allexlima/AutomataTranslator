#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Importa as bibliotecas básicas para o funcionamento da tradução

import json
import xml
import xmltodict
import jsonschema


# Classe Model é responsável por validar o Input/Output, i.e., a estrutura do autômato
class Model(object):
    def __init__(self):
        self.model_file = "models/json/struct.json"
        self.entry = None
        self.output = None
        self.states = None
        self.transitions = None
        self.__message = None

    # Método para retornar mensagens de erro
    def alerts(self):
        return self.__message

    # Método para criar mensagens de erro
    def create_alert(self, msg):
        self.__message = str(msg)

    # Método responsável por ler o arquivo de regras de estruturação do Autômato (i.e. o padrão de I/O)
    def read_schema(self):
        try:
            with open(self.model_file, "r") as data_file:
                return json.load(data_file)
        except IOError:
            self.create_alert("Erro ler modelo de I/O!")
            return None

    # Método para verificar a síntaxe do Input, conforme as regras de estruturações presentes no
    # arquivo ´models/json/struct.json´
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

    # Carrega a estrutura do Input para os atributos da classe
    def load_base_struct(self):
        self.states = self.entry["structure"]["automaton"]["state"]
        self.transitions = self.entry["structure"]["automaton"]["transition"]

    # Ordena os estados pela propriedade ´id´ e as transições pela propriedade ´from´
    def sort_object(self):
        self.states = sorted(self.states, key=lambda x: int(x["@id"]))
        self.transitions = sorted(self.transitions, key=lambda x: int(x["from"]))


# Jflap é a classe responsável por realizar a Importação e Exportação de arquivos no formato JFLAP#
# Obs.: Ela herda propriedades da classe ´Model´
class Jflap(Model):
    def __init__(self):
        super(Jflap, self).__init__()

    # Método responsável por remover algumas propriedades inúteis para a tradução presente na estrutura
    # do arquivo JFLAP, além de consertar o tipo das propriedades de interesse
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

    # Método responsável por realizar a conversão, através da biblioteca ´xmltodict´, de um modelo
    # JFLAP para json (método utilizado no processo de importação)
    def jff2json(self):
        try:
            self.entry = json.loads(json.dumps(xmltodict.parse(self.entry)))
            self.load_base_struct()
            self.__fix_values_types()
            self.sort_object()
        except xml.parsers.expat.ExpatError as error:
            self.create_alert("Impossível realizar conversão do arquivo .jff!\n" + error.message)

    # Método reponsável por características importantes para a execução do modelo gerado
    # no JFLAP (método utilizado no processo d exportação)
    @staticmethod
    def prepare_layout_jff(content):
        try:
            if not content["type"]:
                content.update({u"type": u"fa"})
        except KeyError:
            pass
        return content

    # Método responsável por realizar a conversão de um arquivo de entrada (json ou dict)
    # para o formato JFLAP compatível
    def make_jff(self, content):
        temp = json.loads(content)
        temp = self.prepare_layout_jff(temp)
        return xmltodict.unparse(temp, pretty=True)

# Classe principal no processo de tradução AFN -> AFD
# herda propriedades da classe ´Jflap´ que, por sua vez, herda da classe ´Model´
# Ou seja, a classe ´Translator´ tem acesso a todos os métodos e atributos não privados das classes anteriores
class Translator(Jflap):
    def __init__(self, entry):
        super(Translator, self).__init__()
        self.entry = entry
        self.initial_state = None
        self.final_state = []
        self.new_transitions = []

    # Método responsável identificar e listar o alfabeto utilizado pelo autômato de entrada
    def __get_alphabet(self):
        alphabet = [str(item["read"]) for item in self.transitions]
        return sorted(list(set(alphabet)))

    # Método responsável por identificar os estados iniciais e finais, bem como
    # realizar a ordenação dos mesmos
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

    # Método responsável por último estado criado
    def __get_last_state_id(self):
        return self.states[-1]["@id"]

    # Método responsável por retornar todas as propriedades de dado estado
    def __get_state(self, state_id):
        return [item for item in self.states if item["@id"] == state_id][0]

    # Método responsável por listar todas as transições ´de um determinado estado´ lendo ´determinado símbolo´
    # das transições do AFD a ser gerado
    def __get_transitions(self, from_id, reading):
        return [item["to"] for item in self.new_transitions if item["from"] == from_id and item["read"] == reading]

    # Método responsável por listar todas as transições ´de um determinado estado´ lendo ´determinado símbolo´
    # das transições do AFN de entrada
    def __get_transitions_afn(self, from_id, reading):
        return [item["to"] for item in self.transitions if item["from"] == from_id and item["read"] == reading]

    # Método responsável apagar uma determinada transição de um ´determinado estado´ lendo ´determinado símbolo´
    def __pop_transition_from(self, state_id, reading):
        state_transitions = [item for item in self.new_transitions if item["from"] == state_id and item["read"] == reading]
        for i in state_transitions:
            self.new_transitions.remove(i)

    # Verifica se ´determinado estado´ é um estado inicial (boolean)
    def __is_initial_state(self, state_id):
            return True if self.initial_state["@id"] is state_id else False

    # Verifica se ´determinado estado´ é um estado final (boolean)
    def __is_final_state(self, states_id):
        for item in self.final_state:
            for state in states_id:
                if item["@id"] == state:
                    return True
        return False

    # Retorna um nome para um novo estado
    # esse nome segue o padrão: q + id_do_estado (e.g. q0, q1, q0q1 etc)
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

    # Cria uma nova transição ´de um determinado estado´ para outro ´determinado estado´ lendo ´um símbolo´
    def __new_transition(self, from_id, to_id, reading):
        transition = {}
        transition.update({u"from": from_id})
        transition.update({u"to": to_id})
        transition.update({u"read": reading})
        self.new_transitions.append(transition)

    # Cria um novo estado
    def __new_state(self, is_initial, is_final, name=None):
        this_id = self.__get_last_state_id() + 1
        state = {}
        state.update({u"@id": this_id})
        state.update({u"@name": self.__set_name_tuple(name, n_id=this_id)})
        state.update({u"initial": True}) if is_initial is True else None
        state.update({u"final": True}) if is_final is True else None
        self.states.append(state)
        return this_id

    # Realiza a união de todas as transições de um ´determinado conjunto de estados´ lendo ´um símbolo´
    # e verifica se essa união dá origem a um novo estado ou a um estado já existente
    def __get_transitions_union(self, transitions, symbol, new_state):
        new_state_transitions = []
        for i in transitions:
            new_state_transitions.append(self.__get_transitions_afn(i, symbol))
        new_state_transitions = list(set([item for sublist in new_state_transitions for item in sublist]))
        if new_state_transitions == transitions:
            return [new_state]
        else:
            return new_state_transitions

    # Função principal para a criação do afn
    def __create_afd_by_afn(self):
        self.load_base_struct()
        self.__get_az_states()
        # Faz um backup das transições presentes no AFN para ter como base para as novas do AFD
        self.new_transitions += self.transitions
        # Dicionário de referência: ´conjunto de transições´ vão para ´este novo estado´
        transictions_dict = {}

        # Para casa estado faça
        for state in self.states:
            # Lendo cada símbolo desse estado faça
            for symbol in self.__get_alphabet():
                # Lista as transições que esse estado tem lendo o símbolo atual (AFD)
                actual_transitions = list(set(self.__get_transitions(state["@id"], symbol)))
                # Lista as transições que esse estado tem lendo o símbolo atual (AFN) (novo)
                actual_transitions_afn = list(set(self.__get_transitions_afn(state["@id"], symbol)))
                # Caso esse estado atual possua mais de uma transição (não determístico), faça...
                if len(actual_transitions) > 1:
                    # Crie um novo estado
                    new_state = self.__new_state(
                        False,
                        self.__is_final_state(actual_transitions_afn),
                        name=actual_transitions_afn
                    )
                    # Salve a refêrencia de transição
                    transictions_dict.update({
                        str(actual_transitions): new_state
                    })
                    # Apague as transições velhas
                    self.__pop_transition_from(state["@id"], symbol)
                    # Crie uma transição do estado atual para o novo estado criado
                    self.__new_transition(state["@id"], new_state, symbol)

                    # Configuração das transições para cada símbolo do novo estado
                    # Para cada símbolo do alfabeto, lendo-se para o novo estado, faça...
                    for symbol_b in self.__get_alphabet():
                        # obtêm a união das transições do estado atual lendo este símbolo da iteração
                        new_transitions = self.__get_transitions_union(actual_transitions, symbol_b, new_state)

                        # caso o símbolo dessa iteração seja o mesmo da principal, i.e
                        # o novo estado receberá a união das transições do estado que o gerou
                        if symbol_b == symbol:
                            for node in new_transitions:
                                self.__new_transition(new_state, node, symbol)
                        else:
                            for node in new_transitions:
                                # se o número de novas transições for maior que 1, i.e,
                                # o estado não recebe uma transição para ele mesmo, então
                                if len(new_transitions) > 1:
                                    try:
                                        # cria-se uma transição do novo estado para uma transição referênciada no dicionário de referências de transições
                                        self.__new_transition(new_state, transictions_dict[str(new_transitions)], symbol_b)
                                    except KeyError as error:
                                        # Caso a referência não exista
                                        self.create_alert(
                                            "Erro ao adicionar novas transições! \n\n" +
                                            json.dumps(transictions_dict, sort_keys=True, indent=4, separators=(',', ': ')) +
                                            "\n\nnew_transitions=" + str(new_transitions) +
                                            "\n\nKeyError not found: " + error.message
                                        )
                                    break
                                else:
                                    self.__new_transition(new_state, node, symbol_b)

    # função main para verificação da estrutura e encaminhamento para a conversão
    def convert(self):
        # verifica se o autômato de entrada está em condições sintáticas de ser traduzido
        if isinstance(self.entry, dict) is not True:
            try:
                self.entry = json.loads(self.entry)
            except ValueError as error:
                self.create_alert(error)
        # se estier tudo ok, ele começa o processo de tradução
        if self.check_syntax(self.entry):
            self.__create_afd_by_afn()

    # Método responsável por montar uma tabela de transição mais 'visual' para o usuário
    def show_automaton(self):
        output = "\n"
        for state in self.states:
            for symbol in self.__get_alphabet():
                output += "q{0} * {1} → {2}\n".format(state["@id"], symbol, ['q'+str(i) for i in self.__get_transitions(state["@id"], symbol)]).replace("u'", "'").replace("['", "").replace("']", "").replace("'", "").replace("'", "").replace("[]", "λ")
        return output
