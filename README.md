Facial Recognition Attendance System
Overview
This Facial Recognition Attendance System uses computer vision and machine learning techniques to mark attendance by recognizing faces. 
It allows the administrator to manage student records and send attendance reports via email.

*----------------------------------*
Check "Guide to setup" file before running the code as you will need to make some changes
*----------------------------------*

Features
Facial Recognition for Attendance: Automatically marks attendance using facial recognition technology.
Email Integration: Sends attendance reports and notifications via email.
Admin Access: Allows the admin to access and manage attendance records.
Student Management: Allows the addition of new students to the system.
Data Storage: Saves attendance data in CSV and Excel formats.
Requirements
Python 3.x
Required libraries:
dlib
opencv-python
numpy
face_recognition
pandas
email
smtplib

Install the required libraries

Project Structure

Facial_Recognition_Attendance_System/
│
├── AttendanceData/          # Directory to store attendance data
├── images/                  # Directory to store student images
├── addstudent.py            # Script to add new students
├── main.py                  # Main script to run the attendance system
└── README.md                # This readme file
Usage
Setup Directories:
Ensure that the AttendanceData and images directories are created. This is handled by the script, but you can create them manually if needed.

Add Student:
Use the addstudent.py script to add new students. Ensure that each student's image file is named in the format ID_name.jpg and placed in the images directory.

Run the System:
Execute the main.py script to start the attendance system. Select from the following options:

Take Attendance: Starts the webcam and marks attendance.
Add Student: Adds a new student to the system.
Admin: Allows the admin to manage and retrieve attendance data.
About and Copyright Policy: Displays information about the project.
EXIT: Exits the program.
Email Reports:
The system can email attendance reports and notify students who were marked present. Ensure that the correct email credentials are configured in the script.

Admin Access
The admin can retrieve all attendance data via email. Admin login requires a username and password, followed by an OTP sent to the admin's email.

Notes
Ensure the webcam is connected and working correctly for facial recognition.
Modify the email configuration and credentials as needed.
Attendance data is saved in CSV format and converted to Excel for emailing.
Disclaimer
This project is free for use. For using this code in any other project/application, please consider taking prior permission.

Developer
Tushar 
Contact: chhikaratushar12@gmail.com
Tarun Joshi (taruntj2003@gmail.com)
Build: 2022
Version: 1.0
Thank you for using the Facial Recognition Attendance System!
