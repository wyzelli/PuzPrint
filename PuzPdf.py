from fpdf import FPDF

# Configuration
CELL_SIZE = 8  # mm per cell
PUZZLE_SIZE = CELL_SIZE * 9
BORDER_WIDTH = 0.8
BOX_LINE_WIDTH = 0.5
CELL_LINE_WIDTH = 0.2
FONT_SIZE = 14  # Font size for bold digits

class SudokuPDF(FPDF):
    def draw_sudoku(self, puzzle_str, x, y):
        """
        Draw a Sudoku puzzle grid with centered digits.
        """
        # Draw outer border
        self.set_line_width(BORDER_WIDTH)
        self.rect(x, y, PUZZLE_SIZE, PUZZLE_SIZE)

        # Draw grid lines
        for i in range(10):
            line_width = BOX_LINE_WIDTH if i % 3 == 0 else CELL_LINE_WIDTH
            self.set_line_width(line_width)

            # Vertical lines
            self.line(
                x + i * CELL_SIZE,
                y,
                x + i * CELL_SIZE,
                y + PUZZLE_SIZE
            )

            # Horizontal lines
            self.line(
                x,
                y + i * CELL_SIZE,
                x + PUZZLE_SIZE,
                y + i * CELL_SIZE
            )

        # Draw numbers with proper centering
        self.set_font("Helvetica", "B", FONT_SIZE)
        for idx, char in enumerate(puzzle_str):
            if char == "0":
                continue  # Skip empty cells
            
            row = idx // 9
            col = idx % 9
            
            # Calculate cell center position
            cell_x = x + col * CELL_SIZE
            cell_y = y + row * CELL_SIZE
            
            # Center text in the cell (adjusting for font metrics)
            text_width = self.get_string_width(char)
            text_x = cell_x + (CELL_SIZE - text_width) / 2
            text_y = cell_y + (CELL_SIZE / 2) + (FONT_SIZE * 0.35 / 2) - 1
            
            self.text(text_x, text_y, char)

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

def create_pdf(puzzles, output_file):
    """
    Generate a PDF with Sudoku puzzles.
    """
    pdf = SudokuPDF()
    pdf.set_auto_page_break(False)

    for i in range(0, len(puzzles), 2):
        pdf.add_page()

        # Calculate positions for vertical centering
        page_width = 210  # A4 width in mm
        page_height = 297  # A4 height in mm
        x_offset = (page_width - PUZZLE_SIZE) / 2

        # First puzzle (top half)
        top_y = (page_height / 2 - PUZZLE_SIZE) / 2
        pdf.draw_sudoku(puzzles[i], x_offset, top_y)

        # Second puzzle (bottom half)
        if i + 1 < len(puzzles):
            bottom_y = page_height / 2 + (page_height / 2 - PUZZLE_SIZE) / 2
            pdf.draw_sudoku(puzzles[i + 1], x_offset, bottom_y)

    pdf.output(output_file)
    print(f"Generated PDF with {len(puzzles)} puzzles: {output_file}")

if __name__ == "__main__":
    puzzles = load_puzzles("puzzles.txt")
    if puzzles:
        create_pdf(puzzles, "sudoku_puzzles.pdf")
    else:
        print("No valid puzzles found in puzzles.txt")
