from io import TextIOWrapper
import os
import re
import threading


class TextProcessor:
    def __init__(self, regex_pattern: str):
        self.regex_pattern = regex_pattern
        self.dict_dir = "./output/dictionary"
        self.text_dir = "./output/text_files"
        self.map_output_dir = "./output/map_output"
        self.reduce_output_dir = "./output/reduce_output"
        self.lock = threading.Lock()

    def map_function(self, file_path: str, map_file: TextIOWrapper):
        with open(file_path, "r") as file:
            for line in file:
                for word in line.split():
                    with self.lock:
                        map_file.write(f"{word}: [1]\n")

    def reduce_function(self, temp_map_path: str, reduce_file: TextIOWrapper):
        word_count = {}

        with open(temp_map_path, "r") as file:
            for line in file:
                word, count_str = line.split(":")
                count = int(count_str.strip(" []\n"))

                if word in word_count:
                    word_count[word] += count
                else:
                    word_count[word] = count

        sorted_counts = sorted(word_count.items())
        for word, count in sorted_counts:
            reduce_file.write(f"{word}: [{count}]\n")

    def map_grep_function(self, file_path: str, file_name: str, map_file: TextIOWrapper):
        with open(file_path, "r") as file:
            for line in file:
                if self.regex_pattern == "" or re.search(self.regex_pattern, line):
                    with self.lock:
                        map_file.write(f"{file_name} | {line.strip()}\n")

    def reduce_grep_function(self, temp_map_path: str, reduce_file: TextIOWrapper):
        with open(temp_map_path, "r") as file:
            lines = file.readlines()

        lines.sort()
        reduce_file.writelines(lines)

    def execute(self):
        os.makedirs(self.map_output_dir, exist_ok=True)

        temp_map_default_path = os.path.join(
            self.map_output_dir, "default_map_temp.txt")
        temp_map_grep_path = os.path.join(
            self.map_output_dir, "grep_map_temp.txt")

        if os.path.exists(temp_map_default_path):
            os.remove(temp_map_default_path)
        if os.path.exists(temp_map_grep_path):
            os.remove(temp_map_grep_path)

        with open(temp_map_default_path, "a") as default_map_file, \
                open(temp_map_grep_path, "a") as grep_map_file:

            threads = []
            for file_name in os.listdir(self.text_dir):
                if file_name.endswith(".txt"):
                    file_path = os.path.join(self.text_dir, file_name)
                    thread_default = threading.Thread(
                        target=self.map_function, args=(
                            file_path, default_map_file)
                    )
                    thread_grep = threading.Thread(
                        target=self.map_grep_function, args=(
                            file_path, file_name, grep_map_file)
                    )

                    threads.extend([thread_default, thread_grep])

                    thread_default.start()
                    thread_grep.start()

            for thread in threads:
                thread.join()

        os.makedirs(self.reduce_output_dir, exist_ok=True)

        reduced_default_path = os.path.join(
            self.reduce_output_dir, "default_reduced.txt")
        reduced_grep_path = os.path.join(
            self.reduce_output_dir, "grep_reduced.txt")

        with open(reduced_default_path, "w") as reduce_default_file, \
                open(reduced_grep_path, "w") as reduce_grep_file:

            self.reduce_function(temp_map_default_path, reduce_default_file)
            self.reduce_grep_function(temp_map_grep_path, reduce_grep_file)
