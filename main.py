import argparse
from pathlib import Path

from unisul_compiler.lexer import describe

# CLI
parser = argparse.ArgumentParser(description='''
Compilador da linguagem "A" (sem geração de código, apenas relatório).
''')
parser.add_argument('source_file_path', help='caminho para o arquivo de texto (código-fonte)')
args = parser.parse_args()

source_file_path = Path(args.source_file_path)

print(f'Analisando o arquivo "{source_file_path}"...')

with open(source_file_path) as source_file:
    print('\nAnálise léxica:')
    tokens = describe(source_file.read())
