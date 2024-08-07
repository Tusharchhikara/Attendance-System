import cv2
import time
import os
import csv

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


# SET THE COUNTDOWN TIMER
# for simplicity we set it to 3
# We can also take this as input
TIMER = int(5)
  
# Open the camera
cap = cv2.VideoCapture(0)

print("ADD Student")


print("""
    Q to take a picture
    """)

while True:
     
    # Read and display each frame
    ret, img = cap.read()
    cv2.imshow('Add_Studnet', img)
 
    # check for the key pressed
    k = cv2.waitKey(125)
 
    # set the key for the countdown
    # to begin. Here we set q
    # if key pressed is q
    if k == ord('q'):
        prev = time.time()
 
        while TIMER >= 0:
            ret, img = cap.read()
 
            # Display countdown on each frame
            # specify the font and draw the
            # countdown using puttext
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(img, str(TIMER),
                        (200, 250), font,
                        7, (0, 255, 255),
                        4, cv2.LINE_AA)
            cv2.imshow('Add_Studnet', img)
            cv2.waitKey(125)
 
            # current time
            cur = time.time()
 
            # Update and keep track of Countdown
            # if time elapsed is one second
            # than decrease the counter
            if cur-prev >= 1:
                prev = cur
                TIMER = TIMER-1
 
        else:
            ret, img = cap.read()
 
            # Display the clicked frame for 2
            # sec.You can increase time in
            # waitKey also
            cv2.imshow('Add_Studnet', img)
 
            # time for which image displayed
            cv2.waitKey(2000)
            def regno():
                r=input("Enter Your Reg_No : ")
                if len(r)==9:
                    if r in personID:
                        print("Already Present")
                        regno()
                else:
                    print("In-valid Re-Enter Reg No")
                    regno()
                return r
            reg=regno()
            name=input("Enter First Name : ")
            email=input("Enter Email : ")
            List = os.listdir()
            # field names 
            fields = ['id', 'name', 'email'] 
            # data rows of csv file 
            rows = [reg,name,email]
            i="record.csv"

            if i in List:
                filename = "record.csv"
                with open(filename, 'a',newline="") as csvfile: 
                    csvwriter = csv.writer(csvfile)  
                    csvwriter.writerow(rows)
            else:
                filename = "record.csv"
                with open(filename, 'a',newline="") as csvfile: 
                    csvwriter = csv.writer(csvfile) 
                    csvwriter.writerow(fields) 
                    csvwriter.writerow(rows)
            
            # Save the frame
            cv2.imwrite('images/'+reg+name+'.jpg', img)
 
            # HERE we can reset the Countdown timer
            # if we want more Capture without closing
            # the camera
            print("Added")
            cv2.waitKey(6000)
            break
    # Press Esc to exit
    elif k == 27:
        break
 
# close the camera
cap.release()
  
# close all the opened windows
cv2.destroyAllWindows()
