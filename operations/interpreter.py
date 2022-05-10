from nodes import *
from values import Number


class Interpreter:
    def __init__(self):
        pass

    def visit(self, node): #передача корневого узла
        method_name = f'visit_{type(node).__name__}' #к примеру метод добавления будет преобразован в метод посещения
        method = getattr(self, method_name) #функция атрибута получаем сообщение от себя а потом передаем имя метода
        return method(node)

    def visit_NumberNode(self, node):
        return Number(node.value) #значение числа будет просто значение числового узла

    def visit_AddNode(self, node):
        return Number(self.visit(node.node_a).value + self.visit(node.node_b).value)

    def visit_SubtractNode(self, node):
        return Number(self.visit(node.node_a).value - self.visit(node.node_b).value)

    def visit_MultiplyNode(self, node):
        return Number(self.visit(node.node_a).value * self.visit(node.node_b).value)

    def visit_DivideNode(self, node):
        try:
            return Number(self.visit(node.node_a).value / self.visit(node.node_b).value)
        except:
            raise Exception("Runtime math error")

    def visit_PlusNode(self, node):
        return self.visit(node, node)

    def visit_MinusNode(self, node):
        return Number(-self.visit(node, node).value) #берем значение из этого числа и возвращаем число с минусом