from enum import Enum, auto


class TokenKind(Enum):
    """Representa um tipo de token da linguagem "A"."""
    # número
    LITERAL_INT = auto()
    LITERAL_FLOAT = auto()
    # sequência de caracteres
    LITERAL_STR = auto()
    # delimitador
    DELIMITER = auto()
    # palavra reservada
    DECLARACOES = auto()
    ALGORITMO = auto()
    INT = auto()
    REAL = auto()
    ATRIBUIR = auto()
    A = auto()
    LER = auto()
    IMPRIMIR = auto()
    SE = auto()
    ENTAO = auto()
    ENQUANTO = auto()
    INICIO = auto()
    FIM = auto()
    # parêntese
    LEFT_PARENTHESIS = auto()
    RIGHT_PARENTHESIS = auto()
    # operador relacional
    EQUAL = auto()
    NOT_EQUAL = auto()
    LESS = auto()
    GREATER = auto()
    LESS_EQUAL = auto()
    GREATER_EQUAL = auto()
    # operador aritmético
    ADDITION = auto()
    SUBTRACTION = auto()
    MULTIPLICATION = auto()
    DIVISION = auto()
    # operador booleano
    AND = auto()
    OR = auto()
    # identificador
    IDENTIFIER = auto()

    def __str__(self):
        return self.name


class Token:
    def __init__(self, kind: TokenKind, lexeme: str):
        """Cria um token da linguagem "A".

        Args:
            kind: O tipo do token.
            lexeme: O lexema do token.
        """
        self._kind = kind
        self._lexeme = lexeme

    def __repr__(self) -> str:
        return f'<{self._kind}, "{self._lexeme}">'

    @property
    def kind(self):
        """O tipo do token."""
        return self._kind

    @property
    def lexeme(self):
        """O lexema do token."""
        return self._lexeme
