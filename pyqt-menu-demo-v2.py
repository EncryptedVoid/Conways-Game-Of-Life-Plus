import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QStackedWidget,
    QComboBox,
    QLineEdit,
    QSpinBox,
    QCheckBox,
    QRadioButton,
    QButtonGroup,
    QMenu,
    QAction,
    QMessageBox,
    QStatusBar,
    QToolBar,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QGroupBox,
)
from PyQt5.QtCore import Qt, QSettings
from PyQt5.QtGui import QIcon


class SettingsDialog(QDialog):
    def __init__(self, settings, parent=None):
        super().__init__(parent)
        self.settings = settings
        self.setWindowTitle("Settings")
        self.resize(300, 200)

        # Create layout
        layout = QVBoxLayout()

        # General settings group
        general_group = QGroupBox("General")
        general_layout = QFormLayout()

        # Username
        self.username_input = QLineEdit()
        current_username = self.settings.value("username", "")
        self.username_input.setText(current_username)
        general_layout.addRow("Username:", self.username_input)

        # Theme selection
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Light", "Dark", "System"])
        current_theme = self.settings.value("theme", "Light")
        self.theme_combo.setCurrentText(current_theme)
        general_layout.addRow("Theme:", self.theme_combo)

        general_group.setLayout(general_layout)
        layout.addWidget(general_group)

        # Notification settings group
        notif_group = QGroupBox("Notifications")
        notif_layout = QVBoxLayout()

        # Enable notifications
        self.enable_notif = QCheckBox("Enable Notifications")
        self.enable_notif.setChecked(
            self.settings.value("notifications_enabled", True, type=bool)
        )
        notif_layout.addWidget(self.enable_notif)

        # Sound notifications
        self.sound_notif = QCheckBox("Enable Sound")
        self.sound_notif.setChecked(
            self.settings.value("sound_enabled", True, type=bool)
        )
        notif_layout.addWidget(self.sound_notif)

        notif_group.setLayout(notif_layout)
        layout.addWidget(notif_group)

        # Dialog buttons
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.setLayout(layout)

    def accept(self):
        # Save settings
        self.settings.setValue("username", self.username_input.text())
        self.settings.setValue("theme", self.theme_combo.currentText())
        self.settings.setValue("notifications_enabled", self.enable_notif.isChecked())
        self.settings.setValue("sound_enabled", self.sound_notif.isChecked())

        print("Settings saved:")
        print(f"Username: {self.username_input.text()}")
        print(f"Theme: {self.theme_combo.currentText()}")
        print(f"Notifications: {self.enable_notif.isChecked()}")
        print(f"Sound: {self.sound_notif.isChecked()}")

        super().accept()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt App Flow Demo")
        self.resize(800, 600)

        # Initialize settings
        self.settings = QSettings("PyQtDemo", "AppFlowDemo")

        # Setup UI
        self.setup_ui()

        # Create status bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Ready")

        # Initialize application state
        self.initialize_state()

    def setup_ui(self):
        # Create central widget and stacked layout to manage "screens"
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        main_layout = QVBoxLayout(self.central_widget)

        # Create stacked widget for different screens
        self.stacked_widget = QStackedWidget()

        # Create screens
        self.create_home_screen()
        self.create_products_screen()
        self.create_settings_screen()
        self.create_profile_screen()

        main_layout.addWidget(self.stacked_widget)

        # Create menus
        self.create_menus()

        # Create toolbar
        self.create_toolbar()

    def create_menus(self):
        # Main menu bar
        menu_bar = self.menuBar()

        # File menu
        file_menu = menu_bar.addMenu("&File")

        # Home action
        home_action = QAction("&Home", self)
        home_action.setShortcut("Ctrl+H")
        home_action.triggered.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        file_menu.addAction(home_action)

        # Products action - with submenu
        products_menu = QMenu("&Products", self)
        file_menu.addMenu(products_menu)

        view_products_action = QAction("&View Products", self)
        view_products_action.triggered.connect(
            lambda: self.stacked_widget.setCurrentIndex(1)
        )
        products_menu.addAction(view_products_action)

        add_product_action = QAction("&Add New Product", self)
        add_product_action.triggered.connect(self.add_new_product)
        products_menu.addAction(add_product_action)

        # Separator
        file_menu.addSeparator()

        # Exit action
        exit_action = QAction("E&xit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # View menu
        view_menu = menu_bar.addMenu("&View")

        # Toggle toolbar action
        self.show_toolbar_action = QAction("Show &Toolbar", self)
        self.show_toolbar_action.setCheckable(True)
        self.show_toolbar_action.setChecked(True)
        self.show_toolbar_action.triggered.connect(self.toggle_toolbar)
        view_menu.addAction(self.show_toolbar_action)

        # Tools menu
        tools_menu = menu_bar.addMenu("&Tools")

        # Settings action
        settings_action = QAction("&Settings", self)
        settings_action.triggered.connect(self.show_settings_dialog)
        tools_menu.addAction(settings_action)

        # Profile action
        profile_action = QAction("&Profile", self)
        profile_action.triggered.connect(lambda: self.stacked_widget.setCurrentIndex(3))
        tools_menu.addAction(profile_action)

        # Help menu with dynamic content
        self.help_menu = menu_bar.addMenu("&Help")

        # About action
        about_action = QAction("&About", self)
        about_action.triggered.connect(self.show_about)
        self.help_menu.addAction(about_action)

        # Context-sensitive help - this menu will change based on current screen
        self.context_help_action = QAction("Context Help", self)
        self.context_help_action.triggered.connect(self.show_context_help)
        self.help_menu.addAction(self.context_help_action)

    def create_toolbar(self):
        # Main toolbar
        self.toolbar = QToolBar("Navigation")
        self.addToolBar(self.toolbar)

        # Add navigation buttons
        home_btn = QPushButton("Home")
        home_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        self.toolbar.addWidget(home_btn)

        products_btn = QPushButton("Products")
        products_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        self.toolbar.addWidget(products_btn)

        settings_btn = QPushButton("Settings")
        settings_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        self.toolbar.addWidget(settings_btn)

        profile_btn = QPushButton("Profile")
        profile_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(3))
        self.toolbar.addWidget(profile_btn)

    def toggle_toolbar(self, checked):
        self.toolbar.setVisible(checked)
        print(f"Toolbar visibility: {'shown' if checked else 'hidden'}")

    def create_home_screen(self):
        home_widget = QWidget()
        layout = QVBoxLayout(home_widget)

        # Welcome message
        welcome_label = QLabel("Welcome to the App Flow Demo")
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setStyleSheet("font-size: 24px; margin: 20px;")
        layout.addWidget(welcome_label)

        # Navigation buttons
        button_layout = QHBoxLayout()

        products_btn = QPushButton("Browse Products")
        products_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        button_layout.addWidget(products_btn)

        settings_btn = QPushButton("Settings")
        settings_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        button_layout.addWidget(settings_btn)

        profile_btn = QPushButton("My Profile")
        profile_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(3))
        button_layout.addWidget(profile_btn)

        layout.addLayout(button_layout)

        # Add to stacked widget
        self.stacked_widget.addWidget(home_widget)

    def create_products_screen(self):
        products_widget = QWidget()
        layout = QVBoxLayout(products_widget)

        # Header
        header = QLabel("Products")
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("font-size: 20px; margin: 10px;")
        layout.addWidget(header)

        # Product selection
        self.product_combo = QComboBox()
        self.product_combo.addItems(
            ["Product A - $10.99", "Product B - $24.99", "Product C - $5.99"]
        )
        self.product_combo.currentIndexChanged.connect(self.update_product_info)
        layout.addWidget(self.product_combo)

        # Product info
        self.product_info = QLabel("Select a product to see details")
        self.product_info.setAlignment(Qt.AlignCenter)
        self.product_info.setStyleSheet("font-style: italic;")
        layout.addWidget(self.product_info)

        # Add to cart button with counter
        cart_layout = QHBoxLayout()

        self.quantity_spinner = QSpinBox()
        self.quantity_spinner.setMinimum(1)
        self.quantity_spinner.setMaximum(10)
        cart_layout.addWidget(QLabel("Quantity:"))
        cart_layout.addWidget(self.quantity_spinner)

        add_to_cart_btn = QPushButton("Add to Cart")
        add_to_cart_btn.clicked.connect(self.add_to_cart)
        cart_layout.addWidget(add_to_cart_btn)

        layout.addLayout(cart_layout)

        # Navigation
        back_btn = QPushButton("Back to Home")
        back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        layout.addWidget(back_btn)

        # Add to stacked widget
        self.stacked_widget.addWidget(products_widget)

    def create_settings_screen(self):
        settings_widget = QWidget()
        layout = QVBoxLayout(settings_widget)

        # Header
        header = QLabel("Settings")
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("font-size: 20px; margin: 10px;")
        layout.addWidget(header)

        # Settings form
        form_layout = QFormLayout()

        # Username
        self.username_input = QLineEdit()
        form_layout.addRow("Username:", self.username_input)

        # Theme selection
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Light", "Dark", "System"])
        form_layout.addRow("Theme:", self.theme_combo)

        # Notification options
        notif_layout = QVBoxLayout()
        self.enable_notif = QCheckBox("Enable Notifications")
        notif_layout.addWidget(self.enable_notif)

        self.sound_notif = QCheckBox("Enable Sound")
        notif_layout.addWidget(self.sound_notif)

        # Add the notification layout to the form
        notif_group = QGroupBox("Notification Settings")
        notif_group.setLayout(notif_layout)
        form_layout.addRow(notif_group)

        layout.addLayout(form_layout)

        # Buttons
        button_layout = QHBoxLayout()

        save_btn = QPushButton("Save Settings")
        save_btn.clicked.connect(self.save_settings)
        button_layout.addWidget(save_btn)

        reset_btn = QPushButton("Reset to Defaults")
        reset_btn.clicked.connect(self.reset_settings)
        button_layout.addWidget(reset_btn)

        layout.addLayout(button_layout)

        # Navigation
        back_btn = QPushButton("Back to Home")
        back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        layout.addWidget(back_btn)

        # Add to stacked widget
        self.stacked_widget.addWidget(settings_widget)

    def create_profile_screen(self):
        profile_widget = QWidget()
        layout = QVBoxLayout(profile_widget)

        # Header
        header = QLabel("User Profile")
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("font-size: 20px; margin: 10px;")
        layout.addWidget(header)

        # Username display
        self.profile_username = QLabel("Username: Not Set")
        layout.addWidget(self.profile_username)

        # Stats
        stats_layout = QVBoxLayout()
        self.cart_count = QLabel("Items in cart: 0")
        stats_layout.addWidget(self.cart_count)

        self.last_product = QLabel("Last viewed product: None")
        stats_layout.addWidget(self.last_product)

        stats_group = QGroupBox("User Stats")
        stats_group.setLayout(stats_layout)
        layout.addWidget(stats_group)

        # Subscription options (radio buttons that save state)
        sub_layout = QVBoxLayout()

        self.sub_group = QButtonGroup(self)

        self.sub_free = QRadioButton("Free Plan")
        self.sub_group.addButton(self.sub_free, 1)
        sub_layout.addWidget(self.sub_free)

        self.sub_premium = QRadioButton("Premium Plan")
        self.sub_group.addButton(self.sub_premium, 2)
        sub_layout.addWidget(self.sub_premium)

        self.sub_enterprise = QRadioButton("Enterprise Plan")
        self.sub_group.addButton(self.sub_enterprise, 3)
        sub_layout.addWidget(self.sub_enterprise)

        sub_group = QGroupBox("Subscription")
        sub_group.setLayout(sub_layout)
        layout.addWidget(sub_group)

        # Navigation
        back_btn = QPushButton("Back to Home")
        back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        layout.addWidget(back_btn)

        # Add to stacked widget
        self.stacked_widget.addWidget(profile_widget)

    def initialize_state(self):
        # Load saved settings
        username = self.settings.value("username", "")
        if username:
            self.username_input.setText(username)
            self.profile_username.setText(f"Username: {username}")

        theme = self.settings.value("theme", "Light")
        self.theme_combo.setCurrentText(theme)

        # Notification settings
        self.enable_notif.setChecked(
            self.settings.value("notifications_enabled", True, type=bool)
        )
        self.sound_notif.setChecked(
            self.settings.value("sound_enabled", True, type=bool)
        )

        # Subscription plan
        sub_plan = self.settings.value("subscription_plan", 1, type=int)
        if sub_plan == 1:
            self.sub_free.setChecked(True)
        elif sub_plan == 2:
            self.sub_premium.setChecked(True)
        elif sub_plan == 3:
            self.sub_enterprise.setChecked(True)

        # Initialize application variables
        self.cart_items = []
        self.last_viewed_product = ""

        # Connect signals for stacked widget changes
        self.stacked_widget.currentChanged.connect(self.screen_changed)

    def screen_changed(self, index):
        """Handle screen navigation events"""
        screens = ["Home", "Products", "Settings", "Profile"]
        if index < len(screens):
            screen_name = screens[index]
            print(f"Navigated to {screen_name} screen")
            self.statusBar.showMessage(f"Current screen: {screen_name}")

            # Update context help based on current screen
            self.context_help_action.setText(f"Help for {screen_name}")

            # If we navigated to profile, update the display
            if index == 3:  # Profile screen
                self.update_profile_display()

    def update_profile_display(self):
        """Update profile screen with current data"""
        username = self.settings.value("username", "")
        self.profile_username.setText(
            f"Username: {username if username else 'Not Set'}"
        )

        self.cart_count.setText(f"Items in cart: {len(self.cart_items)}")
        self.last_product.setText(
            f"Last viewed product: {self.last_viewed_product or 'None'}"
        )

    def update_product_info(self, index):
        """Update product information when selection changes"""
        products_info = [
            "Product A: Basic model with standard features.",
            "Product B: Premium model with advanced features.",
            "Product C: Budget-friendly option with essential features.",
        ]

        if 0 <= index < len(products_info):
            self.product_info.setText(products_info[index])
            product_name = self.product_combo.currentText().split(" - ")[0]
            self.last_viewed_product = product_name
            print(f"Selected product: {product_name}")

    def add_to_cart(self):
        """Add current product to cart"""
        product = self.product_combo.currentText()
        quantity = self.quantity_spinner.value()

        item = f"{quantity}x {product}"
        self.cart_items.append(item)

        print(f"Added to cart: {item}")
        print(f"Cart now contains {len(self.cart_items)} items")

        self.statusBar.showMessage(f"Added {product} to cart", 2000)

        # Show a confirmation dialog
        QMessageBox.information(
            self, "Added to Cart", f"Added {quantity}x {product} to your cart."
        )

    def add_new_product(self):
        """Handle adding a new product (just a demo)"""
        QMessageBox.information(
            self,
            "Add Product",
            "This would open a product creation form in a real application.",
        )
        print("Add new product action triggered")

    def save_settings(self):
        """Save current settings"""
        # Save to QSettings
        self.settings.setValue("username", self.username_input.text())
        self.settings.setValue("theme", self.theme_combo.currentText())
        self.settings.setValue("notifications_enabled", self.enable_notif.isChecked())
        self.settings.setValue("sound_enabled", self.sound_notif.isChecked())

        # Save subscription plan
        sub_plan = self.sub_group.checkedId()
        self.settings.setValue("subscription_plan", sub_plan)

        print("Settings saved:")
        print(f"Username: {self.username_input.text()}")
        print(f"Theme: {self.theme_combo.currentText()}")
        print(f"Notifications: {self.enable_notif.isChecked()}")
        print(f"Sound: {self.sound_notif.isChecked()}")
        print(f"Subscription: {sub_plan}")

        # Confirm to user
        QMessageBox.information(
            self, "Settings Saved", "Your settings have been saved successfully."
        )

        # Update profile display if we've set a username
        if self.username_input.text():
            self.profile_username.setText(f"Username: {self.username_input.text()}")

    def reset_settings(self):
        """Reset settings to defaults"""
        # Ask for confirmation
        reply = QMessageBox.question(
            self,
            "Reset Settings",
            "Are you sure you want to reset all settings to default values?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if reply == QMessageBox.Yes:
            # Clear settings
            self.settings.clear()

            # Reset UI
            self.username_input.setText("")
            self.theme_combo.setCurrentText("Light")
            self.enable_notif.setChecked(True)
            self.sound_notif.setChecked(True)
            self.sub_free.setChecked(True)

            print("Settings reset to defaults")

            QMessageBox.information(
                self,
                "Settings Reset",
                "All settings have been reset to default values.",
            )

    def show_settings_dialog(self):
        """Show settings in a separate dialog"""
        dialog = SettingsDialog(self.settings, self)
        result = dialog.exec_()

        if result == QDialog.Accepted:
            # Refresh our displays with new settings
            username = self.settings.value("username", "")
            if username:
                self.username_input.setText(username)
                self.profile_username.setText(f"Username: {username}")

            self.theme_combo.setCurrentText(self.settings.value("theme", "Light"))
            self.enable_notif.setChecked(
                self.settings.value("notifications_enabled", True, type=bool)
            )
            self.sound_notif.setChecked(
                self.settings.value("sound_enabled", True, type=bool)
            )

            print("Settings updated from dialog")

    def show_context_help(self):
        """Show help for the current screen"""
        current_index = self.stacked_widget.currentIndex()
        screens = ["Home", "Products", "Settings", "Profile"]

        if current_index < len(screens):
            screen_name = screens[current_index]

            help_text = {
                "Home": "This is the home screen. Navigate to other sections using the buttons.",
                "Products": "Browse products, select quantities, and add them to your cart.",
                "Settings": "Configure application settings and preferences.",
                "Profile": "View your profile information and subscription status.",
            }

            QMessageBox.information(
                self,
                f"Help for {screen_name}",
                help_text.get(screen_name, "Help content not available."),
            )

            print(f"Showing context help for {screen_name} screen")

    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(
            self,
            "About PyQt App Flow Demo",
            "This application demonstrates menu navigation, screen flows, "
            "and state management in PyQt applications.",
        )
        print("About dialog displayed")


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
