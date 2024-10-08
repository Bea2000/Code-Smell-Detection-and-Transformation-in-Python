from ast import *
import ast
from core.rewriter import RewriterCommand

class AssertTrueTransformer(NodeTransformer):

    def visit_Call(self, node):     
        if node.func.attr == 'assertEquals':
            for arg in node.args:
                if isinstance(arg, Name):
                    argName = arg

            return Call(func=Attribute(value=Name(id='self', ctx=Load()), 
                        attr='assertTrue', ctx=Load()), 
                        args=[argName], 
                        keywords=node.keywords)
        else:
            return node


class AssertTrueCommand(RewriterCommand):
    # Implementar comando, recuerde que puede necesitar implementar además clases NodeTransformer y/o NodeVisitor.

    def apply(self, node):
        print(ast.dump(node, indent=4))
        visitor = AssertTrueTransformer()
        new_tree = fix_missing_locations(visitor.visit(node))
        return new_tree

