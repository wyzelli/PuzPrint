def load_puzzles(file_path):
    """
    Load puzzles from a file. Each line must contain exactly 81 digits (0-9).
    """
    puzzles = []
    with open(file_path, 'r') as f:
        for line in f:
            clean_line = line.strip().replace(" ", "")[:81]
            if len(clean_line) == 81 and clean_line.isdigit():
                puzzles.append(clean_line)
    return puzzles


def format_rtf(puzzles):
    """
    Format Sudoku puzzles into RTF content with properly defined tables.
    """
    rtf_content = r"{\rtf1\ansi\deff0 {\fonttbl {\f0 Courier;}}"
    cell_width_twips = 1000  # Width of each cell in twips (1 twip = 1/1440 inch)

    for i, puzzle in enumerate(puzzles):
        # Add a title for each puzzle
        rtf_content += f"\\pard\\qc\\b\\fs24 Puzzle {i + 1}\\par\n"
        
        # Start table definition
        for row_idx in range(9):
            rtf_content += "\\trowd\\trgaph10"  # Row properties
            
            # Define cell positions (column widths)
            for col_idx in range(9):
                rtf_content += f"\\cellx{(col_idx + 1) * cell_width_twips}"
            
            # Add cell content
            for col_idx in range(9):
                digit = puzzle[row_idx * 9 + col_idx]
                if digit != "0":
                    rtf_content += f"\\pard\\intbl\\qc\\b {digit}\\cell"
                else:
                    rtf_content += "\\pard\\intbl\\qc \\cell"
            
            # End row
            rtf_content += "\\row\n"
        
        # Add spacing between puzzles
        if i < len(puzzles) - 1:
            rtf_content += "\\pard\\par\n"

    rtf_content += "}"  # Close the RTF document
    return rtf_content


def create_rtf_file(puzzles, output_file):
    """
    Write Sudoku puzzles to an RTF file.
    """
    rtf_content = format_rtf(puzzles)
    with open(output_file, "w") as f:
        f.write(rtf_content)
    print(f"Generated RTF file with {len(puzzles)} puzzles: {output_file}")


if __name__ == "__main__":
    input_file = "puzzles.txt"
    output_file = "sudoku_puzzles.rtf"

    puzzles = load_puzzles(input_file)

    if puzzles:
        create_rtf_file(puzzles, output_file)
    else:
        print("No valid puzzles found in puzzles.txt")
