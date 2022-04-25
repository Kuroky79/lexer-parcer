from enum import Enum
from dataclasses import dataclass

class TokenType(Enum):
	NUMBER    = 0 #токены и их индефикация по порядку
	PLUS      = 1
	MINUS     = 2
	MULTIPLY  = 3
	DIVIDE    = 4
	LPAREN    = 5
	RPAREN    = 6
	VAR       = 7
	INT       = 8
	IF_KW     = 9
	FOR_KW    = 10
	WHILE_KW  = 11
	ASSIGN_OP = 12
	SPACE     = 13
	END_LINE  = 14
	R_BRACE   = 15
	L_BRACE   = 16
@dataclass
class Token: #класс для определения существования токена
	type: TokenType
	value: any = None

	def __repr__(self): #функция для нормальной отладки токена если он определен
		return self.type.name + (f":{self.value}" if self.value != None else "")
