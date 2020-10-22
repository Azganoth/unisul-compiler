from enum import Enum, auto
from pathlib import Path
from typing import List


class TokenKind(Enum):
    """Representa um tipo de token da linguagem "AL"."""
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
        """Cria um token válido da linguagem "AL".

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


def describe_code(source_file_path: Path):
    """Retorna uma lista de tokens válidos, para a linguagem "AL", encontrados
    no código-fonte do arquivo.

    Args:
        source_file_path: O caminho do arquivo contendo o código-fonte.

    Returns:
        A lista de tokens válidos encontrados no código-fonte do arquivo.

    Raises:
        ALLexicalError: Caso um token inválido seja encontrado no código-fonte.
    """
    tokens: List[Token] = []

    with open(source_file_path) as source_file:
        source_code = source_file.read()

        # Ponteiro
        pointer = 0

        def peek():
            """Retorna o caractere embaixo do ponteiro sem modificar a posição
            do ponteiro.

            Returns:
                O caractere embaixo do ponteiro ou ``''`` caso o ponteiro
                esteja fora dos limites do código-fonte, simbolizando
                o fim do arquivo.
            """
            try:
                return source_code[pointer]
            except IndexError:
                return ''

        def skip():
            """Move o ponteiro para o próximo caractere."""
            nonlocal pointer
            pointer += 1

        def consume():
            """Retorna o caractere embaixo do ponteiro e move o ponteiro para
            o próximo caractere.

            Returns:
                O caractere embaixo do ponteiro ou ``''`` caso o ponteiro
                esteja fora dos limites do código-fonte, simbolizando
                o fim do arquivo.
            """
            character = peek()
            skip()
            return character

        def recede(len_: int):
            """Retrocede a posição do ponteiro.

            Args:
                len_: A quantidade de caracteres a retroceder.
            """
            nonlocal pointer
            pointer -= len_

        # Padrões da linguagem "AL"
        def _garbage():
            """Ignora espaços em branco e comentários."""
            # ignorar qualquer espaço em branco ou comentário
            while (peeked_character := peek()) in [' ', '\t', '\r', '\n', '%']:
                # se for encontrado o início de um comentário,
                # ignorar todos os caracteres até uma quebra de linha ou o fim do arquivo
                if peeked_character == '%':
                    skip()
                    while peek() not in ['\r', '\n', '']:
                        skip()
                else:
                    skip()

        def _number():
            """Captura um número inteiro ou um número real.

            Returns:
                O token válido ou ``None`` caso não seja possível formar
                um token válido.
            """
            lexeme = ''

            if peek() in ['+', '-']:
                lexeme += consume()

            if peek().isnumeric():
                lexeme += consume()
                while peek().isnumeric():
                    lexeme += consume()
            else:
                recede(len(lexeme))
                return None

            if peek() == '.':
                lexeme += consume()

                if peek().isnumeric():
                    lexeme += consume()
                    while peek().isnumeric():
                        lexeme += consume()

                    return Token(TokenKind.FLOAT, lexeme)
                else:
                    recede(len(lexeme))
                    return None
            else:
                return Token(TokenKind.INTEGER, lexeme)

        def _string():
            """Captura uma cadeia de caracteres.

            Returns:
                O token válido ou ``None`` caso não seja possível formar
                um token válido.
            """
            lexeme = ''

            if peek() == "'":
                lexeme += consume()
                while peek() not in ["'", '\n', '']:
                    lexeme += consume()

                if peek() in ['\n', '']:
                    recede(len(lexeme))
                    return None
                else:
                    return Token(TokenKind.STRING, lexeme)
            else:
                return None

        def _reserved_word():
            """Captura uma palavra reservada.

            Returns:
                O token válido ou ``None`` caso não seja possível formar
                um token válido.
            """
            lexeme = ''

            while peek().isalpha():
                lexeme += consume()

            if lexeme == 'DECLARACOES':
                return Token(TokenKind.DECLARACOES_RESERVED_WORD, lexeme)
            elif lexeme == 'ALGORITMO':
                return Token(TokenKind.ALGORITMO_RESERVED_WORD, lexeme)
            elif lexeme == 'INT':
                return Token(TokenKind.INT_RESERVED_WORD, lexeme)
            elif lexeme == 'REAL':
                return Token(TokenKind.REAL_RESERVED_WORD, lexeme)
            elif lexeme == 'ATRIBUIR':
                return Token(TokenKind.ATRIBUIR_RESERVED_WORD, lexeme)
            elif lexeme == 'A':
                return Token(TokenKind.A_RESERVED_WORD, lexeme)
            elif lexeme == 'LER':
                return Token(TokenKind.LER_RESERVED_WORD, lexeme)
            elif lexeme == 'IMPRIMIR':
                return Token(TokenKind.IMPRIMIR_RESERVED_WORD, lexeme)
            elif lexeme == 'SE':
                return Token(TokenKind.SE_RESERVED_WORD, lexeme)
            elif lexeme == 'ENTAO':
                return Token(TokenKind.ENTAO_RESERVED_WORD, lexeme)
            elif lexeme == 'ENQUANTO':
                return Token(TokenKind.ENQUANTO_RESERVED_WORD, lexeme)
            elif lexeme == 'INICIO':
                return Token(TokenKind.INICIO_RESERVED_WORD, lexeme)
            elif lexeme == 'FIM':
                return Token(TokenKind.FIM_RESERVED_WORD, lexeme)
            else:
                recede(len(lexeme))
                return None

        def _boolean_operator():
            """Captura um operador booleano.

            Returns:
                O token válido ou ``None`` caso não seja possível formar
                um token válido.
            """
            lexeme = ''

            while peek().isalpha():
                lexeme += consume()

            if lexeme == 'AND':
                return Token(TokenKind.AND_BOOLEAN_OPERATOR, lexeme)
            elif lexeme == 'OR':
                return Token(TokenKind.OR_BOOLEAN_OPERATOR, lexeme)
            else:
                recede(len(lexeme))
                return None

        def _identifier():
            """Captura um identificador.

            Returns:
                O token válido ou ``None`` caso não seja possível formar
                um token válido.
            """
            lexeme = ''

            if peek().isalpha():
                lexeme += consume()

                while peek().isalnum():
                    lexeme += consume()

                return Token(TokenKind.IDENTIFIER, lexeme)
            else:
                recede(len(lexeme))
                return None

        def _relational_operator():
            """Captura um operador relacional.

            Returns:
                O token válido ou ``None`` caso não seja possível formar
                um token válido.
            """
            lexeme = ''

            if (peeked_character := peek()) == '=':
                lexeme += consume()
                return Token(TokenKind.EQUAL_RELATIONAL_OPERATOR, lexeme)
            elif peeked_character == '<':
                lexeme += consume()
                if (peeked_character := peek()) == '=':
                    return Token(TokenKind.LESS_EQUAL_RELATIONAL_OPERATOR, lexeme)
                elif peeked_character == '>':
                    return Token(TokenKind.EQUIVALENT_RELATIONAL_OPERATOR, lexeme)
                else:
                    return Token(TokenKind.LESS_RELATIONAL_OPERATOR, lexeme)
            elif peeked_character == '>':
                lexeme += consume()
                if peek() == '=':
                    lexeme += consume()
                    return Token(TokenKind.GREATER_EQUAL_RELATIONAL_OPERATOR, lexeme)
                else:
                    return Token(TokenKind.GREATER_RELATIONAL_OPERATOR, lexeme)
            else:
                return None

        def _arithmetic_operator():
            """Captura um operador aritmético.

            Returns:
                O token válido ou ``None`` caso não seja possível formar
                um token válido.
            """
            lexeme = ''

            if (peeked_character := peek()) == '+':
                lexeme += consume()
                return Token(TokenKind.ADDITION_ARITHMETIC_OPERATOR, lexeme)
            elif peeked_character == '-':
                lexeme += consume()
                return Token(TokenKind.SUBTRACTION_ARITHMETIC_OPERATOR, lexeme)
            elif peeked_character == '*':
                lexeme += consume()
                return Token(TokenKind.MULTIPLICATION_ARITHMETIC_OPERATOR, lexeme)
            elif peeked_character == '/':
                lexeme += consume()
                return Token(TokenKind.DIVISION_ARITHMETIC_OPERATOR, lexeme)
            else:
                return None

        def _parenthesis():
            """Captura um parêntese.

            Returns:
                O token válido ou ``None`` caso não seja possível formar
                um token válido.
            """
            lexeme = ''

            if (peeked_character := peek()) == '(':
                lexeme += consume()
                return Token(TokenKind.OPEN_PARENTHESIS, lexeme)
            elif peeked_character == ')':
                lexeme += consume()
                return Token(TokenKind.CLOSE_PARENTHESIS, lexeme)
            else:
                return None

        def _delimiter():
            """Captura um delimitador.

            Returns:
                O token válido ou ``None`` caso não seja possível formar
                um token válido.
            """
            lexeme = ''

            if peek() == ':':
                lexeme += consume()
                return Token(TokenKind.DELIMITER, lexeme)
            else:
                return None

        # percorrer todo o código-fonte
        while pointer < len(source_code):
            _garbage()

            # ignorar verificações caso tenhamos chegado no fim do arquivo
            if peek() == '':
                continue
            # verificar cada padrão até encontrar um token válido
            elif (token := _number()) is not None:
                tokens.append(token)
            elif (token := _string()) is not None:
                tokens.append(token)
            elif (token := _reserved_word()) is not None:
                tokens.append(token)
            elif (token := _boolean_operator()) is not None:
                tokens.append(token)
            elif (token := _identifier()) is not None:
                tokens.append(token)
            elif (token := _relational_operator()) is not None:
                tokens.append(token)
            elif (token := _arithmetic_operator()) is not None:
                tokens.append(token)
            elif (token := _parenthesis()) is not None:
                tokens.append(token)
            elif (token := _delimiter()) is not None:
                tokens.append(token)
            # levantar um erro léxico caso nenhum padrão seja encontrado
            else:
                raise ALLexicalError('Erro léxico!')

    return tokens


class ALLexicalError(Exception):
    """Levanta uma exceção ao encontrar um erro léxico da Linguagem "AL"
    no código-fonte.
    """
