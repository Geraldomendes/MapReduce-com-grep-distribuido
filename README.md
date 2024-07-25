## Projeto MapReduce com Grep Distribuído

Este projeto implementa um framework MapReduce para processar e contar a frequência de palavras em arquivos de texto, bem como realizar buscas distribuídas com expressões regulares. O projeto é dividido em dois módulos principais: `RandomFileCreator` e `TextProcessor`.

## Estrutura do Projeto

- **file_generator.py**: Gera arquivos de texto com palavras aleatórias e divide-os em partes.
- **map_reduce.py**: Implementa as funções Map e Reduce para contagem de palavras e grep distribuído.
- **main.py**: Controla a execução do projeto, coordenando a geração de arquivos e o processamento MapReduce.

## Requisitos

- Python 3.x
- Bibliotecas padrão do Python (`os`, `random`, `re`, `threading`)

## Configuração

### Instalação

Clone o repositório e navegue até o diretório do projeto:

```bash
git clone <https://github.com/Geraldomendes/MapReduce-com-grep-distribuido>
cd <DIRETÓRIO_DO_PROJETO>
```

Certifique-se de ter Python 3.x instalado em sua máquina. Este projeto não requer dependências externas além das bibliotecas padrão do Python.

## Uso

### Geração de Arquivos e Processamento MapReduce

Para executar o projeto, você deve fornecer as seguintes informações ao iniciar o programa:

1. **Número de arquivos a serem gerados**: Quantidade de arquivos em que o texto será dividido.
2. **Número total de palavras a serem geradas**: Total de palavras a serem geradas.
3. **Conjunto de caracteres para gerar palavras**: Conjunto de caracteres a ser utilizado.
4. **Comprimento mínimo das palavras**: O comprimento mínimo das palavras geradas.
5. **Comprimento máximo das palavras**: O comprimento máximo das palavras geradas.

Depois de gerar os arquivos, você pode fornecer uma expressão regular para buscar padrões específicos.

#### Executar o Projeto

Execute o programa principal `main.py` para iniciar o processo de geração de arquivos e o processamento MapReduce:

```bash
python main.py
```

### Exemplos de Uso

**Geração de Arquivos**

```bash
$ python main.py
Digite o número de arquivos a serem gerados: 3
Digite o número total de palavras a serem geradas: 100
Digite os caracteres para formar palavras: abcdefghijklmnopqrstuvwxyz
Digite o comprimento mínimo das palavras: 3
Digite o comprimento máximo das palavras: 8
```

**Busca com Expressão Regular**

```bash
$ python main.py
Digite o número de arquivos a serem gerados: 3
Digite o número total de palavras a serem geradas: 100
Digite os caracteres para formar palavras: abcdefghijklmnopqrstuvwxyz
Digite o comprimento mínimo das palavras: 3
Digite o comprimento máximo das palavras: 8
Digite uma expressão regular (ou deixe em branco para ignorar): foo
```

## Detalhes das Funções

### `RandomFileCreator`

- **Construtor**: Recebe parâmetros para configurar a geração e divisão dos arquivos.
- **Métodos**:
  - `generate_word()`: Gera uma palavra aleatória com comprimento entre `min_length` e `max_length`.
  - `create_dictionary()`: Gera um arquivo de texto com palavras aleatórias.
  - `split_dictionary(index, words_per_file)`: Divide o arquivo de palavras em partes e salva em arquivos separados.
  - `clear_files()`: Remove arquivos existentes na pasta de saída.
  - `execute()`: Coordena a geração e divisão dos arquivos.

### `TextProcessor`

- **Construtor**: Recebe um padrão regex para filtragem.
- **Métodos**:
  - `map_function(file_path, map_file)`: Processa o arquivo e escreve pares chave-valor no arquivo temporário.
  - `reduce_function(temp_map_path, reduce_file)`: Agrega contagens de palavras a partir do arquivo temporário.
  - `map_grep_function(file_path, file_name, map_file)`: Busca linhas que correspondem ao padrão regex e escreve no arquivo temporário.
  - `reduce_grep_function(temp_map_path, reduce_file)`: Ordena e escreve as linhas correspondentes no arquivo de saída.
  - `execute()`: Coordena o processo de MapReduce.