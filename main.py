import cv2
import face_recognition
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import mysql.connector
import json  # Import the json module

class CriminalRecognitionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Criminal Recognition App")

        self.video_capture = cv2.VideoCapture(0)

        self.label = ttk.Label(root, text="Detected Criminal:")
        self.label.pack(pady=10)

        self.result_label = ttk.Label(root, text="Unknown")
        self.result_label.pack(pady=10)

        self.detect_button = ttk.Button(root, text="Detect Criminal", command=self.detect_criminal)
        self.detect_button.pack(pady=10)

        self.add_criminal_button = ttk.Button(root, text="Add Criminal", command=self.add_criminal)
        self.add_criminal_button.pack(pady=10)

        self.quit_button = ttk.Button(root, text="Quit", command=self.quit_app)
        self.quit_button.pack(pady=10)

        # Inisialisasi koneksi ke database MySQL
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="penjahat"
        )

        self.create_table()

    def create_table(self):
        # Membuat tabel jika belum ada
        query = '''
            CREATE TABLE IF NOT EXISTS criminals (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                encoding TEXT NOT NULL
            )
        '''
        with self.conn.cursor() as cursor:
            cursor.execute(query)
        self.conn.commit()

    def add_criminal(self):
        # Function to handle adding criminal when button is pressed
        def add_criminal_handler():
            name = tk.simpledialog.askstring("Add Criminal", "Enter criminal's name:")
            if name:
                # Continue with adding criminal to the database

                # Ambil dan encode wajah penjahat dari gambar
                _, frame = self.video_capture.read()
                face_locations = face_recognition.face_locations(frame)
                face_encodings = face_recognition.face_encodings(frame, face_locations)

                if not face_encodings:
                    messagebox.showerror("Error", "No face detected. Unable to add criminal.")
                    return

                criminal_encoding = face_encodings[0]

                # Masukkan data ke dalam database
                query = "INSERT INTO criminals (name, encoding) VALUES (%s, %s)"
                with self.conn.cursor() as cursor:
                    cursor.execute(query, (name, json.dumps(criminal_encoding.tolist())))
                self.conn.commit()

                messagebox.showinfo("Success", "Criminal added to the database.")

            else:
                messagebox.showerror("Error", "Please enter a valid name.")

        add_criminal_handler()

    def detect_criminal(self):
        # Ambil data penjahat dari database
        query = "SELECT * FROM criminals"
        
        with self.conn.cursor(dictionary=True) as cursor:
            cursor.execute(query)
            
            # Fetch all rows from the result set
            criminal_data = {}
            for row in cursor.fetchall():
                try:
                    # Check if the JSON string is not empty before decoding
                    if row['encoding']:
                        criminal_data[row['name']] = json.loads(row['encoding'])
                    else:
                        print(f"Empty JSON string for {row['name']}")
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON for {row['name']}: {e}")
                    print(f"Problematic JSON string: {row['encoding']}")

        _, frame = self.video_capture.read()

        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        name = "Unknown"

        for _, face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(list(criminal_data.values()), face_encoding)

            if True in matches:
                first_match_index = matches.index(True)
                name = list(criminal_data.keys())[first_match_index]

        self.result_label.config(text=name)

    def quit_app(self):
        self.video_capture.release()
        self.conn.close()
        self.root.destroy()

def main():
    root = tk.Tk()
    app = CriminalRecognitionApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
