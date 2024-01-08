from django.db import models
from django.contrib.auth.models import User
from django import forms 
class User(models.Model):
    firstname = models.CharField(max_length=100,default="null")
    lastname = models.CharField(max_length=100,default="null")
    phone=models.CharField(max_length=10,default="0000000000")
    dob=models.CharField(max_length=10,default="00-00-0000")
    college=models.CharField(max_length=200,default="null")
    email = models.EmailField(max_length=254,default="null")
    password = models.CharField(max_length=100,default="null")
    coins = models.IntegerField(default=0)
    def __str__(self):
        return self.firstname
    
class Quiz_Info(models.Model):
    q_name=models.CharField(max_length=255,default="NULL")
    q1=models.CharField(max_length=255,default="Null")
    op1_1=models.CharField(max_length=255,default="Null")
    op2_1=models.CharField(max_length=255,default="Null")
    op3_1=models.CharField(max_length=255,default="Null")
    op4_1=models.CharField(max_length=255,default="Null")
    ans_1=models.CharField(max_length=255,default="Null")
    
    q2=models.CharField(max_length=255,default="Null")
    op1_2=models.CharField(max_length=255,default="Null")
    op2_2=models.CharField(max_length=255,default="Null")
    op3_2=models.CharField(max_length=255,default="Null")
    op4_2=models.CharField(max_length=255,default="Null")
    ans_2=models.CharField(max_length=255,default="Null")


    q3=models.CharField(max_length=255,default="Null")
    op1_3=models.CharField(max_length=255,default="Null")
    op2_3=models.CharField(max_length=255,default="Null")
    op3_3=models.CharField(max_length=255,default="Null")
    op4_3=models.CharField(max_length=255,default="Null")
    ans_3=models.CharField(max_length=255,default="Null")

class Quiz_Results(models.Model):
    stu_id=models.ForeignKey(User,on_delete=models.CASCADE)
    q_score = models.IntegerField(default=0)
    q_time = models.IntegerField(default=0)
    quizz_id=models.ForeignKey(Quiz_Info,on_delete=models.CASCADE)
    
class Quiz_Attempts(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    quiz_id=models.ForeignKey(Quiz_Info,on_delete=models.CASCADE)
class HTML(models.Model):
    user_id=models.IntegerField(default="null")
    
class Java(models.Model):
    user_id=models.IntegerField(default="null")
    
class Js(models.Model):
    user_id=models.IntegerField(default="null")
    
class StudentForm(forms.Form):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    subject=forms.CharField(max_length=255,required=True)
    date=forms.DateField()
    email = forms.EmailField(max_length=100, required=True)
    file = forms.FileField()

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if not first_name.isalpha():
            raise forms.ValidationError('First name should contain only alphabets.')
        return first_name