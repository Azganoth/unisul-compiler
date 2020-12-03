from typing import List

from .token import Token, TokenKind
from .exceptions import ALexicalError


def describe(source_code: str):
    """Analisa o código-fonte e retorna os tokens válidos encontrados
    da línguagem "A".

    Args:
        source_code: O código-fonte.

    Returns:
        Os tokens válidos encontrados no código-fonte.

    Raises:
        ALexicalError: Caso encontre um símbolo inválido no código-fonte.
    """
    tokens: List[Token] = []

    pointer = 0

    def peek():
        """Retorna o caractere sob o ponteiro.

        Returns:
            O caractere sob o ponteiro.
            ``''`` caso o ponteiro esteja fora dos limites do código-fonte.
        """
        try:
            return source_code[pointer]
        except IndexError:
            return ''

    def skip():
        """Avança a posição do ponteiro."""
        nonlocal pointer
        pointer += 1

    def recede():
        """Retrocede a posição do ponteiro."""
        nonlocal pointer
        pointer -= 1

    def advance():
        """Consome o caractere sob o ponteiro, avança a posição do ponteiro
        e retorna o caractere consumido.

        Returns:
            O caractere sob o ponteiro.
            ``''`` caso o ponteiro esteja fora dos limites do código-fonte.
        """
        character = peek()
        skip()
        return character

    # Padrões léxicos da linguagem "A"
    def garbage():
        """Ignora espaços em branco e comentários."""
        while (peeked_character := peek()) in [' ', '\t', '\r', '\n', '%']:
            skip()
            if peeked_character == '%':
                while peek() not in ['\r', '\n', '']:
                    skip()

    def number():
        """Captura um número inteiro ou real.

        Returns:
            O token.
            ``None`` caso não forme um token válido.
        """
        lexeme = ''

        if peek() in ['+', '-']:
            try:
                if tokens[-1].kind in [TokenKind.LITERAL_INT, TokenKind.LITERAL_FLOAT, TokenKind.IDENTIFIER]:
                    return None
            except IndexError:
                pass
            lexeme += advance()

        if peek().isnumeric():
            lexeme += advance()
            while peek().isnumeric():
                lexeme += advance()
        else:
            for _ in range(len(lexeme)):
                recede()
            return None

        if peek() == '.':
            lexeme += advance()

            if peek().isnumeric():
                lexeme += advance()
                while peek().isnumeric():
                    lexeme += advance()

                return Token(TokenKind.LITERAL_FLOAT, lexeme)
            else:
                for _ in range(len(lexeme)):
                    recede()
                return None
        else:
            return Token(TokenKind.LITERAL_INT, lexeme)

    def string():
        """Captura uma cadeia de caracteres.

        Returns:
            O token.
            ``None`` caso não forme um token válido.
        """
        lexeme = ''

        if peek() == "'":
            lexeme += advance()
            while peek() not in ["'", '\n', '']:
                lexeme += advance()

            if peek() == "'":
                lexeme += advance()
                return Token(TokenKind.LITERAL_STR, lexeme)
            else:
                for _ in range(len(lexeme)):
                    recede()
                return None
        else:
            return None

    def delimiter():
        """Captura um delimitador.

        Returns:
            O token.
            ``None`` caso não forme um token válido.
        """
        lexeme = ''

        if peek() == ':':
            lexeme += advance()
            return Token(TokenKind.DELIMITER, lexeme)
        else:
            return None

    def reserved_word():
        """Captura uma palavra reservada.

        Returns:
            O token.
            ``None`` caso não forme um token válido.
        """
        lexeme = ''

        while peek().isalpha():
            lexeme += advance()

        if lexeme == 'DECLARACOES':
            return Token(TokenKind.DECLARACOES, lexeme)
        elif lexeme == 'ALGORITMO':
            return Token(TokenKind.ALGORITMO, lexeme)
        elif lexeme == 'INT':
            return Token(TokenKind.INT, lexeme)
        elif lexeme == 'REAL':
            return Token(TokenKind.REAL, lexeme)
        elif lexeme == 'ATRIBUIR':
            return Token(TokenKind.ATRIBUIR, lexeme)
        elif lexeme == 'A':
            return Token(TokenKind.A, lexeme)
        elif lexeme == 'LER':
            return Token(TokenKind.LER, lexeme)
        elif lexeme == 'IMPRIMIR':
            return Token(TokenKind.IMPRIMIR, lexeme)
        elif lexeme == 'SE':
            return Token(TokenKind.SE, lexeme)
        elif lexeme == 'ENTAO':
            return Token(TokenKind.ENTAO, lexeme)
        elif lexeme == 'ENQUANTO':
            return Token(TokenKind.ENQUANTO, lexeme)
        elif lexeme == 'INICIO':
            return Token(TokenKind.INICIO, lexeme)
        elif lexeme == 'FIM':
            return Token(TokenKind.FIM, lexeme)
        else:
            for _ in range(len(lexeme)):
                recede()
            return None

    def parenthesis():
        """Captura um parêntese.

        Returns:
            O token.
            ``None`` caso não forme um token válido.
        """
        lexeme = ''

        if (peeked_character := peek()) == '(':
            lexeme += advance()
            return Token(TokenKind.LEFT_PARENTHESIS, lexeme)
        elif peeked_character == ')':
            lexeme += advance()
            return Token(TokenKind.RIGHT_PARENTHESIS, lexeme)
        else:
            return None

    def relational_operator():
        """Captura um operador relacional.

        Returns:
            O token.
            ``None`` caso não forme um token válido.
        """
        lexeme = ''

        if (peeked_character := peek()) == '=':
            lexeme += advance()
            return Token(TokenKind.EQUAL, lexeme)
        elif peeked_character == '<':
            lexeme += advance()
            if (peeked_character := peek()) == '=':
                lexeme += advance()
                return Token(TokenKind.LESS_EQUAL, lexeme)
            elif peeked_character == '>':
                lexeme += advance()
                return Token(TokenKind.NOT_EQUAL, lexeme)
            else:
                return Token(TokenKind.LESS, lexeme)
        elif peeked_character == '>':
            lexeme += advance()
            if peek() == '=':
                lexeme += advance()
                return Token(TokenKind.GREATER_EQUAL, lexeme)
            else:
                return Token(TokenKind.GREATER, lexeme)
        else:
            return None

    def arithmetic_operator():
        """Captura um operador aritmético.

        Returns:
            O token.
            ``None`` caso não forme um token válido.
        """
        lexeme = ''

        if (peeked_character := peek()) == '+':
            lexeme += advance()
            return Token(TokenKind.ADDITION, lexeme)
        elif peeked_character == '-':
            lexeme += advance()
            return Token(TokenKind.SUBTRACTION, lexeme)
        elif peeked_character == '*':
            lexeme += advance()
            return Token(TokenKind.MULTIPLICATION, lexeme)
        elif peeked_character == '/':
            lexeme += advance()
            return Token(TokenKind.DIVISION, lexeme)
        else:
            return None

    def boolean_operator():
        """Captura um operador booleano.

        Returns:
            O token.
            ``None`` caso não forme um token válido.
        """
        lexeme = ''

        while peek().isalpha():
            lexeme += advance()

        if lexeme == 'E':
            return Token(TokenKind.AND, lexeme)
        elif lexeme == 'OU':
            return Token(TokenKind.OR, lexeme)
        else:
            for _ in range(len(lexeme)):
                recede()
            return None

    def identifier():
        """Captura um identificador.

        Returns:
            O token.
            ``None`` caso não forme um token válido.
        """
        lexeme = ''

        if peek().isalpha():
            lexeme += advance()

            while peek().isalnum():
                lexeme += advance()

            return Token(TokenKind.IDENTIFIER, lexeme)
        else:
            return None

    # procurar padrões da linguagem "A" até o fim do código-fonte
    while True:
        garbage()

        # parar a procura por padrões ao chegar no fim do código-fonte
        if peek() == '':
            break

        # procurar e capturar um token válido,
        if (token := number()) is not None:
            tokens.append(token)
        elif (token := string()) is not None:
            tokens.append(token)
        elif (token := delimiter()) is not None:
            tokens.append(token)
        elif (token := reserved_word()) is not None:
            tokens.append(token)
        elif (token := parenthesis()) is not None:
            tokens.append(token)
        elif (token := relational_operator()) is not None:
            tokens.append(token)
        elif (token := arithmetic_operator()) is not None:
            tokens.append(token)
        elif (token := boolean_operator()) is not None:
            tokens.append(token)
        elif (token := identifier()) is not None:
            tokens.append(token)
        # caso não encontre um token válido, levantar um erro léxico
        else:
            raise ALexicalError('erro léxico encontrado')

        print(f'🥳 {token} encontrado')

    return tokens
