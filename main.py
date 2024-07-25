from file_generator import RandomFileCreator
from map_reduce import TextProcessor


def main():
    try:
        file_count = int(
            input("Digite o número de arquivos a serem gerados: "))
        total_words = int(
            input("Digite o número total de palavras a serem geradas: "))
        chars = list(input("Digite os caracteres para formar palavras: "))
        min_length = int(input("Digite o comprimento mínimo das palavras: "))
        max_length = int(input("Digite o comprimento máximo das palavras: "))

        if file_count <= 0 or total_words <= 0 or min_length <= 0 or max_length <= 0:
            raise ValueError("Todos os valores devem ser inteiros positivos.")
        if min_length > max_length:
            raise ValueError(
                "O comprimento mínimo não pode ser maior que o comprimento máximo.")

        generator = RandomFileCreator(
            file_count, total_words, chars, min_length, max_length)
        generator.execute()

        regex = input(
            "Digite uma expressão regular (deixe em branco para não usar filtro): ")

        processor = TextProcessor(regex)
        processor.execute()

    except ValueError as e:
        print(f"Erro de entrada: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")


if __name__ == "__main__":
    main()
