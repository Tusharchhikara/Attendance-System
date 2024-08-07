import dlib
import cv2
import numpy as np
import face_recognition
import os
import sys
import hashlib
from datetime import datetime
from multiprocessing import Process
import time
import pandas as pd
import csv
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
import smtplib
from email.utils import formatdate
from email import encoders
import getpass
from subprocess import call
import random

# Creating Folder AttendanceData & images
try:
    os.mkdir("AttendanceData")
    os.mkdir("images")
    print ("Directory is created")
except FileExistsError:
    a=0

# Attendance Part
def attendance_system():
    path = 'images'
    images = []
    personNames = []
    personID = []
    myList = os.listdir(path)
    #print(myList)
    for cu_img in myList:
        current_Img = cv2.imread(f'{path}/{cu_img}')
        images.append(current_Img)
        # personNames.append(os.path.splitext(cu_img)[0])
        details=os.path.splitext(cu_img)[0]
        personNames.append(details[9:])
        personID.append(details[:9])
    #print(personNames)
    #print(personID)
    file=input("Enter Name For Attendance file : ")
    
    with open("./AttendanceData/"+file+'.csv', 'w+') as f:
        f.writelines('ID,Name,Time,Date')
    def faceEncodings(images):
        encodeList = []
        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        return encodeList

    def attendance(name,ID):
        with open("./AttendanceData/"+file+".csv", 'r+') as f:
            myDataList = f.readlines()
            nameList = []
            IDlist = []
            for line in myDataList:
                entry = line.split(',')
                IDlist.append(entry[0])
            if ID not in IDlist:
                time_now = datetime.now()
                tStr = time_now.strftime('%H:%M:%S')
                dStr = time_now.strftime('%d/%m/%Y')
                f.writelines(f'\n{ID},{name},{tStr},{dStr}')
                print("Dectected and Marked")


    encodeListKnown = faceEncodings(images)
    #print('All Encodings Complete!!!')
    print("Started")
    cap = cv2.VideoCapture(0)
    timeout = time.time() + 60*0.5   # 18 sec from now
    while True:
        ret, frame = cap.read()
        faces = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
        faces = cv2.cvtColor(faces, cv2.COLOR_BGR2RGB)

        facesCurrentFrame = face_recognition.face_locations(faces)
        encodesCurrentFrame = face_recognition.face_encodings(faces, facesCurrentFrame)

        for encodeFace, faceLoc in zip(encodesCurrentFrame, facesCurrentFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            # print(faceDis)
            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                name = personNames[matchIndex].upper()
                ID = personID[matchIndex]
                # print(name)
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(frame, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(frame, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                attendance(name,ID)


        cv2.imshow('Webcam', frame)
        if cv2.waitKey(1) == 13:
            break
        if timeout<=time.time():
            break

    count=len(personID)
    #cap.release()
    #cv2.destroyAllWindows()

    ###     Email Attendance File 

    def send_mail():
        ans1=input("Do you want attendance file via E-Mail [Y/N]: ")
        if ans1=="y" or ans1=="Y" or ans1=="YES" or ans1=="Yes" or ans1=="yes":
            email=input("Enter You E-Mail : ")
            time_now = datetime.now()
            dStr = time_now.strftime('%d/%m/%Y')
            # Create a message
            msg = MIMEMultipart()
            body_part = MIMEText('Find The File Attached \nAttendance Report \nThis is an auto genrated mail', 'plain')
            msg['Subject'] = file+f" - {dStr}"
            msg['From'] = 'anymail@outlook.com'
            msg['To'] = email
            # body of email
            msg.attach(body_part)

            #covert csv to xlsx
                
            df = pd.read_csv("./AttendanceData/"+file+'.csv')
            df.to_excel("./AttendanceData/"+file+'.xlsx', index=None, header=True)
            os.remove("./AttendanceData/"+file+".csv")
            
            part = MIMEBase('application', "octet-stream")
            part.set_payload(open("./AttendanceData/"+file+".xlsx", "rb").read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', "attachment; "+"filename="+file+".xlsx")
            msg.attach(part)

            # Create SMTP object
            server = smtplib.SMTP('smtp.office365.com', 587)
            server.starttls()    
            # Login to the server
            server.login('anymail@outlook.com','password')


            # Convert the message to a string and send it
            server.sendmail(msg['From'], msg['To'], msg.as_string())
            server.quit()
            print("E-Mail Sent")
                

                
        elif ans1=="n" or ans1=="N" or ans1=="NO" or ans1=="no" or ans1=="No" :
            print("Fill Will be Saved on computer")
            df = pd.read_csv("./AttendanceData/"+file+'.csv')
            df.to_excel("./AttendanceData/"+file+'.xlsx', index=None, header=True)
            os.remove("./AttendanceData/"+file+".csv")
            print("File Saved")
        else:
            print("Please Enter valid choice :)")
            send_mail()
    send_mail()

    ##     Auto E-mail to Student

    def present_student_mail(personID):
        ans1=input("Do you want to Notify All Present Student via E-Mail [Y/N]: ")
        if ans1=="y" or ans1=="Y" or ans1=="YES" or ans1=="Yes" or ans1=="yes":
            def present_mail(mail,name):
                email=mail
                time_now = datetime.now()
                dStr = time_now.strftime('%d/%m/%Y')
                # Create a message
                msg = MIMEMultipart()
                body_part = MIMEText(name +', You are Marked Present \nThis is an auto genrated mail '+'\nAttendance Report' + 'plain')
                msg['Subject'] = "Attendance of"+f" - {dStr}"
                msg['From'] = 'anymail@outlook.com'
                msg['To'] = email

                msg.attach(body_part)

                # Create SMTP object
                server = smtplib.SMTP('smtp.office365.com', 587)
                server.starttls()    
                # Login to the server
                server.login('anymail@outlook.com','password')

                # Convert the message to a string and send it
                server.sendmail(msg['From'], msg['To'], msg.as_string())
                server.quit()
        

            data=open("record.csv","r+")
            DataCaptured = csv.reader(data, delimiter=',', skipinitialspace=True)
            ID,Name ,Email =[], [], []
            for row in DataCaptured:
                if row[0] not in ID:
                    ID.append(row[0])
                if row[1] not in ID:
                    Name.append(row[1])
                if row[2] not in Email:
                    Email.append(row[2])
            ID.remove("id")
            Email.remove("email")
            Name.remove("name")
            id_dct = {ID[i]: Email[i] for i in range(0, len(ID))}
            name_dct = {ID[i]: Name[i] for i in range(0, len(ID))}
            l=id_dct.keys()
            for i in range(len(personID)):
                if str(personID[i]) in l:
                    mail=id_dct[str(personID[i])]
                    name=name_dct[str(personID[i])]
                    present_mail(mail,name)
            print("All E-Mail Sent")      

            
        elif ans1=="n" or ans1=="N" or ans1=="NO" or ans1=="no" or ans1=="No" :
            print()	
        else:
            print("Please Enter valid choice :)")
            present_student_mail()
    present_student_mail(personID)

#ADMIN
def admin():
    print("ADMIN Login")
    name=input("User Name : ")
    checker=hashlib.md5(name.encode()).hexdigest()
    if checker=="hardcoded hash value of admin username":
        print("""
    Loged in as Tushar
              
        """)
        while True:
            print("Welcome Admin")
            print("Recive All Attendance Data Via E-Mail")
            password=getpass.getpass("Enter Password ")
            epassword=hashlib.md5(password.encode()).hexdigest()
            if epassword=="hardcode hash value of password":
                email="enter your email"
                def otp():
                    onetimepass=[]
                    number=["0","1","2","3","4","5","6","7","8","9"]
                    i=1
                    while i<=6:
                        for j in range(0,1):
                            onetimepass.append(random.choice(number))
                            i=i+1
                    gen_pass="".join(onetimepass)
                    return gen_pass
                otp1=otp()
                msg = MIMEMultipart()
                body_part = MIMEText('Your One Time Password is : '+str(otp1)+' \nAttendance Report \nThis is an auto genrated mail', 'plain')
                msg['Subject'] = "ADMIN OTP"
                msg['From'] = 'anymail@outlook.com'
                msg['To'] = email
                # body of email
                msg.attach(body_part)
                server = smtplib.SMTP('smtp.office365.com', 587)
                server.starttls()    
                # Login to the server
                server.login('anymail@outlook.com','password')
                # Convert the message to a string and send it
                server.sendmail(msg['From'], msg['To'], msg.as_string())
                server.quit()
                otp2=input("Enter The OTP Sent To Your Email : ")
                if otp1==otp2 :
                    time_now = datetime.now()
                    dStr = time_now.strftime('%d/%m/%Y')
                    # Create a message
                    msg = MIMEMultipart()
                    body_part = MIMEText('ADMIN please Find ALL File Attached \nThis is an auto genrated mail', 'plain')
                    msg['Subject'] = "ADMIN Attendance Report"+f" - {dStr}"
                    msg['From'] = 'anymail@outlook.com'
                    msg['To'] = email
                    # body of email
                    msg.attach(body_part)
                    for file in os.listdir("AttendanceData"):
                        part = MIMEBase('application', "octet-stream")
                        part.set_payload(open("./AttendanceData/"+file, "rb").read())
                        encoders.encode_base64(part)
                        part.add_header('Content-Disposition','attachment; filename="%s"' % file)
                        msg.attach(part)

                    # Create SMTP object
                    server = smtplib.SMTP('smtp.office365.com', 587)
                    server.starttls()    
                    # Login to the server
                    server.login('anymail@outlook.com','password')

                    # Convert the message to a string and send it
                    server.sendmail(msg['From'], msg['To'], msg.as_string())
                    server.quit()
                    print("E-Mail Sent")
                    break
                else:
                    print("OTP In-valid")
                    break
            else:
                continue               

# Add Student
def add_student():
    call(['python','addstudent.py'])

# Main Selection Part
def main():
    input1=int(input("""Please Select One Option :
1.Take Attendance
2.Add Student
3.Admin
4.About and Copyright Policy
5.EXIT
    """))
    if input1==1:
        os.system('cls')
        print(" Ready To Take Attendance ")
        attendance_system()
        os.system('cls')
        main()
    elif input1==2:
        os.system('cls')
        add_student()
        os.system('cls')
        main()
    elif input1==3:
        os.system('cls')
        admin()
        os.system('cls')
        main()
    elif input1==4:
        os.system('cls')
        print("""
                About
    Facial Recogniation Attendance System
    
    It is free for use.

    For use of this program's code in any project/application/any other program .
    Please Considering taking persimission prior :)
    Thank You

      Bulid 2022
      Version 1.0
      Developer Tushar and Team
      Contact chhikaratushar12@gmail.com
         """)
        print("Thank You :)")
        main()
    elif input1==5:
        sys.exit()
    else:
        print("Enter vaild Choice :)")
        main()
print("Welcome, To Attendance System")
main()
