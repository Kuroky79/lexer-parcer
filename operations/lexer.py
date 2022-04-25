import re
from tokens import Token, TokenType

WHITESPACE = ' \n\t' #содержит символ пробела и сивол табуляции
DIGITS = '0123456789'
VAR = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'

class Lexer:
    def __init__(self, text): #функция конструктора для приема текста
        self.text = iter(text)
        self.advance()

    def advance(self): #расширенный метод для перехода к следующему символу
        try:
            self.current_char = next(self.text)
        except StopIteration:
            self.current_char = None

    def generate_tokens(self): #метод генерации токенов
        while self.current_char != None:
            if self.current_char in WHITESPACE:
                self.advance()
            elif self.current_char == '.' or self.current_char in DIGITS:
                yield self.generate_number()
            elif self.current_char in VAR:
                yield self.generate_var()
            elif self.current_char == '+':
                self.advance()
                yield Token(TokenType.PLUS)
            elif self.current_char == '-':
                self.advance()
                yield Token(TokenType.MINUS)
            elif self.current_char == '*':
                self.advance()
                yield Token(TokenType.MULTIPLY)
            elif self.current_char == '/':
                self.advance()
                yield Token(TokenType.DIVIDE)
            elif self.current_char == '(':
                self.advance()
                yield Token(TokenType.LPAREN)
            elif self.current_char == ')':
                self.advance()
                yield Token(TokenType.RPAREN)
            elif self.current_char == 'if':
                self.advance()
                yield Token(TokenType.IF_KW)
            elif self.current_char == 'for':
                self.advance()
                yield Token(TokenType.FOR_KW)
            elif self.current_char == 'while':
                self.advance()
                yield Token(TokenType.WHILE_KW)
            elif self.current_char == '=':
                self.advance()
                yield Token(TokenType.ASSIGN_OP)
            elif self.current_char == ' ':
                self.advance()
                yield Token(TokenType.SPACE)
            elif self.current_char == ';':
                self.advance()
                yield Token(TokenType.END_LINE)
            elif self.current_char == '}':
                self.advance()
                yield Token(TokenType.R_BRACE)
            elif self.current_char == '\\{':
                self.advance()
                yield Token(TokenType.L_BRACE)
            else:
                raise Exception(f"Illegal character '{self.current_char}'")

    def generate_number(self):
        decimal_point_count = 0
        number_str = self.current_char #начало строки и отслеживание по текущему символу
        self.advance()

        while self.current_char != None and (self.current_char == '.' or self.current_char in DIGITS):
            if self.current_char == '.': #проверка на две точки в числе
                decimal_point_count += 1
                if decimal_point_count > 1:
                    break

            number_str += self.current_char
            self.advance()

        if number_str.startswith('.'):
            number_str = '0' + number_str
        if number_str.endswith('.'):
            number_str += '0'

        return Token(TokenType.NUMBER, float(number_str))

    def generate_var(self):
        decimal_point_count = 0
        var_str = self.current_char
        self.advance()

        while self.current_char != None and (self.current_char == '.' or self.current_char in VAR):
            if self.current_char == '.':
                decimal_point_count += 1
                if decimal_point_count > 1:
                    break

            var_str += self.current_char
            self.advance()
        return Token(TokenType.VAR, var_str)