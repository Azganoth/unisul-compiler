import argparse
from pathlib import Path

from unisul_compiler.lexer import describe_code

# CLI
parser = argparse.ArgumentParser(description='''
Analisa o código-fonte da linguagem "AL".
''')
parser.add_argument('source_code_path', help='caminho para o arquivo contendo o código-fonte')
args = parser.parse_args()

source_code_path = Path(args.source_code_path)

print(*describe_code(source_code_path), sep='\n')
