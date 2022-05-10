from dataclasses import dataclass


@dataclass
class Number:
    value: any

    def __repr__(self): #метод представления
        return f"{self.value}"