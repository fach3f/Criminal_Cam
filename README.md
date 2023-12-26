# Criminal Recognition App

Criminal Recognition App is a simple Python application that allows users to detect and track criminals using facial recognition. The application uses the face_recognition library for facial recognition and a MySQL database for storing criminal data.

## Features

- **Detect Criminals**: Use the camera to detect and recognize faces, identifying potential criminals based on the database entries.

- **Add Criminals**: Add new criminals to the database by capturing and storing their facial features.

- **User-friendly Interface**: The application provides a simple and intuitive graphical user interface using Tkinter.

## Prerequisites

Before running the application, make sure you have the following dependencies installed:

- Python 3.x
- OpenCV
- face_recognition
- Tkinter
- mysql-connector-python

Install the dependencies using the following command:

```bash
pip install opencv-python face-recognition pillow mysql-connector-python
```

## Setup

1. Clone the repository:

```bash
git clone https://github.com/fach3f/criminal-recognition-app.git
cd criminal-recognition-app
```

2. Set up the MySQL database:
    - Create a database named `penjahat`.
    - Update the database connection details in the `main.py` file.

3. Run the application:

```bash
python main.py
```

## Usage

1. Launch the application by running `main.py`.
2. Use the "Add Criminal" button to add new criminals to the database.
3. Use the "Detect Criminal" button to start facial recognition and identify potential criminals.
4. The detected criminal's name will be displayed on the user interface.

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.
