import tkinter as tk
from tkinter import messagebox, scrolledtext
import json
from datetime import datetime
from tkinter import ttk
import time
import cv2
from PIL import Image, ImageTk
import os

# File to store attendance data
ATTENDANCE_FILE = "attendance_data.json"
IMAGE_FOLDER = "attendance_images"

if not os.path.exists(IMAGE_FOLDER):
    os.makedirs(IMAGE_FOLDER)

# Load existing attendance data
def load_attendance():
    try:
        with open(ATTENDANCE_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Save attendance data
def save_attendance(data):
    with open(ATTENDANCE_FILE, "w") as file:
        json.dump(data, file, indent=4)

# Capture Image
def capture_image(employee_id):
    ret, frame = cap.read()
    if ret:
        image_path = os.path.join(IMAGE_FOLDER, f"{employee_id}.jpg")
        cv2.imwrite(image_path, frame)
        return image_path
    return None

# Mark attendance
def mark_attendance():
    employee_id = entry_id.get()
    employee_name = entry_name.get()

    if not employee_id or not employee_name:
        messagebox.showwarning("Input Error", "Please enter both Employee ID and Name.")
        return

    attendance_data = load_attendance()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if employee_id in attendance_data:
        messagebox.showinfo("Info", f"Attendance already marked for {employee_name} (ID: {employee_id}).")
    else:
        image_path = capture_image(employee_id)
        attendance_data[employee_id] = {
            "name": employee_name,
            "timestamp": current_time,
            "image": image_path
        }
        save_attendance(attendance_data)
        messagebox.showinfo("Success", f"Attendance marked for {employee_name} (ID: {employee_id}).")
        animate_success()
        entry_id.delete(0, tk.END)
        entry_name.delete(0, tk.END)
        update_attendance_display()

# Update the attendance display
def update_attendance_display():
    attendance_data = load_attendance()
    display_area.delete(1.0, tk.END)
    if not attendance_data:
        display_area.insert(tk.END, "No attendance records found.")
    else:
        for emp_id, data in attendance_data.items():
            display_area.insert(tk.END, f"ID: {emp_id}, Name: {data['name']}, Time: {data['timestamp']}\n", ("record",))
            if data.get("image") and os.path.exists(data["image"]):
                img = Image.open(data["image"])
                img = img.resize((100, 100), Image.ANTIALIAS)
                imgtk = ImageTk.PhotoImage(img)
                display_area.image_create(tk.END, image=imgtk)
                display_area.insert(tk.END, "\n")
                display_area.image = imgtk
                display_area.insert(tk.END, "\n\n")

# Success animation
def animate_success():
    for _ in range(10):
        title_label.config(fg="#2ECC71")
        app.update()
        time.sleep(0.1)
        title_label.config(fg="#ECF0F1")
        app.update()
        time.sleep(0.1)

# Camera Capture
cap = cv2.VideoCapture(0)

def show_camera():
    def update_frame():
        ret, frame = cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            camera_label.imgtk = imgtk
            camera_label.configure(image=imgtk)
        camera_label.after(10, update_frame)

    update_frame()

# UI Setup
app = tk.Tk()
app.title("Office Attendance System")
app.geometry("900x700")
app.config(bg="#1B2631")

style = ttk.Style()
style.configure("TButton", font=("Arial", 12), padding=10, background="#E74C3C", foreground="white")

# Title Label
title_label = tk.Label(app, text="Office Attendance System", font=("Helvetica", 28, "bold"), bg="#1B2631", fg="#ECF0F1")
title_label.pack(pady=20)

# Left Frame for Input
left_frame = tk.Frame(app, bg="#34495E", padx=20, pady=20, relief=tk.GROOVE, bd=5)
left_frame.pack(side=tk.LEFT, padx=20, pady=20, fill=tk.BOTH, expand=True)

label_id = tk.Label(left_frame, text="Employee ID:", font=("Arial", 12), bg="#34495E", fg="white")
label_id.pack(pady=5)
entry_id = tk.Entry(left_frame, font=("Arial", 12))
entry_id.pack(pady=5)

label_name = tk.Label(left_frame, text="Employee Name:", font=("Arial", 12), bg="#34495E", fg="white")
label_name.pack(pady=5)
entry_name = tk.Entry(left_frame, font=("Arial", 12))
entry_name.pack(pady=5)

button_mark = ttk.Button(left_frame, text="Mark Attendance", command=mark_attendance)
button_mark.pack(pady=20)

# Camera Frame
camera_label = tk.Label(left_frame, bg="#34495E")
camera_label.pack(pady=10, fill=tk.BOTH, expand=True)

# Right Frame for Display
right_frame = tk.Frame(app, bg="#2C3E50", padx=20, pady=20, relief=tk.GROOVE, bd=5)
right_frame.pack(side=tk.RIGHT, padx=20, pady=20, fill=tk.BOTH, expand=True)

label_display = tk.Label(right_frame, text="Attendance Records:", font=("Arial", 14, "bold"), bg="#2C3E50", fg="white")
label_display.pack(pady=5)

display_area = scrolledtext.ScrolledText(right_frame, wrap=tk.WORD, width=50, height=15, font=("Arial", 12), bg="#F4F6F6", fg="#2C3E50")
display_area.pack(pady=5, fill=tk.BOTH, expand=True)
display_area.tag_configure("record", foreground="#34495E", font=("Arial", 12))

# Load and display existing attendance data on startup
update_attendance_display()
show_camera()

# Run the application
app.mainloop()
