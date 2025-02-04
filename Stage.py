class Stage:
    def __init__(self, height, width):
        """Initialize the game stage.

        Args:
            height (int): Number of rows in the grid
            width (int): Number of columns in the grid
        """
        self.height = height  # Number of rows
        self.width = width  # Number of columns
        self.current_grid = self.blank_grid()
        self.next_grid = self.blank_grid()

    def blank_grid(self):
        """Create an empty grid with the correct dimensions.

        Returns:
            list: 2D list where first dimension is rows (height)
                 and second dimension is columns (width)
        """
        return [[False for col in range(self.width)] for row in range(self.height)]

    def get_neighbors(self, row, col):
        """Get coordinates of all 8 neighboring cells, with wraparound.

        Args:
            row (int): Row of the current cell
            col (int): Column of the current cell

        Returns:
            list: List of (row, col) tuples for neighboring cells
        """
        return [
            # Top row neighbors
            ((row - 1) % self.height, (col - 1) % self.width),  # Top-left
            ((row - 1) % self.height, col % self.width),  # Top-center
            ((row - 1) % self.height, (col + 1) % self.width),  # Top-right
            # Middle row neighbors
            (row % self.height, (col - 1) % self.width),  # Middle-left
            (row % self.height, (col + 1) % self.width),  # Middle-right
            # Bottom row neighbors
            ((row + 1) % self.height, (col - 1) % self.width),  # Bottom-left
            ((row + 1) % self.height, col % self.width),  # Bottom-center
            ((row + 1) % self.height, (col + 1) % self.width),  # Bottom-right
        ]

    def generate_next_grid(self):
        """Apply Conway's Game of Life rules to generate the next generation."""
        # Check each cell in the grid
        for row in range(self.height):
            for col in range(self.width):
                # Count living neighbors
                living_neighbors = sum(
                    1
                    for neighbor_row, neighbor_col in self.get_neighbors(row, col)
                    if self.current_grid[neighbor_row][neighbor_col]
                )

                # Apply Conway's rules
                current_cell = self.current_grid[row][col]
                if current_cell:
                    # Living cell survives if it has 2 or 3 neighbors
                    self.next_grid[row][col] = living_neighbors in (2, 3)
                else:
                    # Dead cell becomes alive if it has exactly 3 neighbors
                    self.next_grid[row][col] = living_neighbors == 3

        # Update current grid with the new generation
        for row in range(self.height):
            for col in range(self.width):
                self.current_grid[row][col] = self.next_grid[row][col]

        # Reset the next grid
        self.next_grid = self.blank_grid()
