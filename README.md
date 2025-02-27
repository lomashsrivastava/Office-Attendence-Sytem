Office Attendance System

Description

This Office Attendance System is a desktop application built using Python and Tkinter for managing employee attendance with live face capture. The system allows users to mark attendance by entering their Employee ID and Name, while simultaneously capturing their live image using a webcam.

Features

Employee ID and Name Input

Automatic Time & Date Recording

Live Camera Preview

Image Capture with Attendance

Real-time Attendance Record Display

Scrollable Attendance Records

Animated Success Effect

Modern UI with Color Themes

Technologies Used

Python

Tkinter (GUI Development)

OpenCV (Image Capture)

JSON (Data Storage)

Pillow (Image Processing)

Installation

Clone the repository:

git clone https://github.com/yourusername/attendance-system.git
cd attendance-system

Install the required libraries:

pip install opencv-python-headless Pillow

Run the Application:

python a.py

Folder Structure

attendance-system/
├─ attendance_data.json      # Attendance data file
├─ attendance_images/        # Captured employee images
└─ a.py                      # Main Application File

How to Use

Enter the Employee ID and Name in the input fields.

The live camera feed will display your image.

Click on Mark Attendance.

The system will capture your image and store it with the timestamp.

The attendance record with the captured image will be displayed.

Preview



License

This project is licensed under the MIT License.

Author

Lomash Srivastava

Contributing

Feel free to raise issues or submit pull requests!
