import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QAction,
    QMenu,
    QToolBar,
    QStatusBar,
    QMessageBox,
    QInputDialog,
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt


class MenuDemo(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set window title and size
        self.setWindowTitle("PyQt Menu Demo")
        self.setGeometry(100, 100, 600, 400)

        # Create status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")

        # Create menubar and menus
        self.create_menus()

        # Create toolbar
        self.create_toolbar()

    def create_menus(self):
        # Create menubar
        menu_bar = self.menuBar()

        # File menu
        file_menu = menu_bar.addMenu("&File")

        # File menu actions
        new_action = QAction("&New", self)
        new_action.setShortcut("Ctrl+N")
        new_action.setStatusTip("Create a new file")
        new_action.triggered.connect(self.new_file)
        file_menu.addAction(new_action)

        open_action = QAction("&Open", self)
        open_action.setShortcut("Ctrl+O")
        open_action.setStatusTip("Open an existing file")
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        save_action = QAction("&Save", self)
        save_action.setShortcut("Ctrl+S")
        save_action.setStatusTip("Save the current file")
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)

        # Add a separator
        file_menu.addSeparator()

        # Exit action
        exit_action = QAction("E&xit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.setStatusTip("Exit the application")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Edit menu
        edit_menu = menu_bar.addMenu("&Edit")

        # Edit menu actions
        cut_action = QAction("Cu&t", self)
        cut_action.setShortcut("Ctrl+X")
        cut_action.triggered.connect(self.cut)
        edit_menu.addAction(cut_action)

        copy_action = QAction("&Copy", self)
        copy_action.setShortcut("Ctrl+C")
        copy_action.triggered.connect(self.copy)
        edit_menu.addAction(copy_action)

        paste_action = QAction("&Paste", self)
        paste_action.setShortcut("Ctrl+V")
        paste_action.triggered.connect(self.paste)
        edit_menu.addAction(paste_action)

        # View menu with submenu
        view_menu = menu_bar.addMenu("&View")

        # Zoom submenu
        zoom_menu = QMenu("&Zoom", self)
        view_menu.addMenu(zoom_menu)

        zoom_in_action = QAction("Zoom &In", self)
        zoom_in_action.setShortcut("Ctrl++")
        zoom_in_action.triggered.connect(self.zoom_in)
        zoom_menu.addAction(zoom_in_action)

        zoom_out_action = QAction("Zoom &Out", self)
        zoom_out_action.setShortcut("Ctrl+-")
        zoom_out_action.triggered.connect(self.zoom_out)
        zoom_menu.addAction(zoom_out_action)

        reset_zoom_action = QAction("&Reset Zoom", self)
        reset_zoom_action.triggered.connect(self.reset_zoom)
        zoom_menu.addAction(reset_zoom_action)

        # Toggle actions
        self.show_toolbar_action = QAction("Show &Toolbar", self)
        self.show_toolbar_action.setCheckable(True)
        self.show_toolbar_action.setChecked(True)
        self.show_toolbar_action.triggered.connect(self.toggle_toolbar)
        view_menu.addAction(self.show_toolbar_action)

        self.show_statusbar_action = QAction("Show &Statusbar", self)
        self.show_statusbar_action.setCheckable(True)
        self.show_statusbar_action.setChecked(True)
        self.show_statusbar_action.triggered.connect(self.toggle_statusbar)
        view_menu.addAction(self.show_statusbar_action)

        # User Input menu
        input_menu = menu_bar.addMenu("&Input")

        text_action = QAction("Text Input", self)
        text_action.triggered.connect(self.get_text_input)
        input_menu.addAction(text_action)

        number_action = QAction("Number Input", self)
        number_action.triggered.connect(self.get_number_input)
        input_menu.addAction(number_action)

        options_action = QAction("Options", self)
        options_action.triggered.connect(self.get_option_input)
        input_menu.addAction(options_action)

        # Help menu
        help_menu = menu_bar.addMenu("&Help")

        about_action = QAction("&About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def create_toolbar(self):
        # Create main toolbar
        self.toolbar = QToolBar("Main Toolbar")
        self.addToolBar(self.toolbar)

        # Add actions to toolbar
        new_action = QAction("New", self)
        new_action.triggered.connect(self.new_file)
        self.toolbar.addAction(new_action)

        open_action = QAction("Open", self)
        open_action.triggered.connect(self.open_file)
        self.toolbar.addAction(open_action)

        save_action = QAction("Save", self)
        save_action.triggered.connect(self.save_file)
        self.toolbar.addAction(save_action)

    # File menu handlers
    def new_file(self):
        print("New file action triggered")
        self.status_bar.showMessage("Created new file", 2000)

    def open_file(self):
        print("Open file action triggered")
        self.status_bar.showMessage("Opened file", 2000)

    def save_file(self):
        print("Save file action triggered")
        self.status_bar.showMessage("File saved", 2000)

    # Edit menu handlers
    def cut(self):
        print("Cut action triggered")
        self.status_bar.showMessage("Cut to clipboard", 2000)

    def copy(self):
        print("Copy action triggered")
        self.status_bar.showMessage("Copied to clipboard", 2000)

    def paste(self):
        print("Paste action triggered")
        self.status_bar.showMessage("Pasted from clipboard", 2000)

    # View menu handlers
    def zoom_in(self):
        print("Zoom in action triggered")
        self.status_bar.showMessage("Zoomed in", 2000)

    def zoom_out(self):
        print("Zoom out action triggered")
        self.status_bar.showMessage("Zoomed out", 2000)

    def reset_zoom(self):
        print("Reset zoom action triggered")
        self.status_bar.showMessage("Zoom reset", 2000)

    def toggle_toolbar(self, checked):
        print(f"Toolbar visibility toggled: {'shown' if checked else 'hidden'}")
        self.toolbar.setVisible(checked)

    def toggle_statusbar(self, checked):
        print(f"Statusbar visibility toggled: {'shown' if checked else 'hidden'}")
        self.status_bar.setVisible(checked)

    # Input menu handlers
    def get_text_input(self):
        text, ok = QInputDialog.getText(self, "Text Input", "Enter some text:")
        if ok:
            print(f"Text input received: {text}")
            self.status_bar.showMessage(f"Text entered: {text}", 2000)

    def get_number_input(self):
        number, ok = QInputDialog.getInt(
            self, "Number Input", "Enter a number:", 0, -100, 100
        )
        if ok:
            print(f"Number input received: {number}")
            self.status_bar.showMessage(f"Number entered: {number}", 2000)

    def get_option_input(self):
        options = ["Option 1", "Option 2", "Option 3", "Option 4"]
        option, ok = QInputDialog.getItem(
            self, "Select Option", "Choose an option:", options, 0, False
        )
        if ok:
            print(f"Option selected: {option}")
            self.status_bar.showMessage(f"Selected: {option}", 2000)

    # Help menu handlers
    def show_about(self):
        print("About dialog opened")
        QMessageBox.about(
            self,
            "About PyQt Menu Demo",
            "This is a simple demo application showing how to create menus in PyQt5.",
        )


def main():
    app = QApplication(sys.argv)
    window = MenuDemo()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
