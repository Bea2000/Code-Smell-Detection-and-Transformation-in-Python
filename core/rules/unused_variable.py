from _ast import FunctionDef
from ..rule import *
import ast

class UnusedVariableVisitor(WarningNodeVisitor):
    #  Implementar Clase
    def __init__(self):
        super().__init__()
        self.vars = {}
    
    def visit_FunctionDef(self, node: FunctionDef):
        for i in range(0,len(node.body)):
            expr = node.body[i]
            match expr:
                case Assign(targets=[Name(id=x, ctx=Store())], value=Constant(value=y)):
                    self.vars[x] = node.body[i].lineno
            match expr:
                case Assign(targets=[Name(id=x, ctx=Store())], value=BinOp(left=y, op=operation, right=z)):
                    if isinstance(y,Name):
                        if y.id in self.vars:
                            del self.vars[y.id]
                    if isinstance(z,Name):
                        if z.id in self.vars:
                            del self.vars[z.id]
                    self.vars[x] = node.body[i].lineno
            if isinstance(expr.value, Call):
                for arg in expr.value.args:
                    if isinstance(arg, Name):
                        if arg.id in self.vars:
                            del self.vars[arg.id]
        for var in self.vars:
            self.addWarning('UnusedVariable', self.vars[var], 'variable '+var+' has not been used')
        NodeVisitor.generic_visit(self, node)
        
class UnusedVariableTestRule(Rule):
    #  Implementar Clase
    def analyze(self, node):
        visitor = UnusedVariableVisitor()
        visitor.visit(node)
        print(ast.dump(node,indent=3))
        return visitor.warningsList()
        
    @classmethod
    def name(cls):
        return 'not-used-variable'
