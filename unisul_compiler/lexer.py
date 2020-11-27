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
                if tokens[-1].kind in [TokenKind.INTEGER, TokenKind.FLOAT, TokenKind.IDENTIFIER]:
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

                return Token(TokenKind.FLOAT, lexeme)
            else:
                for _ in range(len(lexeme)):
                    recede()
                return None
        else:
            return Token(TokenKind.INTEGER, lexeme)

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
                return Token(TokenKind.STRING, lexeme)
            else:
                for _ in range(len(lexeme)):
                    recede()
                return None
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
            for _ in range(len(lexeme)):
                recede()
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

        if lexeme == 'AND':
            return Token(TokenKind.AND_BOOLEAN_OPERATOR, lexeme)
        elif lexeme == 'OR':
            return Token(TokenKind.OR_BOOLEAN_OPERATOR, lexeme)
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

    def relational_operator():
        """Captura um operador relacional.

        Returns:
            O token.
            ``None`` caso não forme um token válido.
        """
        lexeme = ''

        if (peeked_character := peek()) == '=':
            lexeme += advance()
            return Token(TokenKind.EQUAL_RELATIONAL_OPERATOR, lexeme)
        elif peeked_character == '<':
            lexeme += advance()
            if (peeked_character := peek()) == '=':
                return Token(TokenKind.LESS_EQUAL_RELATIONAL_OPERATOR, lexeme)
            elif peeked_character == '>':
                return Token(TokenKind.EQUIVALENT_RELATIONAL_OPERATOR, lexeme)
            else:
                return Token(TokenKind.LESS_RELATIONAL_OPERATOR, lexeme)
        elif peeked_character == '>':
            lexeme += advance()
            if peek() == '=':
                lexeme += advance()
                return Token(TokenKind.GREATER_EQUAL_RELATIONAL_OPERATOR, lexeme)
            else:
                return Token(TokenKind.GREATER_RELATIONAL_OPERATOR, lexeme)
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
            return Token(TokenKind.ADDITION_ARITHMETIC_OPERATOR, lexeme)
        elif peeked_character == '-':
            lexeme += advance()
            return Token(TokenKind.SUBTRACTION_ARITHMETIC_OPERATOR, lexeme)
        elif peeked_character == '*':
            lexeme += advance()
            return Token(TokenKind.MULTIPLICATION_ARITHMETIC_OPERATOR, lexeme)
        elif peeked_character == '/':
            lexeme += advance()
            return Token(TokenKind.DIVISION_ARITHMETIC_OPERATOR, lexeme)
        else:
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
            return Token(TokenKind.OPEN_PARENTHESIS, lexeme)
        elif peeked_character == ')':
            lexeme += advance()
            return Token(TokenKind.CLOSE_PARENTHESIS, lexeme)
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
        elif (token := reserved_word()) is not None:
            tokens.append(token)
        elif (token := boolean_operator()) is not None:
            tokens.append(token)
        elif (token := identifier()) is not None:
            tokens.append(token)
        elif (token := relational_operator()) is not None:
            tokens.append(token)
        elif (token := arithmetic_operator()) is not None:
            tokens.append(token)
        elif (token := parenthesis()) is not None:
            tokens.append(token)
        elif (token := delimiter()) is not None:
            tokens.append(token)
        # caso não encontre um token válido, levantar um erro léxico
        else:
            raise ALexicalError('erro léxico encontrado')

        print(f'🥳 {token} encontrado')

    return tokens
