"""Modules
        cv2 for video Manipulation
        pandas for store data in DataFrame
        datetime for record time which stored in pandas DataFrame"""
import cv2,pandas
from datetime import datetime

video = cv2.VideoCapture(0)
first_frame = None
status_list = [None,None]
times = []
df = pandas.DataFrame(columns =["Start","End"] )
"""Record continues video i.e(picture Frame by Frame) """
while True:

    check,frame = video.read()
    status = 0
    # convert Color Frame Into Gray Frame
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray,(21,21),0)

    # Take First Frame
    if first_frame is None:
        first_frame = gray
        continue

    # Take the Difference between First frame and Gray Frame
    delta_frame = cv2.absdiff(first_frame,gray)

    thresh_frame = cv2.threshold(delta_frame,30,255,cv2.THRESH_BINARY)[1]
    thresh_frame = cv2.dilate(thresh_frame,None,iterations=2)

    (cnts,_)=cv2.findContours(thresh_frame.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # If contour is Grater than 10000 then make a rectangle around the moving thing
    for contour in cnts:
        if cv2.contourArea(contour)<10000:
            continue
        # Set status to 1 if object is seen within range of contour
        status = 1
        (x,y,w,h)=cv2.boundingRect(contour)
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3)
    
    #Append the status in Status_list
    status_list.append(status)

    """When Object is seen in front of camera and when status is set to 1
        then time is append in times list"""
    if status_list[-1]==1 and status_list[-2]==0:
        times.append(datetime.now())
    if status_list[-2]==1 and status_list[-1]==0:
        times.append(datetime.now())

    # show gray image on window
    cv2.imshow("gray frame",gray)
    cv2.imshow("delta frame",delta_frame)
    cv2.imshow("threshold frame",thresh_frame)
    cv2.imshow("color_frame",frame)
    # wait for one second and record the another frame
    key = cv2.waitKey(1)

    # if user press "q" then close all the window frames 
    if key==ord('q'):
        if status==1:
            times.append(datetime.now())
        break

print(status_list)
print(times)

# read the times list and append in pandas DataFrame into csv File(Times.csv)
for i in range(0,len(times),2):
    df = df.append({"Start":times[i],"End":times[i+1]},ignore_index = True)
df.to_csv("Times.csv")

# Release the Window and Destroy all Windows
video.release()
cv2.destroyAllWindows()