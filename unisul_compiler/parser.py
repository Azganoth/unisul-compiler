from typing import Dict, List, Literal, Optional

from .token import Token, TokenKind
from .exceptions import ASyntaxError, ASemanticError


# Syntax
#
# program := ':' DECLARACOES {declaration} ':' ALGORITMO {command}
#
# declaration := var ':' (INT | REAL)
#
# command :=
#   ATRIBUIR arithmetic_expression A var |
#   LER var |
#   IMPRIMIR (var | STRING) |
#   SE relational_expression ENTAO command |
#   ENQUANTO relational_expression command |
#   INICIO [command] FIM
#
# relational_expression :=
#   ['('] arithmetic_expression relational_operator arithmetic_expression
#   [boolean_operator relational_expression] [')']
#
# boolean_operator := 'E' | 'OU'
#
# arithmetic_expression :=
#   ['('] exp [arithmetic_operator arithmetic_expression] [')']
#
# arithmetic_operator := '+' | '-' | '*' | '/'
#
# relational_operator := '=' | '<' | '>' | '<=' | '>=' | '<>'
#
# exp := int | float | var
#
# var := identifier


def parse(tokens: List[Token]):
    pointer = 0

    def peek():
        """Retorna o token sob o ponteiro.

        Returns:
            O token sob o ponteiro.
            ``None`` caso o ponteiro esteja fora dos limites da lista de tokens.
        """
        try:
            return tokens[pointer]
        except IndexError:
            return None

    def expect(*token_kinds: TokenKind):
        """Captura o token sob o ponteiro, certifica que o seu tipo satisfaça
        um dos tipos de token esperados, avança o ponteiro e retorna o token.

        Args:
            token_kinds: Os tipos de token esperados.

        Raises:
            ASyntaxError: Caso o tipo do token não satisfaça
                nenhum dos tipos de token esperados.

        Returns:
            O token sob o ponteiro.
        """
        nonlocal pointer
        token_kinds_repr = " | ".join(map(str, token_kinds))

        # verificar se ainda existem tokens
        if (token := peek()) is not None:
            # verificar se o tipo do token satisfaz um dos tipos de tokens esperados
            if token.kind in token_kinds:
                print(f'👌 {token} satisfaz [{token_kinds_repr}]')
                pointer += 1
                return token
            else:
                raise ASyntaxError(
                    f'erro sintático, o tipo do token {token} não satisfaz '
                    f'nenhum dos tipos de tokens esperados [{token_kinds_repr}]')
        else:
            raise ASyntaxError(
                'erro sintático, não existem mais tokens para satisfazer '
                f'nenhum dos tipos de tokens esperados [{token_kinds_repr}]')

    # Dicionário de símbolos do programa (escopo global)
    symbols: Dict[str, Literal[TokenKind.LITERAL_INT, TokenKind.LITERAL_FLOAT]] = {}

    def expect_variable(
            var_name: str,
            var_type: Optional[Literal[TokenKind.LITERAL_INT, TokenKind.LITERAL_FLOAT]] = None):
        """Certifica que a variável foi declarada e retorna seu tipo,
        e, caso especificado, satisfaça o tipo de variável esperado.

        Args:
            var_name: O identificador da variável.
            var_type: O tipo de variável esperado (opcional).

        Raises:
            ASemanticError: Caso a variável não esteja declarada.
            ASemanticError: Caso o tipo da variável não satisfaça
                o tipo de variável esperado.

        Returns:
            O tipo da variável.
        """
        # verificar se a variável foi declarada
        if (symbol_kind := symbols.get(var_name, None)) is None:
            raise ASemanticError(f'erro semântico, variável "{var_name}" não declarada')
        # verificar se o tipo da variável satisfaz o tipo de variável esperado
        elif var_type is not None and symbol_kind is not var_type:
            raise ASemanticError(
                f'erro semântico, variável "{var_name}" com o tipo {symbol_kind} não satisfaz {var_type}')

        return symbol_kind

    # Padrões da linguagem "A"
    def declaration():
        """Captura uma declaração."""
        name_token = expect(TokenKind.IDENTIFIER)
        expect(TokenKind.DELIMITER)
        type_token = expect(TokenKind.INT, TokenKind.REAL)

        # adicionar a variável ao dicionário de símbolos
        if (var_name := name_token.lexeme) not in symbols:
            symbols[var_name] = (TokenKind.LITERAL_INT
                                 if type_token.kind == TokenKind.INT else
                                 TokenKind.LITERAL_FLOAT)
        else:
            raise ASemanticError(f'erro semântico, variável "{var_name}" já foi declarada')

    def arithmetic_expression() -> Literal[TokenKind.LITERAL_INT, TokenKind.LITERAL_FLOAT]:
        """Captura uma expressão aritmética.

        Returns:
            O tipo da expressão aritmética encontrada.
        """
        left_expression = expect(TokenKind.LITERAL_INT, TokenKind.LITERAL_FLOAT,
                                 TokenKind.IDENTIFIER, TokenKind.LEFT_PARENTHESIS)

        # resolver uma expressão aritmética ao reconhecer um parênteses aberto
        if (has_parenthesis := (left_expression_kind := left_expression.kind) == TokenKind.LEFT_PARENTHESIS):
            left_expression_kind = arithmetic_expression()

        # certificar que a variável foi declarada e resgatar seu tipo, caso seja uma variável...
        if left_expression_kind == TokenKind.IDENTIFIER:
            left_expression_kind = expect_variable(left_expression.lexeme)

        if peek().kind in [
                TokenKind.ADDITION, TokenKind.SUBTRACTION,
                TokenKind.MULTIPLICATION, TokenKind.DIVISION]:
            operator = expect(
                TokenKind.ADDITION, TokenKind.SUBTRACTION,
                TokenKind.MULTIPLICATION, TokenKind.DIVISION)
            right_expression_kind = arithmetic_expression()

            # capturar o parênteses fechado (2)
            if has_parenthesis:
                expect(TokenKind.RIGHT_PARENTHESIS)

            # resolver em "inteiro" caso as duas expressões aritméticas resultarem
            # em números inteiros e o operador for adição, subtração ou multiplicação,
            # caso contrário resultar em "real"
            if (left_expression_kind == TokenKind.LITERAL_INT
                and right_expression_kind == TokenKind.LITERAL_INT
                and operator.kind in [
                    TokenKind.ADDITION, TokenKind.SUBTRACTION, TokenKind.MULTIPLICATION]):
                return TokenKind.LITERAL_INT

            return TokenKind.LITERAL_FLOAT

        # capturar o parênteses fechado (1)
        if has_parenthesis:
            expect(TokenKind.RIGHT_PARENTHESIS)

        return left_expression_kind

    def relational_expression():
        """Captura uma expressão relacional."""
        # permitir a comparação entre "int" e "real"
        arithmetic_expression()
        expect(TokenKind.EQUAL, TokenKind.LESS, TokenKind.GREATER,
               TokenKind.LESS_EQUAL, TokenKind.GREATER_EQUAL, TokenKind.NOT_EQUAL)
        arithmetic_expression()
        if peek().kind in [TokenKind.AND, TokenKind.OR]:
            expect(TokenKind.AND, TokenKind.OR)
            relational_expression()

    def command():
        """Captura um comando."""
        command_token = expect(
            TokenKind.ATRIBUIR, TokenKind.LER, TokenKind.IMPRIMIR,
            TokenKind.SE, TokenKind.ENQUANTO, TokenKind.INICIO)

        if command_token.kind == TokenKind.ATRIBUIR:
            expression_kind = arithmetic_expression()
            expect(TokenKind.A)
            var_token = expect(TokenKind.IDENTIFIER)
            expect_variable(var_token.lexeme, expression_kind)
        elif command_token.kind == TokenKind.LER:
            var_token = expect(TokenKind.IDENTIFIER)
            expect_variable(var_token.lexeme)
        elif command_token.kind == TokenKind.IMPRIMIR:
            possible_var_token = expect(TokenKind.IDENTIFIER, TokenKind.LITERAL_STR)
            if possible_var_token.kind == TokenKind.IDENTIFIER:
                expect_variable(possible_var_token.lexeme)
        elif command_token.kind == TokenKind.SE:
            relational_expression()
            expect(TokenKind.ENTAO)
            command()
        elif command_token.kind == TokenKind.ENQUANTO:
            relational_expression()
            command()
        else:  # TokenKind.INICIO_RESERVED_WORD
            # permitir que existam blocos "INICIO FIM" vazios ou com outros blocos "INICIO FIM"
            while peek().kind != TokenKind.FIM:
                command()
            expect(TokenKind.FIM)

    # capturar um programa da linguagem "A"
    expect(TokenKind.DELIMITER)
    expect(TokenKind.DECLARACOES)
    while peek().kind == TokenKind.IDENTIFIER:
        declaration()

    expect(TokenKind.DELIMITER)
    expect(TokenKind.ALGORITMO)
    while peek() is not None:
        command()
