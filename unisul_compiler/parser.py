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
        token_kinds_repr = " | ".join(map(lambda token_kind: token_kind.name, token_kinds))

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
    symbols: Dict[str, Literal[TokenKind.INTEGER, TokenKind.FLOAT]] = {}

    def expect_variable(
            var_name: str, var_type: Optional[Literal[TokenKind.INTEGER, TokenKind.FLOAT]] = None):
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
                f'erro semântico, {symbol_kind.name}, tipo da variável "{var_name}", '
                f'não satisfaz {var_type.name}')

        return symbol_kind

    # Padrões da linguagem "A"
    def declaration():
        """Captura uma declaração."""
        name_token = expect(TokenKind.IDENTIFIER)
        expect(TokenKind.DELIMITER)
        type_token = expect(TokenKind.INT_RESERVED_WORD, TokenKind.REAL_RESERVED_WORD)

        # adicionar a variável ao dicionário de símbolos
        if (var_name := name_token.lexeme) not in symbols:
            symbols[var_name] = (TokenKind.INTEGER
                                 if type_token.kind == TokenKind.INT_RESERVED_WORD else
                                 TokenKind.FLOAT)
        else:
            raise ASemanticError(f'erro semântico, variável "{var_name}" já foi declarada')

    def arithmetic_expression() -> Literal[TokenKind.INTEGER, TokenKind.FLOAT]:
        """Captura uma expressão aritmética.

        Returns:
            O tipo da expressão aritmética encontrada.
        """
        left_expression = expect(TokenKind.INTEGER, TokenKind.FLOAT, TokenKind.IDENTIFIER,
                                 TokenKind.OPEN_PARENTHESIS)

        # resolver uma expressão aritmética ao reconhecer um parênteses aberto
        if (has_parenthesis := (left_expression_kind := left_expression.kind) == TokenKind.OPEN_PARENTHESIS):
            left_expression_kind = arithmetic_expression()

        # certificar que a variável foi declarada e resgatar seu tipo, caso seja uma variável...
        if left_expression_kind == TokenKind.IDENTIFIER:
            left_expression_kind = expect_variable(left_expression.lexeme)

        if peek().kind in [
                TokenKind.ADDITION_ARITHMETIC_OPERATOR,
                TokenKind.SUBTRACTION_ARITHMETIC_OPERATOR,
                TokenKind.MULTIPLICATION_ARITHMETIC_OPERATOR,
                TokenKind.DIVISION_ARITHMETIC_OPERATOR]:
            operator = expect(
                TokenKind.ADDITION_ARITHMETIC_OPERATOR,
                TokenKind.SUBTRACTION_ARITHMETIC_OPERATOR,
                TokenKind.MULTIPLICATION_ARITHMETIC_OPERATOR,
                TokenKind.DIVISION_ARITHMETIC_OPERATOR)
            right_expression_kind = arithmetic_expression()

            # capturar o parênteses fechado (2)
            if has_parenthesis:
                expect(TokenKind.CLOSE_PARENTHESIS)

            # resolver em "inteiro" caso as duas expressões aritméticas resultarem
            # em números inteiros e o operador for adição, subtração ou multiplicação,
            # caso contrário resultar em "real"
            if (left_expression_kind == TokenKind.INTEGER
                and right_expression_kind == TokenKind.INTEGER
                and operator.kind in [
                    TokenKind.ADDITION_ARITHMETIC_OPERATOR,
                    TokenKind.SUBTRACTION_ARITHMETIC_OPERATOR,
                    TokenKind.MULTIPLICATION_ARITHMETIC_OPERATOR]):
                return TokenKind.INTEGER

            return TokenKind.FLOAT

        # capturar o parênteses fechado (1)
        if has_parenthesis:
            expect(TokenKind.CLOSE_PARENTHESIS)

        return left_expression_kind

    def relational_expression():
        """Captura uma expressão relacional."""
        # permitir a comparação entre "int" e "real"
        arithmetic_expression()
        expect(TokenKind.EQUAL_RELATIONAL_OPERATOR, TokenKind.LESS_RELATIONAL_OPERATOR,
               TokenKind.GREATER_RELATIONAL_OPERATOR, TokenKind.LESS_EQUAL_RELATIONAL_OPERATOR,
               TokenKind.GREATER_EQUAL_RELATIONAL_OPERATOR, TokenKind.EQUIVALENT_RELATIONAL_OPERATOR)
        arithmetic_expression()
        if peek().kind in [TokenKind.AND_BOOLEAN_OPERATOR, TokenKind.OR_BOOLEAN_OPERATOR]:
            expect(TokenKind.AND_BOOLEAN_OPERATOR, TokenKind.OR_BOOLEAN_OPERATOR)
            relational_expression()

    def command():
        """Captura um comando."""
        command_token = expect(
            TokenKind.ATRIBUIR_RESERVED_WORD, TokenKind.LER_RESERVED_WORD,
            TokenKind.IMPRIMIR_RESERVED_WORD, TokenKind.SE_RESERVED_WORD,
            TokenKind.ENQUANTO_RESERVED_WORD, TokenKind.INICIO_RESERVED_WORD)

        if command_token.kind == TokenKind.ATRIBUIR_RESERVED_WORD:
            expression_kind = arithmetic_expression()
            expect(TokenKind.A_RESERVED_WORD)
            var_token = expect(TokenKind.IDENTIFIER)
            print(expression_kind)
            expect_variable(var_token.lexeme, expression_kind)
        elif command_token.kind == TokenKind.LER_RESERVED_WORD:
            var_token = expect(TokenKind.IDENTIFIER)
            expect_variable(var_token.lexeme)
        elif command_token.kind == TokenKind.IMPRIMIR_RESERVED_WORD:
            possible_var_token = expect(TokenKind.IDENTIFIER, TokenKind.STRING)
            if possible_var_token.kind == TokenKind.IDENTIFIER:
                expect_variable(possible_var_token.lexeme)
        elif command_token.kind == TokenKind.SE_RESERVED_WORD:
            relational_expression()
            expect(TokenKind.ENTAO_RESERVED_WORD)
            command()
        elif command_token.kind == TokenKind.ENQUANTO_RESERVED_WORD:
            relational_expression()
            command()
        else:  # TokenKind.INICIO_RESERVED_WORD
            # permitir que existam blocos "INICIO FIM" vazios ou com outros blocos "INICIO FIM"
            while peek().kind != TokenKind.FIM_RESERVED_WORD:
                command()
            expect(TokenKind.FIM_RESERVED_WORD)

    # capturar um programa da linguagem "A"
    expect(TokenKind.DELIMITER)
    expect(TokenKind.DECLARACOES_RESERVED_WORD)
    while peek().kind == TokenKind.IDENTIFIER:
        declaration()

    expect(TokenKind.DELIMITER)
    expect(TokenKind.ALGORITMO_RESERVED_WORD)
    while peek() is not None:
        command()
