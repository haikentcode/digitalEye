from django.shortcuts import render,HttpResponse,render_to_response,HttpResponseRedirect
from django.contrib import auth
from home.models import  Teacher , Attendance , Student

from digitalEye import Objects as obj
from digitalEye import Recog as rec
import sys
import cv2
import os

def onTeacher(request):
      return Teacher.objects.get(emailId=request.session.get('teacher'))

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



def history(request):
    teacher=onTeacher(request)
    attendanceList=Attendance.objects.filter(teacher=teacher)
    print attendanceList[0].teacher
    return render(request,'home/history.html',{'attendanceList':attendanceList,'user':teacher})


def startcapturing(request):
      #cap=cv2.VideoCapture("http://10.42.0.41:8080/video")
      #print cap
      hk=0
      course=request.POST.get('course')
      branch=request.POST.get('branch')
      batch=request.POST.get('batch')
      students=Student.objects.filter(course__iexact=course,branch__iexact=branch,batch__iexact=batch) # __iexact ignore case

      images=[]
      lables=[]
      for student in students:
          for image in student.imagedata_set.all():
              lables.append(int(student.rollNumber))
              img='media/%s' % image
              img=cv2.imread(img)
              img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
              images.append(img)
      print images
      print lables

      recog = rec.Recognizer()
      recog1 = rec.Recognizer()
      recog2 = rec.Recognizer()
      recog.train(images,lables,0)
      recog1.train(images,lables,1)
      recog2.train(images,lables,2)


      """
      while(hk<=1000):
         hk+=1
         print hk
         ret,frame=cap.read()
         if not ret: continue
         cv2.imshow('frame',frame)
         cv2.waitKey(1)
      cv2.destroyAllWindows()
      """
      return HttpResponse("ho gya")
