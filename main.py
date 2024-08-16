from src.sudoku import *

if __name__ == "__main__":
    grid = Sudoku()
    grid.createSudokuGrid("./grids/easy.sudoku")
    grid.solver()
    grid.displaySudokuGrid(grid.sudoku_grid)
