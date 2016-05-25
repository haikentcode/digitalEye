from __future__ import unicode_literals
from django.db import models
from django.contrib import admin
from datetime import datetime

from string import join
import os
import uuid
Image_Folder="media/"

class Teacher(models.Model):
    firstName=models.CharField(max_length=50)
    lastName=models.CharField(max_length=50)
    emailId=models.EmailField(blank=False,null=False,primary_key=True)
    contactNo=models.CharField(max_length=10)
    password=models.CharField(max_length=50)
    image = models.ImageField(upload_to=Image_Folder, null = True)

    def image_tag(self):
          return u'<img src="/media/%s" width="100px" height="100px"/>' % self.image
    image_tag.short_description = 'Item Image'
    image_tag.allow_tags = True

    def __str__(self):
        return "%s %s %s"%(self.firstName,self.lastName,self.emailId)

    class Admin:
        pass

class Student(models.Model):
     rollNumber = models.CharField(max_length=50,blank=True,null=True)
     branch =  models.CharField(max_length=50)
     batch = models.CharField(max_length=50)
     course = models.CharField(max_length=50)
     date = models.DateField(blank=True,null=True)

     def __str__(self):
        return "%s" % (self.rollNumber)

     class Admin:
        pass

class ImageData(models.Model):
    image = models.ImageField(upload_to=Image_Folder, null = True)
    student = models.ForeignKey(Student)
    def image_tag(self):
          return u'<img src="/media/%s" width="100px" height="100px"/>' % self.image
    image_tag.short_description = 'Item Image'
    image_tag.allow_tags = True
    def __str__(self):
       return "%s" % (self.image)

class Attendance(models.Model):
    students = models.ManyToManyField(Student)
    teacher = models.ForeignKey(Teacher)
    date = models.DateField(auto_now_add=True,blank=True,null=True)

class Log(models.Model):
      text=models.CharField(max_length=1000,blank=True,null=True)
      def __str__(self):
         return "%s" % (self.text)
