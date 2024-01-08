from django.shortcuts import get_object_or_404,render,redirect
from django.http import HttpResponse
from .models import User,HTML,Java,Js,Quiz_Attempts,Quiz_Info,Quiz_Results
from django.http import JsonResponse
from django.template import loader
from django.core.mail import send_mail,BadHeaderError
from django.conf import settings
import random
import json
from django.contrib import messages
from loginn.functions import handle_uploaded_file  
from loginn.forms import StudentForm 
import os
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'static'))
upload_dir = os.path.join(static_dir, 'filesuploaded')

def download_file(request, file_name):
    file_path = os.path.join(upload_dir, file_name)
    
    # Check if the file exists
    if not os.path.exists(file_path):
        return HttpResponse(f"{file_name} not found.", status=404)
    
    # Open the file in read-only binary mode
    with open(file_path, 'rb') as file:
        # Create an HTTP response with the file as the content
        response = HttpResponse(file.read())
        # Set the Content-Disposition header to force the browser to download the file
        response['Content-Disposition'] = f'attachment; filename="{file_name}"'
        # Set the Content-Type header to the correct MIME type for the file
        response['Content-Type'] = 'application/octet-stream'
        return response
def my_view(request):
    file_names = os.listdir(upload_dir)
    file_info = []

    for name in file_names:
        try:
            with open(os.path.join(upload_dir, f"{name}.txt"), 'r') as file_info_file:
                file_info_dict = {'name': name}
                for line in file_info_file:
                    key, value = line.strip().split(': ')
                    file_info_dict[key.lower()] = value
                file_info.append(file_info_dict)
                
        except FileNotFoundError:
            # If the text file does not exist, skip this file
            continue

    # Render the template with the file info
    return render(request, 'files.html', {'files': file_info})

@csrf_exempt
def upload(request):  
    if request.method == 'POST':  
        student = StudentForm(request.POST, request.FILES)  
        if student.is_valid():  
            first_name = request.POST.get('firstname')
            last_name = request.POST.get('lastname')
            subject=request.POST.get('subject')
            date=request.POST.get('date')
            email = request.POST.get('email')
        
            handle_uploaded_file(request.FILES['file'], first_name, last_name, subject,date,email)
            template=loader.get_template('success.html')

            context={
            'msg':"File uploaded successfuly"
            }
            return HttpResponse(template.render(context,request))
       
     
    student = StudentForm()  
    return render(request,"admin.html",{'form':student})
    
def delete_file(request, file_name):
    file_path = os.path.join(upload_dir, file_name)
    
    # Check if the file exists
    if os.path.exists(file_path):
        os.remove(file_path)
        
    # Redirect back to my_view to update the file list
    return redirect('my_view')

def handle_uploaded_file(file, first_name, last_name,subject,date, email):
    file_path = os.path.join(upload_dir, file.name)
    with open(file_path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    # save first name, last name, and email with the uploaded file
    file_info = {'name': file.name, 'first_name': first_name, 'last_name': last_name, 'subject':subject,'date':date,'email': email}
    with open(os.path.join(upload_dir, f"{file.name}.txt"), 'w') as file_info_file:
        for key, value in file_info.items():
            file_info_file.write(f"{key.capitalize()}: {value}\n")


        
def signup(request):
    if request.method == 'POST':
        # Get the form data from the request object
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        phone=request.POST.get('phone')
        dob=request.POST.get('dob')
        college=request.POST.get('college')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Insert the form data into the database using a model
        
        user = User(firstname=firstname, lastname=lastname, phone=phone, dob=dob,college=college,email=email, password=password)
        user.save()

        # Render a success message to the user
        template=loader.get_template('success.html')

        context={
            'msg':"Thanks For Signing Up!!"
            }
        return HttpResponse(template.render(context,request))
    
    return render(request,"signup.html")

def home(request):
    template=loader.get_template('home.html')
    return HttpResponse(template.render())



def login(request):
    template=loader.get_template('home_after_login.html')
    if request.method == 'POST':
        email = request.POST.get('uname')
        password = request.POST.get('password')
        user_type = request.POST.get('type')
        try:
            user = User.objects.get(email=email, password=password)
            id=user.id
            context={
                'id':id
            }
            if user_type == 'student':
                return HttpResponse(template.render(context,request))
            elif user_type == 'teacher':
                return redirect('teacherportal')
            elif user_type == 'admin':
                return redirect('admin_portal')
            
        except User.DoesNotExist:
            return render(request,'login.html',{'message': 'Invalid credentials. Please try again.'})        
    return render(request,'login.html')

def teacherportal(request):
    template=loader.get_template('teacherportal.html')
    return HttpResponse(template.render())
def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        # Check if user with this email exists
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'There is no user with this email address.')
            return render(request, 'forgot_password.html')
        # Generate OTP
        otp = str(random.randint(100000, 999999))
        # Store OTP in session
        request.session['otp'] = otp
        request.session['email'] = email
        # Send OTP to user's email
        subject = 'OTP for password reset'
        message = f'Your OTP for password reset is {otp}. Do not share it with anyone.'
        from_email = "sia2121181@sicsr.ac.in"
        recipient_list = [email]
        print(subject," ",message," ",from_email," ",recipient_list)
        try:
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)
            print('Email sent successfully!')
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        # Redirect to verify OTP view
        return redirect('verify_otp')
    return render(request, 'forgot_password.html')

def verify_otp(request):
    if request.method == 'POST':
        entered_otp = request.POST['otp']
        stored_otp = request.session.get('otp')
        if entered_otp == stored_otp:
            # OTP is valid, allow user to reset their password
            # Get user's email from session
            email = request.session.get('email')
            # Remove stored OTP and email from session
        
            # Redirect to reset password view
            messages.success(request, 'OTP verified. Please enter a new password.')
            return redirect('reset_password')
        else:
            # OTP is invalid, show an error message
            messages.error(request, 'Invalid OTP. Please try again.')
    return render(request, 'verify_otp.html')

def reset_password(request):
    if request.method == 'POST':
        email = request.session.get('email')
        # Get user with this email
        user = User.objects.get(email=email)
        if user:
        # Set new password
            new_password = request.POST.get('new_password2')
            user.password=new_password
            user.save()
        # Authenticate and login user
            user = User.objects.get(email=email, password=new_password)
            print(user)
            if user:
                return redirect('login')
        else:
            messages.error(request, 'User with the given email does not exist.')
    return render(request, 'reset_password.html')

def quiz(request):
    template=loader.get_template('quiz.html')
    return HttpResponse(template.render())  
    
def dashboard(request, user_id):
    
    user = User.objects.get(id=user_id)
    course1=""
    course2=""
    course3=""
    course_count=0
    if(HTML.objects.filter(user_id=user_id).exists()):
        course1+="Introduction to HTML"
        course_count+=1
    
    if(Java.objects.filter(user_id=user_id).exists()):
        course2+="Object oriented programming: Java"
        course_count+=1
    if(Js.objects.filter(user_id=user_id).exists()):
        course3+="Basics of JavaScript"
        course_count+=1
    # fetch details from MySQL database using the user object
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM loginn_user WHERE id = %s", [user.id])
        details = cursor.fetchall()
    quiz_attempts = Quiz_Attempts.objects.filter(user_id=user_id)
    quiz_attempted = set([attempt.quiz_id for attempt in quiz_attempts])
    total_count=len(quiz_attempted)
    total_quiz=Quiz_Info.objects.count()
    
    request.session['id']=user_id
    total_coins=user.coins
    context={'total_count':total_count,
            'total_quiz':total_quiz,
            'total_coins':total_coins,
            'user': user, 'details': details,'course1':course1,'course2':course2,'course3':course3,'course_count':course_count}
    # pass the details to the template
    return render(request, 'dashboard.html', context)

def home_after_login(request,user_id):
    request.session['id']=user_id
    template=loader.get_template('home_after_login.html')
    return HttpResponse(template.render())


def course1(request,user_id):
    template=loader.get_template('course1.html')
    id=request.session.get('id')
    context={
        'id':id
    }
    return HttpResponse(template.render(context,request))

def course2(request,user_id):
    template=loader.get_template('course2.html')
    id=request.session.get('id')
    context={
        'id':id
    }
    return HttpResponse(template.render(context,request))
def course3(request,user_id):
    template=loader.get_template('course3.html') 
    id=request.session.get('id')
    context={
        'id':id
    }
    return HttpResponse(template.render(context,request))

@csrf_exempt
def enroll(request):
    template=loader.get_template('success.html')
    error=loader.get_template('error.html')
    context={
        'msg':"Enrolled successfully!!"
        }
    
    if request.method == 'POST':
        sub=request.POST.get('sub')
        id=request.POST.get('id')
        if sub=='HTML':
            if HTML.objects.filter(user_id=id).exists():
                return HttpResponse(error.render())
            else:
                html=HTML(user_id=id)
                html.save()
        if sub=='Java':
            if Java.objects.filter(user_id=id).exists():
                return HttpResponse(error.render())
            else:
                jav=Java(user_id=id)
                jav.save()
        if sub=='Js':
            if Js.objects.filter(user_id=id).exists():
                return HttpResponse(error.render())
            else:
                js=Js(user_id=id)
                js.save()
    return HttpResponse(template.render(context,request))

def admin_portal(request):
    template=loader.get_template('admin_portal.html')
    return HttpResponse(template.render())
    
def quiz_list_admin(request):
    
    quizzes = Quiz_Info.objects.all()
    template=loader.get_template('quiz_list_admin.html')
    context={
        'quiz':quizzes    
    }
    return HttpResponse(template.render(context,request))    

def reward(request):
    id = request.session.get('id')
    results = Quiz_Results.objects.filter(quizz_id=id).order_by('q_time', '-q_score')[:3]
    if request.method == 'POST':
        if results:
            results[0].stu_id.coins += 20  # Add 20 coins to rank 1
            results[0].stu_id.save()
            if len(results) >= 2:
                results[1].stu_id.coins += 10  # Add 10 coins to rank 2
                results[1].stu_id.save()
            if len(results) >= 3:
                results[2].stu_id.coins += 5  # Add 5 coins to rank 3
                results[2].stu_id.save()
        
        # Set a flag in the session to disable the button on the next render
        request.session['disable_button'] = True
    
    return redirect('result_table', id=id)



    
def result_table(request, id):
    request.session['id'] = id
    results = Quiz_Results.objects.filter(quizz_id=id).order_by('q_time', '-q_score')[:3]
    
    # Determine whether the button should be disabled
    disable_button = False
    if 'disable_button' in request.session:
        disable_button = request.session['disable_button']
        del request.session['disable_button']  # Clear the flag from the session
    
    context = {
        'results': results,
        'disable_button': disable_button,  # Pass the flag to the template
    }
    template = loader.get_template('result_table.html')
    return HttpResponse(template.render(context, request))

@csrf_exempt
def update_coins(request):
    print('request received')
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            id = data['user_id']
            req_coins = data['required_coins']
            user = User.objects.get(id=id)
            user.coins -= req_coins
            user.save()
            return JsonResponse({'success': True})
        except (json.decoder.JSONDecodeError, KeyError) as e:
            return JsonResponse({'success': False, 'error': str(e)})
        
def voucher(request):
    login_id=request.session.get('id')
    user=User.objects.get(id=login_id)
    total_coins=user.coins
    context={
        'total_coins':total_coins,
        'login_id':login_id
    }
    return render(request,'voucher.html',context)
@csrf_exempt
def quizView(request):
    print("request received")
    user_id=request.session.get('login_id')
    quiz_id=request.session.get('quiz_id')
    user=User.objects.get(id=user_id)
    quiz=Quiz_Info.objects.get(id=quiz_id)
    attempt=Quiz_Attempts(user=user,quiz_id=quiz)
    attempt.save()
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            score = data['score']
            totalTime = data['total_quiz_time']
            # Create a new quiz object with the data
            new_quiz = Quiz_Results(stu_id=user,q_score=score, q_time=totalTime,quizz_id=quiz)
            # Save the quiz object to the database
            new_quiz.save()
            return JsonResponse({'success': True})
        except (json.decoder.JSONDecodeError, KeyError) as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return render(request, 'quiz.html')


def add_mcq_questions(request):

    if request.method == 'POST':

        q_name = request.POST.get('qname')
        q1 = request.POST.get('question1')
        op1_1 = request.POST.get('option1_1')
        op2_1 = request.POST.get('option2_1')
        op3_1 = request.POST.get('option3_1')
        op4_1 = request.POST.get('option4_1')
        ans_1 = request.POST.get('correct_answer1')

        q2 = request.POST.get('question2')
        op1_2 = request.POST.get('option1_2')
        op2_2 = request.POST.get('option2_2')
        op3_2 = request.POST.get('option3_2')
        op4_2 = request.POST.get('option4_2')
        ans_2 = request.POST.get('correct_answer2')

        q3 = request.POST.get('question3')
        op1_3 = request.POST.get('option1_3')
        op2_3 = request.POST.get('option2_3')
        op3_3 = request.POST.get('option3_3')
        op4_3 = request.POST.get('option4_3')
        ans_3 = request.POST.get('correct_answer3')

        quiz_data = Quiz_Info(q_name=q_name, q1=q1, op1_1=op1_1, op2_1=op2_1, op3_1=op3_1, op4_1=op4_1, ans_1=ans_1, q2=q2, op1_2=op1_2,
                            op2_2=op2_2, op3_2=op3_2, op4_2=op4_2, ans_2=ans_2, q3=q3, op1_3=op1_3, op2_3=op2_3, op3_3=op3_3, op4_3=op4_3, ans_3=ans_3)
        quiz_data.save()
        template=loader.get_template('success.html')
        context={
        'msg':"QUIZ SAVED."
        }
        return HttpResponse(template.render(context,request))
    return render(request, 'quiz_creation.html')


def quiz_list(request, id):
    login_id = id
    request.session['login_id'] = login_id
    quizzes = Quiz_Info.objects.all()

    # Check if user has attempted the quiz
    quiz_attempts = Quiz_Attempts.objects.filter(user_id=login_id)
    quiz_attempted = set([attempt.quiz_id for attempt in quiz_attempts])
    total_count=len(quiz_attempted)
    context = {'quizzes': quizzes,
            'login_id': login_id,
            'count':total_count}
    context['quiz_attempted'] = quiz_attempted

    return render(request, 'quiz_list.html', context)


def quiz(request, quiz_id):
    login_id=request.session.get('login_id')
    request.session['user_id']=login_id    
    request.session['quiz_id']=quiz_id    
    quiz = get_object_or_404(Quiz_Info, id=quiz_id)
    context = {'quiz': quiz,
            'login_id':login_id}
    return render(request, 'quiz.html', context)


def summary(request):
    template=loader.get_template('OnePageSummary.html')
    return HttpResponse(template.render())