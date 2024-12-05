import os
import re


def clean_dialogue(text):
    """
    Clean text by removing content inside parentheses and brackets.
    """
    # Remove everything in parentheses and brackets
    text = re.sub(r"\(.*?\)|\[.*?\]", "", text)
    # Remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()
    return text


def process_folder(input_folder, output_file):
    """
    Process all text files in the folder, clean the content, and save to one output file.
    """
    cleaned_lines = []

    for filename in os.listdir(input_folder):
        if filename.endswith(".txt"):
            file_path = os.path.join(input_folder, filename)
            with open(file_path, "r", encoding="utf-8") as file:
                lines = file.readlines()

            # Remove the first two lines (title and author)
            lines = lines[2:]

            # Process lines
            for line in lines:
                # Check for new scene marker
                if re.match(r"\[Scene: .*?\]", line):
                    # Add a blank line before new scene
                    if cleaned_lines and cleaned_lines[-1] != "":
                        cleaned_lines.append("")
                # Clean dialogue and add to list
                cleaned_line = clean_dialogue(line)
                if cleaned_line:  # Ignore empty lines
                    cleaned_lines.append(cleaned_line)

    # Save the cleaned content to the output file
    with open(output_file, "w", encoding="utf-8") as output:
        output.write("\n".join(cleaned_lines))


if __name__ == "__main__":
    input_folder = "./ori"  # Replace with the path to your folder
    output_file = "cleaned_dialogues.txt"  # Output file name
    process_folder(input_folder, output_file)
    print(f"Cleaned dialogues saved to {output_file}")