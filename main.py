import argparse
from pathlib import Path

# CLI
parser = argparse.ArgumentParser(description='''
Analisa o código-fonte da linguagem "A".
''')
parser.add_argument('source_code_path', help='caminho para o arquivo contendo o código-fonte')
args = parser.parse_args()

source_code_path = Path(args.source_code_path)

print(f'Caminho do arquivo: {source_code_path}')
