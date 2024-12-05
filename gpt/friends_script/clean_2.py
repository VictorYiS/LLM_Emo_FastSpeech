import os

def clean_file(input_file, output_file):
    """
    Clean a text file by removing lines that contain specific patterns.
    """
    # Patterns to search for and remove
    patterns_to_remove = [
        "Directed by:",
        "Teleplay by:",
        "Story by:",
        "Part 1 written by:",
        "Part 2 written by:",
        "Written by:",
        "Produced by:",
        "Transcribed by:",
        "End"
    ]

    with open(input_file, "r", encoding="utf-8") as file:
        lines = file.readlines()

    cleaned_lines = [
        line for line in lines
        if not any(pattern in line for pattern in patterns_to_remove)
    ]

    with open(output_file, "w", encoding="utf-8") as file:
        file.writelines(cleaned_lines)

if __name__ == "__main__":
    input_file = "cleaned_dialogues.txt"  # Replace with the path to your input file
    output_file = "cleaned_dialogues.txt"  # Replace with the desired output file name
    clean_file(input_file, output_file)
    print(f"Cleaned file saved to {output_file}")