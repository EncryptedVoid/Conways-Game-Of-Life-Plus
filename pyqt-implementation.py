import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QPushButton
from PyQt5.QtCore import QTimer, Qt


class GameOfLife(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Conway's Game of Life")
        self.rows, self.cols = 20, 20
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.buttons = [[None for _ in range(self.cols)] for _ in range(self.rows)]

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.layout = QGridLayout(central_widget)

        # Create grid of buttons
        for i in range(self.rows):
            for j in range(self.cols):
                button = QPushButton()
                button.setFixedSize(20, 20)
                button.setCheckable(True)
                button.clicked.connect(lambda state, x=i, y=j: self.toggle_cell(x, y))
                self.layout.addWidget(button, i, j)
                self.buttons[i][j] = button

        # Create timer for evolution
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.evolve)

        # Create control buttons
        self.setup_controls()

        self.update_display()

    def toggle_cell(self, x, y):
        self.grid[x][y] = 1 - self.grid[x][y]  # Toggle between 0 and 1
        self.update_display()

    def update_display(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.buttons[i][j].setStyleSheet(
                    "background-color: black;"
                    if self.grid[i][j]
                    else "background-color: white;"
                )

    def evolve(self):
        # Conway's Game of Life rules implementation
        new_grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

        for i in range(self.rows):
            for j in range(self.cols):
                # Count live neighbors
                neighbors = 0
                for di in [-1, 0, 1]:
                    for dj in [-1, 0, 1]:
                        if di == 0 and dj == 0:
                            continue
                        ni, nj = (i + di) % self.rows, (j + dj) % self.cols
                        neighbors += self.grid[ni][nj]

                # Apply Conway's rules
                if self.grid[i][j] == 1 and (neighbors == 2 or neighbors == 3):
                    new_grid[i][j] = 1
                elif self.grid[i][j] == 0 and neighbors == 3:
                    new_grid[i][j] = 1

        self.grid = new_grid
        self.update_display()

    def setup_controls(self):
        # Add start/stop/clear buttons
        # (implementation details omitted for brevity)
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GameOfLife()
    window.show()
    sys.exit(app.exec_())
