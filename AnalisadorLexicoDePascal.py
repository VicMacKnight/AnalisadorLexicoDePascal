import re

pascal_file_path = 'example.pas'

def read_pascal_file(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        print(f"Arquivo '{file_path}' não encontrado.")
    except Exception as e:
        print(f"Erro ao ler o arquivo '{file_path}': {str(e)}")

source_code = read_pascal_file(pascal_file_path)

if source_code:
    print(f"Conteúdo do arquivo '{pascal_file_path}':\n")
    print(pascal_content)

# Classe para representar um token
class Token:
    def __init__(self, code, lexeme):
        self.code = code
        self.lexeme = lexeme

# Classe para o analisador léxico
class Lexer:
    def __init__(self, source_code):
        self.source_code = source_code
        self.current_pos = 0
        self.tokens = []
        self.symbol_table = {}

    # Função para obter o próximo token
    def get_next_token(self):
        # Verifica se chegou ao final do código fonte
        if self.current_pos >= len(self.source_code):
            return None

        # Ignora espaços em branco e quebras de linha
        while self.current_pos < len(self.source_code) and self.source_code[self.current_pos].isspace():
            self.current_pos += 1

        # Verifica se é um identificador
        identifier_regex = r'^[a-zA-Z][a-zA-Z0-9]*$'
        match = re.match(identifier_regex, self.source_code[self.current_pos:])
        if match:
            lexeme = match.group()
            self.current_pos += len(lexeme)
            token_code = self.symbol_table.get(lexeme)
            if not token_code:
                token_code = len(self.symbol_table) + 1
                self.symbol_table[lexeme] = token_code
            return Token(token_code, lexeme)

        # Verifica se é um número inteiro
        integer_regex = r'^\d+'
        match = re.match(integer_regex, self.source_code[self.current_pos:])
        if match:
            lexeme = match.group()
            self.current_pos += len(lexeme)
            return Token(0, int(lexeme))  # Código 0 para números

        # Verifica se é um símbolo especial
        special_symbols = ['+', ';', ':', '=', ':=']
        for symbol in special_symbols:
            if self.source_code.startswith(symbol, self.current_pos):
                self.current_pos += len(symbol)
                return Token(symbol, symbol)

        # Se não é nenhum dos casos acima, gera um erro léxico
        raise Exception(f"Erro léxico: caractere inválido '{self.source_code[self.current_pos]}'")

    # Função para realizar a análise léxica completa
    def tokenize(self):
        token = self.get_next_token()
        while token:
            self.tokens.append(token)
            token = self.get_next_token()

        return self.tokens

lexer = Lexer(source_code)
tokens = lexer.tokenize()

# Imprime a tabela de símbolos
print("Tabela de símbolos:")
for lexeme, code in lexer.symbol_table.items():
    print(f"{lexeme} -> {code}")

# Imprime os tokens encontrados
print("\nTokens:")
for token in tokens:
    if isinstance(token.lexeme, int):
        print(f"({token.code}, {token.lexeme})")
    else:
        print(f"({token.code}, '{token.lexeme}')")