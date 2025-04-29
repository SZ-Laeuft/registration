# Registration Application

This project is a PyQt5-based GUI application for managing user data through a RESTful API. It allows users to create, update, delete, and manage donations and gift collections for users identified by a UID.

## Features

- **Create User**: Add a new user with optional class information.
- **Delete User**: Remove a user by their UID.
- **Update User**: Modify user details using their UID.
- **Donation**: Set donation amounts for users.
- **Gift Collect**: Mark gifts as collected for users.

## Requirements

- Python 3.x
- PyQt5
- requests
- pyscard

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/registration.git
   ```

2. Navigate to the project directory:
   ```bash
   cd registration
   ```

## Usage

1. Run the application:
   ```bash
   python main.py
   ```

2. Use the GUI to perform operations such as creating, updating, or deleting users, and managing donations and gift collections.

## Configuration

- The application connects to a server at `http://szl-server:8080`. Ensure this server is accessible and running the appropriate API services.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.
