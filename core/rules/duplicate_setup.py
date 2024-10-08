import ast
from ..rule import *


class DuplicatedSetupVisitor(WarningNodeVisitor):
    #  Implementar Clase
    def __init__(self):
        super().__init__()
        self.count = 0
        self.code = []

    # Guardamos el código de cada función en una lista
    def visit_FunctionDef(self, node):
        self.code.append(node.body)

    def reorganize_code_list(self):
        # Reorganiza la lista para que en la primera lista, queden todas las primeras lineas de código, en la segunda lista, todas las segundas lineas de código, etc
        # esto hace que sea más fácil de comparar
        new_list = []
        for i in range(len(self.code[0])):  # recorre la cantidad de líneas que hayan en la primera función (la que manda)
            temporary_list = []
            for j in range(len(self.code)): # iteramos en las distintas funciones
                try:
                    temporary_list.append(self.code[j][i])
                except:
                    pass
            new_list.append(temporary_list)        

        # actualizamos self.code 
        self.code = new_list        

    def get_count_duplicated(self):      
        self.reorganize_code_list()
        for line in self.code:    # iterar en cada línea del código
            firstcodeline = ast.dump(ast.parse(line[0]))
            if all(ast.dump(ast.parse(codeline)) == firstcodeline for codeline in line):
                self.count += 1
            else:
                break
        
        if self.count >= 1:
            self.addWarning('DuplicatedSetup', self.count, f"there are {self.count} duplicated setup statements")
    

class DuplicatedSetupRule(Rule):
    #  Implementar Clase    
    def analyze(self, node):
        visitor = DuplicatedSetupVisitor()
        visitor.visit(node)
        visitor.get_count_duplicated()
        return visitor.warningsList()

    @classmethod
    def name(cls):
        return 'duplicate-setup'
