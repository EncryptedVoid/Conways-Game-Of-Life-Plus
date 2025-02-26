# Conway's Game of Life

![Game of Life Demo](https://via.placeholder.com/800x400?text=Game+of+Life+Screenshot)

## Overview

This project is an interactive implementation of Conway's Game of Life using Pygame. Conway's Game of Life is a cellular automaton devised by mathematician John Conway in 1970, simulating the birth and death of cells based on simple rules.

## Features

- **Interactive Grid**: Click to toggle cells between alive and dead states
- **Play/Pause Control**: Start and stop the simulation at any time
- **Wrap-around Grid**: Cells at edges interact with cells on the opposite side
- **Menu System**: Clean interface with settings and game controls
- **Customizable Settings**: Adjust simulation parameters like speed and display options
- **Multiple Button Styles**: Basic buttons and glassmorphic UI elements

## Requirements

- Python 3.6+
- Pygame

```bash
pip install pygame
```

## How to Run

Simply execute the main file:

```bash
python mainv2.py
```

## How to Play

1. **Start the Game**: Launch the application and click "Start Game" from the menu
2. **Create a Pattern**: Click on cells in the grid to toggle them between alive/dead
3. **Run Simulation**: Press the play button to start the simulation
4. **Pause and Edit**: Press the play button again to pause and modify the grid
5. **Adjust Settings**: Access settings from the main menu to customize your experience

## Rules of Conway's Game of Life

1. Any live cell with fewer than two live neighbors dies (underpopulation)
2. Any live cell with two or three live neighbors lives on (survival)
3. Any live cell with more than three live neighbors dies (overpopulation)
4. Any dead cell with exactly three live neighbors becomes alive (reproduction)

## Project Structure

- `Stage.py` - Core game logic for Conway's Game of Life
- `mainv2.py` - Main application with menu system and game loop
- `BuildingBlocks.py` - Basic UI component functions
- `ButtonManager.py` - Button management and interaction
- `glassmorphic_btn.py` - Modern UI button style implementation

## Planned Features

- **Pattern Library**: Save and load common patterns
- **Adjustable Grid Size**: Allow users to choose grid dimensions
- **Simulation Statistics**: Track generations, population counts, and growth rates
- **Multiple Cell Colors**: Support for different cell types or states
- **Export/Import**: Save and share your creations
- **Simulation Speed Control**: Dynamic adjustment of simulation speed while running
- **Drawing Tools**: Line, rectangle, and fill tools for faster pattern creation
- **Rule Editor**: Create and experiment with alternative cellular automaton rules
- **Mobile Support**: Touch-friendly interface for tablet and mobile use
- **Undo/Redo Functionality**: Track grid state history

## Acknowledgments

- John Conway for inventing the Game of Life
- Pygame community for the excellent game development library