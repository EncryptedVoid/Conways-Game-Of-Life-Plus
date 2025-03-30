import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QGridLayout,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QSpinBox,
    QSlider,
)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QColor


class GameOfLife(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set window properties
        self.setWindowTitle("Conway's Game of Life")
        self.setGeometry(100, 100, 800, 600)

        # Game configuration
        self.rows, self.cols = 30, 30
        self.cell_size = 20
        self.is_playing = False

        # Grid state
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.buttons = [[None for _ in range(self.cols)] for _ in range(self.rows)]

        # Setup the GUI
        self.setup_ui()

        # Setup timer for animation
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.evolve)
        self.update_interval = 200  # milliseconds

    def setup_ui(self):
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QVBoxLayout(central_widget)

        # Control panel
        control_panel = QWidget()
        control_layout = QHBoxLayout(control_panel)

        # Play/Pause button
        self.play_button = QPushButton("Play")
        self.play_button.clicked.connect(self.toggle_play)
        control_layout.addWidget(self.play_button)

        # Step button (for single step evolution)
        step_button = QPushButton("Step")
        step_button.clicked.connect(self.evolve)
        control_layout.addWidget(step_button)

        # Clear button
        clear_button = QPushButton("Clear")
        clear_button.clicked.connect(self.clear_grid)
        control_layout.addWidget(clear_button)

        # Random button
        random_button = QPushButton("Random")
        random_button.clicked.connect(self.random_grid)
        control_layout.addWidget(random_button)

        # Glider button
        glider_button = QPushButton("Add Glider")
        glider_button.clicked.connect(self.add_glider)
        control_layout.addWidget(glider_button)

        # Speed control
        speed_label = QLabel("Speed:")
        control_layout.addWidget(speed_label)

        speed_slider = QSlider(Qt.Horizontal)
        speed_slider.setMinimum(50)
        speed_slider.setMaximum(500)
        speed_slider.setValue(200)
        speed_slider.setTickInterval(50)
        speed_slider.setTickPosition(QSlider.TicksBelow)
        speed_slider.valueChanged.connect(self.set_speed)
        control_layout.addWidget(speed_slider)

        # Generation counter
        self.gen_counter = QLabel("Generation: 0")
        control_layout.addWidget(self.gen_counter)

        main_layout.addWidget(control_panel)

        # Game grid
        grid_widget = QWidget()
        self.grid_layout = QGridLayout(grid_widget)
        self.grid_layout.setSpacing(1)

        # Create cell buttons
        for i in range(self.rows):
            for j in range(self.cols):
                button = QPushButton()
                button.setFixedSize(self.cell_size, self.cell_size)
                button.setStyleSheet("background-color: white;")
                button.setCheckable(True)
                button.clicked.connect(
                    lambda checked, row=i, col=j: self.toggle_cell(row, col)
                )
                self.grid_layout.addWidget(button, i, j)
                self.buttons[i][j] = button

        main_layout.addWidget(grid_widget)

        # Status bar
        self.statusBar().showMessage(
            "Ready - Click cells to set initial state, then press Play"
        )

        # Initialize generation counter
        self.generation = 0

    def toggle_cell(self, row, col):
        """Toggle cell state when clicked"""
        self.grid[row][col] = 1 - self.grid[row][col]
        self.update_button_color(row, col)

    def update_button_color(self, row, col):
        """Update button color based on cell state"""
        if self.grid[row][col] == 1:
            self.buttons[row][col].setStyleSheet("background-color: black;")
        else:
            self.buttons[row][col].setStyleSheet("background-color: white;")

    def update_grid_display(self):
        """Update all buttons to reflect current grid state"""
        for i in range(self.rows):
            for j in range(self.cols):
                self.update_button_color(i, j)

    def toggle_play(self):
        """Toggle between playing and paused states"""
        self.is_playing = not self.is_playing

        if self.is_playing:
            self.play_button.setText("Pause")
            self.timer.start(self.update_interval)
            self.statusBar().showMessage("Simulation running")
        else:
            self.play_button.setText("Play")
            self.timer.stop()
            self.statusBar().showMessage("Simulation paused")

    def evolve(self):
        """Evolve the grid according to Conway's Game of Life rules"""
        # Create a new grid
        new_grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

        # Apply Conway's rules
        for i in range(self.rows):
            for j in range(self.cols):
                # Count live neighbors
                neighbors = self.count_neighbors(i, j)

                # Apply rules
                if self.grid[i][j] == 1:
                    # Live cell
                    if neighbors < 2 or neighbors > 3:
                        # Dies (underpopulation or overpopulation)
                        new_grid[i][j] = 0
                    else:
                        # Survives
                        new_grid[i][j] = 1
                else:
                    # Dead cell
                    if neighbors == 3:
                        # Becomes alive (reproduction)
                        new_grid[i][j] = 1

        # Update grid
        self.grid = new_grid
        self.update_grid_display()

        # Update generation counter
        self.generation += 1
        self.gen_counter.setText(f"Generation: {self.generation}")

    def count_neighbors(self, row, col):
        """Count the number of live neighbors for a cell"""
        count = 0

        # Check all 8 neighboring cells
        for i in range(max(0, row - 1), min(self.rows, row + 2)):
            for j in range(max(0, col - 1), min(self.cols, col + 2)):
                # Skip the cell itself
                if i == row and j == col:
                    continue

                # Add to count if neighbor is alive
                count += self.grid[i][j]

        return count

    def clear_grid(self):
        """Clear the grid (set all cells to dead)"""
        for i in range(self.rows):
            for j in range(self.cols):
                self.grid[i][j] = 0

        self.update_grid_display()
        self.generation = 0
        self.gen_counter.setText("Generation: 0")
        self.statusBar().showMessage("Grid cleared")

    def random_grid(self):
        """Fill the grid with random cell states"""
        import random

        for i in range(self.rows):
            for j in range(self.cols):
                self.grid[i][j] = 1 if random.random() < 0.3 else 0

        self.update_grid_display()
        self.generation = 0
        self.gen_counter.setText("Generation: 0")
        self.statusBar().showMessage("Random grid generated")

    def add_glider(self):
        """Add a glider pattern at the center of the grid"""
        # Find center position
        center_row = self.rows // 2
        center_col = self.cols // 2

        # Glider pattern
        glider = [[0, 1, 0], [0, 0, 1], [1, 1, 1]]

        # Add pattern to grid
        for i in range(3):
            for j in range(3):
                row = (center_row - 1 + i) % self.rows
                col = (center_col - 1 + j) % self.cols
                self.grid[row][col] = glider[i][j]

        self.update_grid_display()
        self.statusBar().showMessage("Glider added")

    def set_speed(self, value):
        """Set the animation speed"""
        self.update_interval = 550 - value  # Invert so higher value = faster

        if self.is_playing:
            self.timer.stop()
            self.timer.start(self.update_interval)

        self.statusBar().showMessage(f"Speed set to {value}")


def main():
    app = QApplication(sys.argv)
    window = GameOfLife()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
