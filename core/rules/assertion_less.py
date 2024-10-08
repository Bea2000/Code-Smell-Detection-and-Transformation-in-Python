from _ast import FunctionDef
from typing import Any
from ..rule import *
import ast


class AssertionLessVisitor(WarningNodeVisitor):
    # Implementar Clase
    def __init__(self):
        super().__init__()
        self.counter = 0

    def visit_FunctionDef(self, node: FunctionDef):
        for expr in node.body:
            match expr:
                case Expr(value=Call(
                        func=Attribute(value=Name(id='self', ctx=Load()), attr=x, ctx=Load()),)):
                    if 'assert' in x:
                        self.counter += 1
        if self.counter == 0:
            self.addWarning('AssertionLessWarning', node.lineno, 'it is an assertion less test')
        NodeVisitor.generic_visit(self, node)
        
class AssertionLessTestRule(Rule):
    #  Implementar Clase
    def analyze(self, node):
        visitor = AssertionLessVisitor()
        visitor.visit(node)
        print(ast.dump(node,indent=3))
        return visitor.warningsList()

        
    @classmethod
    def name(cls):
        return 'assertion-less'
