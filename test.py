# import qrcode
# img = qrcode.make("www.google.com")
# img.save("test.jpg")
# creating a qr code img file

# import cv2
# d= cv2.QRCodeDetector()
# val,points,straight_qrcode=d.detectAndDecode(cv2.imread("test.jpg"))
# detecting qr code from file
# print(val)

import cv2
import numpy
import pyzbar.pyzbar as pyzbar

# caapturing video and qrcode in the frame and printing the outpass id
def scan():
    i=0
    id=''
    cap=cv2.VideoCapture(0)
    while i<1:
        _,frame =cap.read()
        decoded=pyzbar.decode(frame)
        for obj in decoded:
            id=obj.data.decode('UTF-8')
            print("\nThe Scanned QR Details:\n"+id+"\n")
            i=i+1
        cv2.imshow("QRCode",frame)
        cv2.waitKey(5)
        cv2.destroyAllWindows
    return id;

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime
from datetime import date, datetime, time
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db=firestore.client()

def time_difference(start_time):
    start_date=datetime.fromtimestamp(start_time.timestamp())
    current_date=datetime.now()
    difference =current_date-start_date
    print("Time Difference",difference)
    return difference
    
def checkOut():
    outpass_id=scan() #got the outpass id
    if(outpass_id!=""):
        print("\n--------Retrieving User Data from firestore-------- \n")
        user=db.collection('Outpass').document(outpass_id).get()
        if(user.exists):  # checking if outpass id present in outpass list
            user=user.to_dict()
            print("\nUser has a valid Outpass\n")
            print(user)
            if(user['status']=='yet to leave'):     #checking status of outpass
                print("\nStudent is yet to leave\n")
                difference_in_time=time_difference(user['start_date'])
                if(difference_in_time.days>=0):
                    print("Student leaving at appropriate time\n")
                    user.update({'status':'left'})#updating student object status
                    db.collection('checked_out').document(outpass_id).set(user) #student added to checked out list
                    db.collection('Outpass').document(outpass_id).update({'status':'left'})#updating status to left in outpass list
                    print("Student Checked out\n")
                else :
                    print("Student leaving before due time\n")
            else :
                print("Outpass has been used before\n")
        else :
            print("NO SUCH USER : INVALID QR")
    else:
        print('Outpass id empty')
    print("-----EXITING CONSOLE----")

# checkIn()

def checkIn():
    outpass_id=scan() #got the outpass id
    if(outpass_id!=""):
        print("\n--------Retrieving User Data from firestore-------- \n")
        user=db.collection('Outpass').document(outpass_id).get()
        if(user.exists):  # checking if outpass id present in outpass list
            user=user.to_dict()
            print("\nUser has a valid Outpass\n")
            print(user)
            if(user['status']=='left'):     #checking status of outpass
                print("\nStudent is returning to campus\n")
                difference_in_time=time_difference(user['end_date'])
                if(difference_in_time.days<0):
                    print("Student arriving at appropriate time\n")
                    user.update({'status':'returned'})#updating student document status
                    db.collection('checked_in').document(outpass_id).set(user) #student added to checked out list
                    db.collection('Outpass').document(outpass_id).update({'status':'returned'})#updating status to returned in outpass list
                    db.collection('checked_out').document(outpass_id).update({'status':'returned'})#updating status to returned in checked outlist
                    print("Student Checked In\n")
                else :
                    print("Student arriving after due time\n")
            else :
                print("Outpass has been used before\n")
        else :
            print("NO SUCH USER : INVALID QR")
    else:
        print('Outpass id empty')
    print("-----EXITING CONSOLE----")

checkIn()
# checkOut()