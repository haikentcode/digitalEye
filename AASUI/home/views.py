from django.shortcuts import render,HttpResponse,render_to_response,HttpResponseRedirect
from django.contrib import auth
from home.models import  Teacher , Attendance , Student ,Log ,ImageData

from digitalEye import Objects as obj
from digitalEye import Recog as rec
import sys
import cv2
import os
import datetime
import time
from django.views.decorators.csrf import csrf_exempt

import redis
import pickle
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

def cpath(fpath):
    return os.path.join(__location__, fpath)
def onTeacher(request):
      return Teacher.objects.get(emailId=request.session.get('teacher'))

def getStudent(rollNumber):
    return Student.objects.get(rollNumber=rollNumber)

def index(request):
    if request.session.get('teacher',None):
        teacher=onTeacher(request)
        return render(request,'home/home.html',{"user":teacher,'range':range(2010,2222)})
    else:

       return HttpResponseRedirect('/login')



def login(request):
    error=""
    if request.POST:
     data=request.POST
     emailId=data.get('emailId')
     password=data.get('password')
     print emailId,password
     flag=False
     try:
          teacher=Teacher.objects.get(emailId=emailId)
          if teacher.emailId==emailId and teacher.password==password:
               flag=True
               request.session['teacher']=emailId
               return HttpResponseRedirect('/home')
          else:
               flag=False
     except Exception,e:
          error=e
    return render(request,'home/login.html',{"error":error})


def logout(request):
      del request.session['teacher']
      return HttpResponseRedirect('/home')


def help(request):
    return render(request,'home/help.html',{})



def history(request,year=0,month=0,day=0):

    teacher=onTeacher(request)
    attendanceList=Attendance.objects.filter(teacher=teacher)
    return render(request,'home/history.html',{'attendanceList':attendanceList,'user':teacher})


def getimageslables(course,branch,batch):
            students=Student.objects.filter(course__iexact=course,branch__iexact=branch,batch__iexact=batch) # __iexact ignore case
            images=[]
            lables=[]
            for student in students:
                for image in student.imagedata_set.all():
                    lables.append(int(student.rollNumber))
                    img='media/%s' % image
                    img=cv2.imread(img)
                    img=cv2.resize(img,(600,600),interpolation=cv2.INTER_AREA)
                    img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
                    images.append(img)
            return images ,lables


def getpredictABC(r1,r2,r3,frame):
    face=obj.Face(1.6,5,20,20)
    faces=face.getFaces(frame)
    print "No of faces found",len(faces)
    abclist=[]
    for f in faces:
           simg=cv2.cvtColor(f,cv2.COLOR_BGR2GRAY)
           simg=cv2.resize(simg,(600,600),interpolation=cv2.INTER_AREA)
           a=r1.getLable(simg)
           b=r2.getLable(simg)
           c=r3.getLable(simg)
           abclist.append(( a,b,c))
    return abclist



def getr1r2r3(course,branch,batch):
      images,lables=getimageslables(course,branch,batch)
      print images,lables
      r1 = rec.Recognizer()
      r2 = rec.Recognizer()
      r3 = rec.Recognizer()
      r1.train(images,lables,0)
      r2.train(images,lables,1)
      r3.train(images,lables,2)
      return r1,r2,r3

def setBranchCourseBatch(request):
    course=request.POST.get('course')
    branch=request.POST.get('branch')
    batch=request.POST.get('batch')
    request.session['course']=course
    request.session['branch']=branch
    request.session['batch']=batch

def getBranchCourseBatch(request):
    course=request.session.get('course')
    branch=request.session.get('branch')
    batch=request.session.get('batch')
    return branch,course,batch

def startcapturing(request):
      #this is way to read video frame
      #path=cpath("/home/haikent/Desktop/fyp/digitalEye/AASUI/media/media/dic.mp4")
      #print path
      #cap=cv2.VideoCapture(path)
      #-------------------*------------------------------------//
      """
      cap=cv2.VideoCapture(0) #"http://10.42.0.41:8080/video"
      course=request.POST.get('course')
      branch=request.POST.get('branch')
      batch=request.POST.get('batch')

      r1,r2,r3=getr1r2r3(course,branch,batch)

      hk=True
      while(True):
         ret,frame=cap.read()
         if not ret: continue
         cv2.imshow('frame',frame)
         print getpredictABC(r1,r2,r3,frame)
         if cv2.waitKey(1)& 0xFF==ord('q'):
                 break
      cv2.destroyAllWindows()

      print "complete task"
      return HttpResponse("ho gya")
      """
      setBranchCourseBatch(request)





def handle_uploaded_file(f,name):
    imagePath='media/'+name
    imageSavePath='media/'+imagePath
    with open(imageSavePath, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return imagePath

def mupload(request):
    images=request.FILES.getlist('file')
    for image in images:
          imagePath=handle_uploaded_file(image,image.name)
          rollNumber=image.name.split(".")[0]  # demo 12103074.9 -> 12103074
          imgd=ImageData()
          imgd.image=imagePath
          student=getStudent(rollNumber)
          if student :
              imgd.student = student
              imgd.save()
          else:
             print "error rollNumber:",rollNumber
    return HttpResponse("done")

def domore(request):
    return render(request,'home/domore.html',{'user': onTeacher(request)})




def webcamtest(request):
        return render(request,'home/testwebcam.html',{'user': onTeacher(request)})



#this function take Inmemoryuploadedfile and save into temp file read as openCV image and return then del tem
def get_uploaded_image(f,name):
    imagePath='media/'+name
    imageSavePath='media/'+imagePath
    with open(imageSavePath, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    img=cv2.imread(imageSavePath)
    os.remove(imageSavePath)
    return img


#this function get webcam.upload using FILES upload method
#csrf_exempt remove csrf missing server side error

@csrf_exempt
def webcamimage(request):
       teacher=onTeacher(request)
       if request.FILES:
           image=request.FILES.get('webcam')
           image=get_uploaded_image(image,teacher.emailId)
           print image ,"notkfdfd"
       return HttpResponse("done")
