from src.logger import *

class Sudoku():
    logger: logging
    sudoku_grid: list[any] = []
    trying_grid: list[dict] = [{}]

    def __init__(self):
        self.setLogger()
        return

    def setLogger(self):
        self.logger = logging.getLogger("Sudoku Logger")
        self.logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(LoggingFormatter())
        self.logger.addHandler(ch)

    def openGrid(self, filename) -> None:
        file: str = None
        try:
            with open(filename) as my_file:
                file = my_file.read()
                file = file.replace('\n', ' ')
        except:
            file = ""
        self.sudoku_grid = file.split(' ')
        self.sudoku_grid.insert(0, "3x3x3")

    def gridIsCorrect(self) -> bool:
        res: bool = True
        for i in range(1, len(self.sudoku_grid)):
            try:
                if int(self.sudoku_grid[i]) > 9:
                    self.logger.error("BAD GRID")
                    res = False
                elif len(self.sudoku_grid[i]) > 1:
                    self.logger.warning("BAD NUMBER")
                    res = False
            except:
                pass
        if res:
            self.logger.info("GOOD GRID")
        return res

    def clearGrid(self) -> None:
        i: int = 1
        while i < len(self.sudoku_grid):
            try:
                int(self.sudoku_grid[i])
                i += 1
            except:
                self.sudoku_grid.pop(i)

    def initSudodukoGrid(self) -> None:
        for i in range(1, len(self.sudoku_grid)):
            self.sudoku_grid[i] = int(self.sudoku_grid[i])
            self.trying_grid.append({0: 'Y', 1: 'Y', 2: 'Y', 3: 'Y', 4: 'Y', 5: 'Y', 6: 'Y', 7: 'Y', 8: 'Y', 9: 'Y'})

    def createSudokuGrid(self, filename) -> None:
        self.openGrid(filename)
        if not self.gridIsCorrect():
            return
        self.clearGrid()
        self.initSudodukoGrid()
        self.displaySudokuGrid(self.sudoku_grid)

    def displaySudokuGrid(self, grid: list) -> None:
        print(self.sudoku_grid[0])
        for i in range(1, len(grid)):
            print(f"{grid[i]}", end = "")
            if i % 3 == 0 and i % 9 != 0 and i != 0:
                print(" | ", end = "")
            elif i % 27 == 0 and i != len(grid) - 1 and i != 0:
                print("\n------+-------+------")
            elif i % 9 == 0 and i != 0:
                print("")
            else:
                print(" ", end = "")

    def solver(self):
        for i in range(1, len(self.sudoku_grid)):
            if self.sudoku_grid == 0: pass
            self.putAnnotations(0, i - 1)

    def putAnnotations(self, num, idx):
        row_lim: tuple[int, int] = [idx - (idx % 9) + 1, idx + (9 - (idx % 9)) + 1]
        col_lim: tuple[int, int] = [idx % 9 + 1, idx % 9 + 74]

        for i in range(row_lim[0], row_lim[1], 1):
            if self.sudoku_grid[i] == 0:
                self.trying_grid[i][num] = 'N'
                self.sudoku_grid[i] = 9

        for i in range(col_lim[0], col_lim[1], 9):
            if self.sudoku_grid[i] == 0:
                self.trying_grid[i][num] = 'N'
                self.sudoku_grid[i] = 6
