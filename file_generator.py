import os
import random
import threading


class RandomFileCreator:
    def __init__(self, file_count: int, total_words: int, chars: list[str], min_length: int, max_length: int):
        self.file_count = file_count
        self.total_words = total_words
        self.chars = chars
        self.min_length = min_length
        self.max_length = max_length
        self.dict_path = "./output/dictionary"
        self.files_path = "./output/text_files"

    def generate_word(self) -> str:
        length = random.randint(self.min_length, self.max_length)
        return ''.join(random.choice(self.chars) for _ in range(length))

    def create_dictionary(self):
        dict_file_path = os.path.join(self.dict_path, "words.txt")
        with open(dict_file_path, "w") as file:
            words = [self.generate_word() for _ in range(self.total_words)]
            file.write(" ".join(words))

    def split_dictionary(self, index: int, words_per_file: int):
        dict_file_path = os.path.join(self.dict_path, "words.txt")
        output_file_path = os.path.join(self.files_path, f"part{index+1}.txt")

        with open(dict_file_path, "r") as dict_file:
            all_words = dict_file.read().split()

        start_index = index * words_per_file
        end_index = start_index + words_per_file
        selected_words = all_words[start_index:end_index]

        words_per_line = 10
        with open(output_file_path, "w") as output_file:
            for i in range(0, len(selected_words), words_per_line):
                line = ' '.join(selected_words[i:i + words_per_line])
                output_file.write(f"{line}\n")

    def clear_files(self):
        for file_name in os.listdir(self.files_path):
            os.remove(os.path.join(self.files_path, file_name))

    def execute(self):
        os.makedirs(self.dict_path, exist_ok=True)
        os.makedirs(self.files_path, exist_ok=True)

        self.clear_files()
        self.create_dictionary()

        threads = []
        words_per_file = self.total_words // self.file_count
        extra_words = self.total_words % self.file_count

        for i in range(self.file_count):
            words_in_file = words_per_file + (1 if i < extra_words else 0)
            thread = threading.Thread(
                target=self.split_dictionary, args=(i, words_in_file))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()
