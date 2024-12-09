import os
import re


def clean_text_in_files(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()

            cleaned_lines = []
            for line in lines:
                if re.search('[a-zA-Z]', line):
                    matches = re.findall(r'"(.*?)"', line)
                    if matches:
                        cleaned_lines.append('.'.join(matches))

            with open(file_path, 'w', encoding='utf-8') as file:
                file.write('\n'.join(cleaned_lines))


# Example usage
clean_text_in_files('disco_elysium')