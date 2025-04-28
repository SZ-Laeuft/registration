import sys
import logging
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QRadioButton, QMessageBox, QGroupBox, QDesktopWidget, QSizePolicy, QButtonGroup
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import requests
from smartcard.System import readers # pip install pyscard
import threading

# Set up logging
logging.basicConfig(level=logging.INFO)


class SmartCardReaderThread(QThread):
    # Signal to send UID data back to the main thread
    uid_signal = pyqtSignal(str)

    def run(self):
        while True:
            try:
                # Get available smart card readers
                r = readers()
                connection = r[0].createConnection()
                connection.connect()
                # APDU command to get UID (for most NFC cards)
                command = [0xFF, 0xCA, 0x00, 0x00, 0x00]
                response, sw1, sw2 = connection.transmit(command)

                # Check if the command was successful
                if sw1 == 0x90:
                    # Convert the response to a string of digits (decimal)
                    uid_value = ''.join(str(byte) for byte in response)
                    # Emit the signal to update the UID in the main thread
                    self.uid_signal.emit(uid_value)
            except Exception as e:
                continue


class ApiDataInputForm(QMainWindow):
    """
    The main application window for the API data input form.

    This class provides a GUI for interacting with a user management API.
    """

    def __init__(self):
        """Initialize the ApiDataInputForm window."""
        super().__init__()
        self.setWindowTitle("API Data Input Form")
        self.setGeometry(100, 100, 600, 600)
        self.center()

        # Apply a modern and beautiful style using QSS
        self.setStyleSheet(self.get_stylesheet())

        # Main widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setSpacing(20)
        self.layout.setContentsMargins(20, 20, 20, 20)

        # Initialize radio button group
        self.radio_button_group = QButtonGroup(self)

        # Operation selection - User Management
        self.operation_group1 = QGroupBox("User Management")
        self.operation_layout1 = QHBoxLayout()

        self.create_user_radio = QRadioButton("Create User")
        self.create_user_radio.setChecked(True)
        self.create_user_radio.toggled.connect(lambda: self.update_ui(1))
        self.operation_layout1.addWidget(self.create_user_radio)
        self.radio_button_group.addButton(self.create_user_radio)

        self.delete_user_radio = QRadioButton("Delete User")
        self.delete_user_radio.toggled.connect(lambda: self.update_ui(2))
        self.operation_layout1.addWidget(self.delete_user_radio)
        self.radio_button_group.addButton(self.delete_user_radio)

        self.update_user_radio = QRadioButton("Update User")
        self.update_user_radio.toggled.connect(lambda: self.update_ui(3))
        self.operation_layout1.addWidget(self.update_user_radio)
        self.radio_button_group.addButton(self.update_user_radio)

        self.operation_group1.setLayout(self.operation_layout1)
        self.layout.addWidget(self.operation_group1)

        # Operation selection - Editing Value
        self.operation_group2 = QGroupBox("Editing Value")
        self.operation_layout2 = QHBoxLayout()

        self.donation_radio = QRadioButton("Donation")
        self.donation_radio.toggled.connect(lambda: self.update_ui(4))
        self.operation_layout2.addWidget(self.donation_radio)
        self.radio_button_group.addButton(self.donation_radio)

        self.gift_collect_radio = QRadioButton("Gift Collect")
        self.gift_collect_radio.toggled.connect(lambda: self.update_ui(5))
        self.operation_layout2.addWidget(self.gift_collect_radio)
        self.radio_button_group.addButton(self.gift_collect_radio)

        self.operation_group2.setLayout(self.operation_layout2)
        self.layout.addWidget(self.operation_group2)

        # Input fields
        self.uid_label = QLabel("UID:")
        self.uid_entry = QLineEdit()
        self.layout.addWidget(self.uid_label)
        self.layout.addWidget(self.uid_entry)

        self.firstname_label = QLabel("Firstname:")
        self.firstname_entry = QLineEdit()
        self.layout.addWidget(self.firstname_label)
        self.layout.addWidget(self.firstname_entry)

        self.lastname_label = QLabel("Lastname:")
        self.lastname_entry = QLineEdit()
        self.layout.addWidget(self.lastname_label)
        self.layout.addWidget(self.lastname_entry)

        self.org_label = QLabel("Organisation:")
        self.org_entry = QLineEdit()
        self.layout.addWidget(self.org_label)
        self.layout.addWidget(self.org_entry)

        self.class_label = QLabel("Class:")
        self.class_entry = QLineEdit()
        self.layout.addWidget(self.class_label)
        self.layout.addWidget(self.class_entry)

        self.Amount_label = QLabel("Amount:")
        self.Amount_entry = QLineEdit()
        self.layout.addWidget(self.Amount_label)
        self.layout.addWidget(self.Amount_entry)

        # Buttons
        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.send_to_api)
        self.layout.addWidget(self.submit_button)

        self.load_button = QPushButton("Load Data")
        self.load_button.clicked.connect(self.load_user_data)
        self.layout.addWidget(self.load_button)
        self.load_button.hide()

        self.clear_button = QPushButton("Clear All")
        self.clear_button.clicked.connect(self.clear_all_inputs)
        self.layout.addWidget(self.clear_button)

        # Initialize UI
        self.update_ui(1)
        self.operation_group1.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.operation_group2.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

        # Initialize the smart card reader thread
        self.reader_thread = SmartCardReaderThread()
        self.reader_thread.uid_signal.connect(self.update_uid_entry)
        self.reader_thread.start()

    def update_uid_entry(self, uid):
        """Update the UID entry with the data received from the smart card reader."""
        self.uid_entry.setText(uid)

    def send_to_api(self):
        """Determine which operation to perform based on the selected radio button."""
        if self.operation_var == 1:  # Create User
            self.create_user()
        elif self.operation_var == 2:  # Delete User
            self.delete_user_by_uid()
        elif self.operation_var == 3:  # Update User
            self.update_user_by_uid()
        elif self.operation_var == 4:  # Donation
            self.donation_by_uid()
        elif self.operation_var == 5:  # Gift Colected
            self.gift_collect_by_uid()

    def create_user(self):
        """Send a POST request to create a new user."""
        class_value = self.class_entry.text()
        uid_value = self.uid_entry.text()

        data = {
            "firstname": self.firstname_entry.text(),
            "lastname": self.lastname_entry.text(),
            "organisation": self.org_entry.text(),
            "school_class": class_value if class_value else None,
            "uid": uid_value if uid_value else None,
        }

        headers = {'Content-Type': 'application/json'}

        if class_value:
            url = 'http://szl-server:8080/api/User/create/with-class'
        else:
            url = 'http://szl-server:8080/api/User/create/without-class'

        self.send_request(url, 'POST', data, headers, "User created successfully!")

    def delete_user_by_uid(self):
        """Send a DELETE request to delete a user by UID."""
        user_uid = self.uid_entry.text()
        if not user_uid:
            QMessageBox.warning(self, "Warning", "Please enter a user UID.")
            return

        url = f'http://szl-server:8080/api/User/delete/{user_uid}'
        headers = {'Content-Type': 'application/json'}

        self.send_request(url, 'DELETE', headers=headers, success_message="User deleted successfully!")

    def update_user_by_uid(self):
        """Send a PUT request to update a user by UID."""
        user_id = self.uid_entry.text()
        if not user_id:
            QMessageBox.warning(self, "Warning", "Please enter a user ID.")
            return

        data = {
            "firstName": self.firstname_entry.text() or None,
            "lastName": self.lastname_entry.text() or None,
            "uid": self.uid_entry.text() or None,
            "schoolClass": self.class_entry.text() or None,
            "organisation": self.org_entry.text() or None
        }

        url = f'http://szl-server:8080/api/User/{user_id}'
        headers = {'Content-Type': 'application/json'}

        self.send_request(url, 'PUT', data, headers, "User updated successfully!")

    def send_request(self, url, method, data=None, headers=None, success_message=None):
        """Send an HTTP request and handle the response."""
        try:
            if method == 'POST':
                response = requests.post(url, json=data, headers=headers, verify=False)
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers, verify=False)
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=headers, verify=False)
            else:
                raise ValueError("Unsupported HTTP method")

            if response.status_code == 200:
                if success_message:
                    QMessageBox.information(self, "Success", success_message)
            else:
                QMessageBox.critical(self, "Error", f"Error: {response.status_code}\n{response.text}")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Error", f"Network error: {str(e)}")

    def update_ui(self, operation_var):
        """Update UI based on selected operation."""
        self.operation_var = operation_var
        self.clear_all_inputs()

        # Hide and show the relevant input fields and labels based on the selected operation
        if operation_var == 1:  # Create User
            self.uid_label.show()
            self.uid_entry.show()
            self.class_label.show()
            self.class_entry.show()
            self.firstname_label.show()
            self.firstname_entry.show()
            self.lastname_label.show()
            self.lastname_entry.show()
            self.org_label.show()
            self.org_entry.show()
            self.Amount_label.hide()
            self.Amount_entry.hide()
            self.load_button.hide()
        elif operation_var == 2:  # Delete User
            self.uid_label.show()
            self.uid_entry.show()
            self.firstname_label.hide()
            self.firstname_entry.hide()
            self.lastname_label.hide()
            self.lastname_entry.hide()
            self.org_label.hide()
            self.org_entry.hide()
            self.class_label.hide()
            self.class_entry.hide()
            self.Amount_label.hide()
            self.Amount_entry.hide()
            self.load_button.show()
        elif operation_var == 3:  # Update User
            self.uid_label.show()
            self.uid_entry.show()
            self.firstname_label.show()
            self.firstname_entry.show()
            self.lastname_label.show()
            self.lastname_entry.show()
            self.org_label.show()
            self.org_entry.show()
            self.class_label.show()
            self.class_entry.show()
            self.Amount_label.hide()
            self.Amount_entry.hide()
            self.load_button.show()
        elif operation_var == 4:  # Donation
            self.uid_label.show()
            self.uid_entry.show()
            self.Amount_label.show()
            self.Amount_entry.show()
            self.firstname_label.hide()
            self.firstname_entry.hide()
            self.lastname_label.hide()
            self.lastname_entry.hide()
            self.org_label.hide()
            self.org_entry.hide()
            self.class_label.hide()
            self.class_entry.hide()
            self.load_button.hide()
        elif operation_var == 5:  # Gift Collect
            self.uid_label.show()
            self.uid_entry.show()
            self.Amount_label.hide()
            self.Amount_entry.hide()
            self.firstname_label.hide()
            self.firstname_entry.hide()
            self.lastname_label.hide()
            self.lastname_entry.hide()
            self.org_label.hide()
            self.org_entry.hide()
            self.class_label.hide()
            self.class_entry.hide()
            self.load_button.hide()

    def clear_all_inputs(self):
        """Clear all input fields."""
        self.firstname_entry.clear()
        self.lastname_entry.clear()
        self.uid_entry.clear()
        self.org_entry.clear()
        self.class_entry.clear()
        self.Amount_entry.clear()

    def load_user_data(self):
        """Load user data based on UID"""
        user_uid = self.uid_entry.text()
        if not user_uid:
            QMessageBox.warning(self, "Warning", "Please enter a user UID to load.")
            return

        url = f'http://szl-server:8080/api/User/read/by-uid?uid={user_uid}'
        headers = {'Content-Type': 'application/json'}

        self.send_request(url, 'GET', headers=headers, success_message="User data loaded successfully!")

    def center(self):
        """Center the window on the screen."""
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def get_stylesheet(self):
        """Return the stylesheet for the application."""
        return """
            QMainWindow { background-color: #f5f5f5; }
            QGroupBox {
                font-size: 25px; font-weight: bold; color: #333;
                border: 2px solid #0078d7; border-radius: 10px;
                margin-top: 20px; padding-top: 20px; padding-bottom: 20px;
            }
            QLabel { font-size: 25px; color: #333; }
            QLineEdit {
                font-size: 25px; padding: 10px; border: 2px solid #ccc;
                border-radius: 5px; background-color: #fff;
            }
            QLineEdit:focus { border: 2px solid #0078d7; }
            QPushButton {
                font-size: 25px; font-weight: bold; padding: 12px 24px;
                background-color: #0078d7; color: white; border: none; border-radius: 5px;
            }
            QPushButton:hover { background-color: #005bb5; }
            QPushButton:pressed { background-color: #004080; }
            QRadioButton { font-size: 25px; color: #333; }
            QRadioButton::indicator { width: 16px; height: 16px; }
        """


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ApiDataInputForm()
    window.show()
    sys.exit(app.exec_())
