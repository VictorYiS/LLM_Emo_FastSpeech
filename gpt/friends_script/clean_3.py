import re

def capitalize_names_in_dialogue(input_file, output_file):
    """
    Read a text file, capitalize character names, and save the modified text to a new file.

    Args:
    - input_file (str): Path to the input text file.
    - output_file (str): Path to the output text file.
    """
    with open(input_file, "r", encoding="utf-8") as file:
        lines = file.readlines()

    updated_lines = []
    for line in lines:
        # Match the pattern "Name: Dialogue"
        match = re.match(r"^(.*?):\s*(.+)$", line)
        if match:
            name, dialogue = match.groups()
            # Capitalize the name
            updated_lines.append(f"{name.upper()}: {dialogue}\n")
        else:
            # If line does not match the pattern, keep it as is
            updated_lines.append(line)

    # Write updated content to the output file
    with open(output_file, "w", encoding="utf-8") as file:
        file.writelines(updated_lines)

# Example usage
input_file = "cleaned_dialogues.txt"  # Input file path
output_file = "cleaned_dialogues_capical.txt"  # Output file path

capitalize_names_in_dialogue(input_file, output_file)

print(f"Processed dialogue saved to {output_file}")