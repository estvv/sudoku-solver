from src.logger import *

class Sudoku():
    logger: logging
    sudoku_grid: list[any] = []
    trying_grid: list[dict] = []
    filename: str

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
        self.filename = filename[1:]
        self.sudoku_grid = file.split(' ')

    def gridIsCorrect(self) -> bool:
        res: bool = True
        for i in range(len(self.sudoku_grid)):
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
        i: int = 0
        while i < len(self.sudoku_grid):
            try:
                int(self.sudoku_grid[i])
                i += 1
            except:
                self.sudoku_grid.pop(i)

    def initSudodukoGrid(self) -> None:
        for i in range(len(self.sudoku_grid)):
            self.sudoku_grid[i] = int(self.sudoku_grid[i])
            self.trying_grid.append({1: 'Y', 2: 'Y', 3: 'Y', 4: 'Y', 5: 'Y', 6: 'Y', 7: 'Y', 8: 'Y', 9: 'Y'})

    def createSudokuGrid(self, filename) -> None:
        self.openGrid(filename)
        if not self.gridIsCorrect():
            return
        self.clearGrid()
        self.initSudodukoGrid()
        self.displaySudokuGrid(self.sudoku_grid)

    def displaySudokuGrid(self, grid: list) -> None:
        for i in range(len(grid)):
            if i % 9 == 0 and i != 0:
                print("")
            if i % 27 == 0 and i != 0:
                print("------+-------+------")
            if i % 3 == 0 and i % 9 != 0:
                print(" | ", end="")
            if (i + 1) % 9 == 0 or (i + 1) % 3 == 0:
                print(grid[i], end="")
            else:
                print(grid[i], end=" ")
        print("")

    def solver(self):
        for i in range(5):
            for i in range(len(self.sudoku_grid)):
                if self.sudoku_grid[i] == 0:
                    pass
                self.putAnnotations(self.sudoku_grid[i], i)

            for i in range(len(self.sudoku_grid)):
                if self.sudoku_grid != 0:
                    pass
                self.checkAnnotations(i)

    def putAnnotations(self, num, idx):
        row_lim: tuple[int, int] = (idx - (idx % 9), idx - (idx % 9) + 9)
        col_lim: tuple[int, int] = (idx % 9, (idx % 9) + 73)
        box_start = (idx // 27) * 27 + ((idx % 9) // 3) * 3
        box_lim: tuple[int, int] = (box_start, box_start + 20)

        for i in range(row_lim[0], row_lim[1], 1):
            if self.sudoku_grid[i] == 0:
                self.trying_grid[i][num] = 'N'

        for i in range(col_lim[0], col_lim[1], 9):
            if self.sudoku_grid[i] == 0:
                self.trying_grid[i][num] = 'N'

        for i in range(box_lim[0], box_lim[1], 9):
            for j in range(3):
                if self.sudoku_grid[i + j] == 0:
                    self.trying_grid[i + j][num] = 'N'

    def checkAnnotations(self, idx):
        is_good: list[int] = []
        for num, state in self.trying_grid[idx].items():
            if state == 'Y':
                is_good.append(num)

        if len(is_good) == 1:
            self.sudoku_grid[idx] = is_good[0]
            self.putAnnotations(self.sudoku_grid[idx], idx)

    def writeGrid(self):
        index = self.filename.index(".")
        filename = "." + self.filename[:index] + "_solution" + self.filename[index:]
        filename = filename.replace("puzzles", "solutions")
        try:
            with open(filename, "w") as f:
                for i in range(len(self.sudoku_grid)):
                    if i % 9 == 0 and i != 0:
                        f.write("\n")
                    if i % 27 == 0 and i != 0:
                        f.write("------+-------+------\n")
                    if i % 3 == 0 and i % 9 != 0:
                        f.write(" | ")
                    if (i + 1) % 9 == 0 or (i + 1) % 3 == 0:
                        f.write(f"{self.sudoku_grid[i]}")
                    else:
                        f.write(f"{self.sudoku_grid[i]} ")
        except:
            self.logger.error(f"CAN'T CREATE {filename}")
