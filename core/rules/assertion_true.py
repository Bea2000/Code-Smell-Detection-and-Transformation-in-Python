from _ast import Assign
from typing import Any
from ..rule import *
import ast

class AssertionTrueVisitor(WarningNodeVisitor):
    #  Implementar Clase
    def __init__(self):
        super().__init__()
        self.vars = {}
    
    def visit_Assign(self, node: Assign):
        for target in node.targets:
            if isinstance(target,Name):
                if isinstance(node.value,Constant):
                    self.vars[target.id] = node.value.value
        NodeVisitor.generic_visit(self, node)
        
    def visit_Call(self, node: Call):
        if isinstance(node.func, Attribute) and node.func.attr == 'assertTrue':
            for arg in node.args:
                if isinstance(arg,Constant):
                    if arg.value == True:
                        self.addWarning('AssertTrueWarning', node.func.lineno, 'useless assert true detected')
                if isinstance(arg,Name):
                    if arg.id in self.vars:
                        if self.vars[arg.id] == True:
                            self.addWarning('AssertTrueWarning', node.func.lineno, 'useless assert true detected')
        NodeVisitor.generic_visit(self, node)
    
    
    
    

class AssertionTrueTestRule(Rule):
    #  Implementar Clase
    def analyze(self, node):
        visitor = AssertionTrueVisitor()
        visitor.visit(node)
        return visitor.warningsList()
        
    @classmethod
    def name(cls):
        return 'assertion-true'
