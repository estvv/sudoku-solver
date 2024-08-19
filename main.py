from src.sudoku import *

if __name__ == "__main__":
    grid = Sudoku()
    grid.createSudokuGrid("./grids/puzzles/easy.sudoku")
    grid.solver()
    grid.writeGrid()
