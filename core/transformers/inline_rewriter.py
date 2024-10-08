from _ast import FunctionDef
from ast import *
from typing import Any
from core.rewriter import RewriterCommand


class InlineTransformer(NodeTransformer):
    def __init__(self):
        super().__init__()
        self.var = {}
        self.newArgs = []
        self.addedArg = False
            
    def visit_FunctionDef(self, node: FunctionDef):
        newNode = NodeTransformer.generic_visit(self,node)
        newAssign = []
        newExpr = []
        for b in newNode.body:
            # seteamos assign
            if isinstance(b, Assign):
                for t in b.targets:
                    if isinstance(t, Name):
                        self.var[t.id] = [0,b]
            elif isinstance(b, Expr):
                if isinstance(b.value, Call):
                    for arg in b.value.args:
                        if isinstance(arg, Name):
                            if arg.id in self.var:
                                if self.var[arg.id][0] == 0:
                                    self.var[arg.id][0] += 1
                                    value = self.var[arg.id][1].value
                                    # revisamos si cambiar o no valores de binop
                                    if isinstance(value, BinOp):
                                        self.countBinOpLeft(value.left)
                                        self.countBinOpRight(value.right)
                                        value.left = self.searchBinOpLeft(value.left)
                                        value.right = self.searchBinOpRight(value.right)
                                    self.newArgs.append(value)
                                    self.addedArg = True
                        if not self.addedArg:
                            self.newArgs.append(arg)
                        self.addedArg = False
                    b.value.args = self.newArgs
                newExpr.append(b)
        for var in self.var:
            if self.var[var][0] > 1:
                newAssign.append(self.var[var][1])
        newBody = newAssign + newExpr
        newNode.body = newBody
        return newNode
    
    def countBinOpLeft(self, value):
        newValue = value
        if isinstance(value, Name):
            if value.id in self.var:
                self.var[value.id][0] += 1
            newValue = self.var[value.id][1].value
            if isinstance(newValue, BinOp):
                self.countBinOpLeft(newValue.left)
                self.countBinOpRight(newValue.right)
            
    def countBinOpRight(self, value):
        newValue = value
        if isinstance(value, Name):
            if value.id in self.var:
                self.var[value.id][0] += 1
            newValue = self.var[value.id][1].value
            if isinstance(newValue, BinOp):
                self.countBinOpLeft(newValue.left)
                self.countBinOpRight(newValue.right)

    def searchBinOpLeft(self, value):
        newValue = value
        if isinstance(value, Name):
            newValue = self.var[value.id][1].value
            if isinstance(newValue, BinOp):
                newValue.left = self.searchBinOpLeft(newValue.left)
                newValue.right = self.searchBinOpRight(newValue.right)
        if isinstance(value, Name):
            if self.var[value.id][0] == 1:
                return newValue
        return value
            
    def searchBinOpRight(self, value):
        newValue = value
        if isinstance(value, Name):
            newValue = self.var[value.id][1].value
            if isinstance(newValue, BinOp):
                newValue.left = self.searchBinOpLeft(newValue.left)
                newValue.right = self.searchBinOpRight(newValue.right)
        if isinstance(value, Name):
            if self.var[value.id][0] == 1:
                return newValue
        return value

class InlineCommand(RewriterCommand):
    # Implementar comando, recuerde que puede necesitar implementar además clases NodeTransformer y/o NodeVisitor.
    def apply(self, node):
        new_tree = fix_missing_locations(InlineTransformer().visit(node))
        return new_tree
