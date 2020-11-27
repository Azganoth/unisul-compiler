from enum import Enum, auto


class TokenKind(Enum):
    """Representa um tipo de token da linguagem "A"."""
    # número
    INTEGER = auto()
    FLOAT = auto()
    # sequência de caracteres
    STRING = auto()
    # palavra reservada
    DECLARACOES_RESERVED_WORD = auto()
    ALGORITMO_RESERVED_WORD = auto()
    INT_RESERVED_WORD = auto()
    REAL_RESERVED_WORD = auto()
    ATRIBUIR_RESERVED_WORD = auto()
    A_RESERVED_WORD = auto()
    LER_RESERVED_WORD = auto()
    IMPRIMIR_RESERVED_WORD = auto()
    SE_RESERVED_WORD = auto()
    ENTAO_RESERVED_WORD = auto()
    ENQUANTO_RESERVED_WORD = auto()
    INICIO_RESERVED_WORD = auto()
    FIM_RESERVED_WORD = auto()
    # operador booleano
    AND_BOOLEAN_OPERATOR = auto()
    OR_BOOLEAN_OPERATOR = auto()
    # identificador
    IDENTIFIER = auto()
    # operador relacional
    EQUAL_RELATIONAL_OPERATOR = auto()
    LESS_RELATIONAL_OPERATOR = auto()
    GREATER_RELATIONAL_OPERATOR = auto()
    LESS_EQUAL_RELATIONAL_OPERATOR = auto()
    GREATER_EQUAL_RELATIONAL_OPERATOR = auto()
    EQUIVALENT_RELATIONAL_OPERATOR = auto()
    # operador aritmético
    ADDITION_ARITHMETIC_OPERATOR = auto()
    SUBTRACTION_ARITHMETIC_OPERATOR = auto()
    MULTIPLICATION_ARITHMETIC_OPERATOR = auto()
    DIVISION_ARITHMETIC_OPERATOR = auto()
    # parêntese
    OPEN_PARENTHESIS = auto()
    CLOSE_PARENTHESIS = auto()
    # delimitador
    DELIMITER = auto()


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
        return f'<{self._kind.name}, "{self._lexeme}">'

    @property
    def kind(self):
        """O tipo do token."""
        return self._kind

    @property
    def lexeme(self):
        """O lexema do token."""
        return self._lexeme
