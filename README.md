# unisul-compiler

Compilador para a matéria Tradução de Linguagens de Programação na UNISUL.

## 📘 Especificação da Linguagem "A"

### Elementos léxicos

#### Comentários

Um comentário começa com porcentagem (`%`) e termina com um final de linha.

#### Identificadores

Um identificador pode conter as letras minúsculas e maiúsculas `A` a `Z`, e, exceto pelo primeiro caractere, os dígitos `0` a `9`.

#### Palavras-reservadas

Os seguintes identificadores são usados como palavras reservadas e não podem ser usados como meros identificadores: `DECLARACOES`, `ALGORITMO`, `INTEIRO`, `REAL`, `ATRIBUIR`, `A`, `LER`, `IMPRIMIR`, `SE`, `ENTAO`, `ENQUANTO`, `INICIO` e `FIM`.

#### Cadeias de caracteres

Uma cadeia de caracteres começa e termina com aspas (`'`) e pode conter uma sequência de caracteres. A barra inversa (`\`) trata o próximo caractere de forma especial, por exemplo, uma barra inversa seguida de aspas (`\'`) não termina a cadeia de caracteres.

#### Números Inteiros

Um número inteiro pode começar com sinal de mais (`+`) ou sinal de menos (`-`) seguido por uma sequência de dígitos (`0` a `9`).

#### Números Reais

Um número real pode começar com sinal de mais (`+`) ou sinal de menos (`-`) seguido por duas sequências de dígitos (`0` a `9`) separadas por ponto final (`.`).

#### Operadores Booleanos

Os identificadores `E` e `OU` são usados como operadores booleanos e não podem ser usados como meros identificadores.

#### Operadores Relacionais

Os símbolos sinal de igual (`=`), chevron aberto (`<`), chevron fechado (`>`), chevron aberto e sinal de igual (`<=`), chevron fechado e sinal de igual (`>=`) e chevron aberto e chevron fechado (`<>`) são usados como operadores relacionais.

#### Operadores Aritméticos

Os símbolos sinal de mais (`+`), sinal de menos (`-`), asteristico (`*`) e barra (`/`) são usados como operadores aritméticos.

#### Parênteses

Os símbolos parêntese aberto (`(`) e parêntese fechado (`)`) são usados como parênteses.

#### Delimitadores

Um delimitador é definido por dois-pontos (`:`).

## 🚀 Como usar

**Requerimentos:**

-   Python 3.8

Criar um ambiente virtual:

```sh
python -m venv venv
```

Carregar as variáveis de ambiente:

```sh
# bash
venv/Scripts/activate

# cmd
venv\Scripts\activate.bat

# powershell
venv/Scripts/Activate.ps1
```

Instalar as dependências do projeto:

```sh
pip install -r requirements.txt
```

Executar o programa:

```sh
python main.py caminho_do_arquivo
```

## 🔑 Licença

Este projeto está sob a [licença MIT](LICENSE.md).
