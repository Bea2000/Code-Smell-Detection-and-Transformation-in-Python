from _ast import AST, Assign, FunctionDef
from ast import *
import ast
from typing import Any
from core.rewriter import RewriterCommand
import astor

class ExtractSetupTransformer(NodeTransformer):
    def __init__(self):
        super().__init__()
        self.bodies = []
        self.common_code = []
        self.setup_method = None

    def visit_FunctionDef(self, node: FunctionDef):
        self.bodies.append(node.body)
        print(self.bodies)
        
        return node
        
    def extract_common_code(self):
        num_sublists = len(self.bodies)

        # Diccionario para contar cuántas veces aparece cada elemento en todas las sublistas
        element_count_dict = {}

        # Iteramos sobre las sublistas y sobre los elementos de cada sublista
        for i in range(len(self.bodies)):
            for j in range(len(self.bodies[i])):
                elem_str = ast.dump(self.bodies[i][j])
                elem_ast = self.bodies[i][j]
                # Si el elemento no está en el diccionario, lo agregamos con valor 1
                if elem_str not in element_count_dict:
                    element_count_dict[elem_str] = {"ast": elem_ast, "count": 1}
                # Si el elemento ya está en el diccionario, le sumamos 1 al valor
                else:
                    element_count_dict[elem_str]["count"] += 1

        # Verificamos cuáles elementos aparecen en todas las sublistas
        for elem_str in element_count_dict:
            if element_count_dict[elem_str]["count"] == num_sublists:
                # Convierte la cadena nuevamente a un objeto AST y se agrega a la lista de código común
                self.common_code.append(element_count_dict[elem_str]["ast"])
                
    def modify_body(self):
        # Create de FunctionDef for setUp
        if self.common_code:
            # Crear una lista de Assign con self para el body del método setUp
            setup_body = [
                Assign(
                    targets=[
                        Attribute(
                            value=Name(id='self', ctx=Load()),
                            attr=elem.targets[0].id,
                            ctx=Store())],
                    value=elem.value,
                ) for elem in self.common_code
            ]

            # Crear el método setUp con la lista de Asssign
            self.setup_method = FunctionDef(
                name='setUp',
                args=arguments(
                    posonlyargs=[],
                    args=[
                        arg(arg='self')],
                    kwonlyargs=[],
                    kw_defaults=[],
                    defaults=[]),
                body=setup_body,
                decorator_list=[],
                )
    
        print("COMENZANDO ELIMINACIÓN".center(50, "-"))
        print(f"Self.bodies 1: {self.bodies}")
        for sub_bodies in self.bodies:
            # Eliminar las líneas comunes de cada body
            for elem_common_code in self.common_code:
                for elem_sub_bodies in sub_bodies:
                    if ast.dump(elem_common_code) == ast.dump(elem_sub_bodies):
                        print(f"Removing {ast.dump(elem_sub_bodies)}")
                        sub_bodies.remove(elem_sub_bodies)
        print(f"Self.bodies 2: {self.bodies}")
        print("TERMINANDO ELIMINACIÓN".center(50, "-"))

        # Agregar self a cada variable
        if self.setup_method:
            for sub_bodies in self.bodies:
                for elem_sub_bodies in sub_bodies:
                    if isinstance(elem_sub_bodies, Expr):
                        if isinstance(elem_sub_bodies.value, Call):
                            print("VALUE",elem_sub_bodies.value)
                            new_arguments = []
                            for argument in elem_sub_bodies.value.args:
                                print("ARGUMENT",argument)
                                if isinstance(argument, Name):
                                    argument = Attribute(
                                        value=Name(id='self', ctx=Load()),
                                        attr=argument.id,
                                        ctx=Load())
                                elif isinstance(argument, Call):
                                    argument =  Call(
                                        func=Attribute(
                                            value=Attribute(
                                                value=Name(id='self', ctx=Load()),
                                                attr=argument.func.value.id,
                                                ctx=Load()),
                                            attr=argument.func.attr,
                                            ctx=Load()),
                                        args=[],
                                        keywords=[])
                                elif isinstance(argument, Constant):
                                    pass
                                new_arguments.append(argument)
                            elem_sub_bodies.value.args = new_arguments
                            print(f"new_arguments: {new_arguments}")
        
    def function_modify_body(self, node):
        # print("NEW NODE COPY",ast.dump(node, indent=4))
        if self.setup_method:
            print(f"node.body[0].body: {node.body[0].body}")
            node.body[0].body.insert(0, self.setup_method)
            print(f"self.bodies: {self.bodies}")
            print(f"len(self.bodies): {len(self.bodies)}".center(50, "+"))
            print(f"len(node.body[0].body): {len(node.body[0].body)}".center(50, "+"))
            for i in range(len(self.bodies)):
                node.body[0].body[i + 1].body = self.bodies[i]

            return node
        return node


class ExtractSetupCommand(RewriterCommand):
    # Implementar comando, recuerde que puede necesitar implementar además clases NodeTransformer y/o NodeVisitor.

    def apply(self, node):
        print("ORIGINAL NODE",ast.dump(node, indent=4))
        visitor = ExtractSetupTransformer()
        visitor.visit(node)
        visitor.extract_common_code()
        visitor.modify_body()
        new_node = visitor.function_modify_body(node)
        print("NEW NODE",ast.dump(new_node, indent=4))
        print(astor.to_source(new_node))
        new_tree = fix_missing_locations(new_node)
        return new_tree

    @classmethod
    def name(cls):
        return 'extract-setup'
