from tokens import TokenType #преобразует наши токены в узлы
from nodes import *


class Parser:
    def __init__(self, tokens): #парацинировать наших токенов
        self.tokens = iter(tokens) #находение токенов в форме иттератора
        self.advance()

    def raise_error(self): #метод поднятой ошибки
        raise Exception("Invalid syntax")

    def advance(self):
        try:
            self.current_token = next(self.tokens) #расширенный метод который назначает переход к следующему токену в ячейках со стопом иттерации которая достигается в конце списка токенов
        except StopIteration:
            self.current_token = None

    def parse(self): #метод уничтожения в собственном методе expr который вернет узел
        if self.current_token == None:
            return None

        result = self.expr()

        if self.current_token != None:
            self.raise_error()

        return result

    def expr(self):
        result = self.term() #вызов термина если находится оператор записываем в результат

        while self.current_token != None and self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            if self.current_token.type == TokenType.PLUS:
                self.advance()
                result = AddNode(result, self.term())
            elif self.current_token.type == TokenType.MINUS:
                self.advance()
                result = SubtractNode(result, self.term())

        return result

    def term(self):
        result = self.factor()

        while self.current_token != None and self.current_token.type in (TokenType.MULTIPLY, TokenType.DIVIDE):
            if self.current_token.type == TokenType.MULTIPLY:
                self.advance()
                result = MultiplyNode(result, self.factor())
            elif self.current_token.type == TokenType.DIVIDE:
                self.advance()
                result = DivideNode(result, self.factor())

        return result

    def factor(self):
        token = self.current_token

        if token.type == TokenType.LPAREN:
            self.advance()
            result = self.expr()

            if self.current_token.type != TokenType.RPAREN:
                self.raise_error()

            self.advance()
            return result

        elif token.type == TokenType.NUMBER: #проверка равен ли текущий токен числу
            self.advance()
            return NumberNode(token.value)

        elif token.type == TokenType.PLUS:
            self.advance()
            return PlusNode(self.factor())

        elif token.type == TokenType.MINUS:
            self.advance()
            return MinusNode(self.factor())

        self.raise_error()