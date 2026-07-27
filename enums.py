from enum import Enum

class MovementType(str, Enum):
    ENTRADA  = "entrada"
    SAIDA  = "saida"
    AJUSTE  = "ajuste"