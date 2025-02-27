import sys
import logging
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QRadioButton, QMessageBox, QGroupBox, QDesktopWidget
)
from PyQt5.QtCore import Qt
import requests
from PyQt5.QtWidgets import QSizePolicy


# Set up logging
logging.basicConfig(level=logging.INFO)

class ApiDataInputForm(QMainWindow):
    def __init__(self):
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

        # Operation selection
        self.operation_group = QGroupBox("Select Operation")
        self.operation_layout = QHBoxLayout()
        self.operation_var = 1  # Default to "Create User"

        self.create_user_radio = QRadioButton("Create User")
        self.create_user_radio.setChecked(True)
        self.create_user_radio.toggled.connect(lambda: self.update_ui(1))
        self.operation_layout.addWidget(self.create_user_radio)

        self.delete_user_radio = QRadioButton("Delete User")
        self.delete_user_radio.toggled.connect(lambda: self.update_ui(2))
        self.operation_layout.addWidget(self.delete_user_radio)

        self.update_user_radio = QRadioButton("Update User")
        self.update_user_radio.toggled.connect(lambda: self.update_ui(3))
        self.operation_layout.addWidget(self.update_user_radio)

        self.operation_group.setLayout(self.operation_layout)
        self.layout.addWidget(self.operation_group)

        # Input fields
        self.id_label = QLabel("User ID:")
        self.id_entry = QLineEdit()
        self.layout.addWidget(self.id_label)
        self.layout.addWidget(self.id_entry)

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

        self.uid_label = QLabel("UID:")
        self.uid_entry = QLineEdit()
        self.layout.addWidget(self.uid_label)
        self.layout.addWidget(self.uid_entry)

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

        self.operation_group.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

    class ApiDataInputForm(QMainWindow):
        def __init__(self):
            # ... (existing code)

            # Add ID input field to the layout
            self.layout.addWidget(self.id_label)
            self.layout.addWidget(self.id_entry)

            # Store the layout item for the ID entry
            self.id_entry_layout_item = self.layout.itemAt(self.layout.count() - 1)

            # ... (rest of existing code)
    def center(self):
        """Center the window on the screen."""
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def get_stylesheet(self):
        """Return the stylesheet for the application."""
        return """
            QMainWindow {
                background-color: #f5f5f5;
            }
            QGroupBox {
                font-size: 25px;
                font-weight: bold;
                color: #333;
                border: 2px solid #0078d7;
                border-radius: 10px;
                margin-top: 20px;
                padding-top: 20px;
                padding-bottom: 20px; 
            }
            QLabel {
                font-size: 25px;
                color: #333;
            }
            QLineEdit {
                font-size: 25px;
                padding: 10px;
                border: 2px solid #ccc;
                border-radius: 5px;
                background-color: #fff;
            }
            QLineEdit:focus {
                border: 2px solid #0078d7;
            }
            QPushButton {
                font-size: 25px;
                font-weight: bold;
                padding: 12px 24px;
                background-color: #0078d7;
                color: white;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #005bb5;
            }
            QPushButton:pressed {
                background-color: #004080;
            }
            QRadioButton {
                font-size: 25px;
                color: #333;
            }
            QRadioButton::indicator {
                width: 16px;
                height: 16px;
            }
        """

    def send_to_api(self):
        """Determine which operation to perform based on the selected radio button."""
        if self.operation_var == 1:  # Create User
            self.create_user()
        elif self.operation_var == 2:  # Delete User
            self.delete_user_by_id()
        elif self.operation_var == 3:  # Update User
            self.update_user_by_id()

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

        if class_value and uid_value:
            url = 'https://192.168.68.116:44320/create-user-that-has-everything'
        elif class_value:
            url = 'https://192.168.68.116:44320/create-user-that-has-no-uid'
        else:
            url = 'https://192.168.68.116:44320/create-user-that-has-no-uid-and-no-class'

        self.send_request(url, 'POST', data, headers, "User created successfully!")

    def delete_user_by_id(self):
        """Send a DELETE request to delete a user by ID."""
        user_id = self.id_entry.text()
        if not user_id:
            QMessageBox.warning(self, "Warning", "Please enter a user ID.")
            return

        url = f'https://192.168.68.116:44320/api/DeleteUserById/{user_id}'
        headers = {'Content-Type': 'application/json'}

        self.send_request(url, 'DELETE', headers=headers, success_message="User deleted successfully!")

    def update_user_by_id(self):
        """Send a PUT request to update a user by ID."""
        user_id = self.id_entry.text()
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

        url = f'https://192.168.68.116:44320/api/ModifyUser/{user_id}'
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
        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))

    def load_user_data(self):
        """Send a GET request to load user data by UID or ID."""
        uid_number = self.uid_entry.text().strip()
        id_number = self.id_entry.text().strip()

        if not uid_number and not id_number:
            QMessageBox.critical(self, "Error", "Please enter a user ID or UID.")
            return

        if uid_number and id_number:
            QMessageBox.critical(self, "Error", "You can only search by one parameter (ID or UID).")
            return

        url = ''
        if uid_number:
            try:
                uid_number = float(uid_number)
                url = f'https://192.168.68.116:44320/api/ReadUserUID?uid={uid_number}'
            except ValueError:
                QMessageBox.critical(self, "Error", "Invalid UID.")
                return
        elif id_number:
            try:
                id_number = int(id_number)
                url = f'https://192.168.68.116:44320/api/ReadUserID/{id_number}'
            except ValueError:
                QMessageBox.critical(self, "Error", "Invalid user ID.")
                return

        headers = {'Content-Type': 'application/json'}

        try:
            response = requests.get(url, headers=headers, verify=False)
            if response.status_code == 200:
                user_data = response.json()

                if not user_data or user_data == {}:
                    QMessageBox.warning(self, "Warning", "No data found.")
                    return

                def clean_value(value):
                    return "" if value == {} else value

                self.id_entry.setText(str(clean_value(user_data.get('id', ''))))
                self.firstname_entry.setText(clean_value(user_data.get('firstName', '')))
                self.lastname_entry.setText(clean_value(user_data.get('lastName', '')))
                self.org_entry.setText(clean_value(user_data.get('organisation', '')))
                self.class_entry.setText(clean_value(user_data.get('schoolClass', '')))
                self.uid_entry.setText(str(clean_value(user_data.get('uid', ''))))

                QMessageBox.information(self, "Success", "Data loaded successfully!")
            elif response.status_code == 400:
                QMessageBox.critical(self, "Error", "Invalid request. Please check your input.")
            else:
                QMessageBox.critical(self, "Error", f"Error: {response.status_code}\n{response.text}")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def update_ui(self, operation):
        """Update the UI based on the selected operation."""
        self.operation_var = operation

        if operation == 1:  # Create User
            self.id_label.hide()
            self.id_entry.hide()
            self.firstname_label.show()
            self.firstname_entry.show()
            self.lastname_label.show()
            self.lastname_entry.show()
            self.org_label.show()
            self.org_entry.show()
            self.class_label.show()
            self.class_entry.show()
            self.uid_label.show()
            self.uid_entry.show()
            self.load_button.hide()
        elif operation == 2:  # Delete User
            self.id_label.show()
            self.id_entry.show()
            self.firstname_label.hide()
            self.firstname_entry.hide()
            self.lastname_label.hide()
            self.lastname_entry.hide()
            self.org_label.hide()
            self.org_entry.hide()
            self.class_label.hide()
            self.class_entry.hide()
            self.uid_label.hide()
            self.uid_entry.hide()
            self.load_button.hide()
        elif operation == 3:  # Update User
            self.id_label.show()
            self.id_entry.show()
            self.firstname_label.show()
            self.firstname_entry.show()
            self.lastname_label.show()
            self.lastname_entry.show()
            self.org_label.show()
            self.org_entry.show()
            self.class_label.show()
            self.class_entry.show()
            self.uid_label.show()
            self.uid_entry.show()
            self.load_button.show()

    def clear_all_inputs(self):
        """Clear all input fields."""
        self.id_entry.clear()
        self.firstname_entry.clear()
        self.lastname_entry.clear()
        self.org_entry.clear()
        self.class_entry.clear()
        self.uid_entry.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ApiDataInputForm()
    window.show()
    sys.exit(app.exec_())