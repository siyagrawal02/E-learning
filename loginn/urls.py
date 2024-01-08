from django.urls import path
from . import views



urlpatterns = [
    path('home/', views.home,name='home'),
    path('signup/', views.signup,name='signup'),
    path('signup/login/signup/', views.signup,name='signup'),
    path('signup/login/', views.login,name='login'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('verify_otp/', views.verify_otp, name='verify_otp'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('quiz/', views.quiz, name='quiz'),
    path('files/', views.my_view, name='my_view'),
    path('download/<str:file_name>/', views.download_file, name='download_file'),
    path('upload/', views.upload,name='upload'),  
    path('dashboard/<int:user_id>/',views.dashboard,name='dashboard'),
    path('home_after_login/<int:user_id>/',views.dashboard,name='home_after_login'),
    path('course1/<int:user_id>',views.course1,name="course1"),
    path('course2/<int:user_id>',views.course2,name="course2"),
    path('course3/<int:user_id>',views.course3,name="course3"),
    path('enroll/',views.enroll,name="enroll"),
    path('delete/<str:file_name>/', views.delete_file, name='delete_file'),
    path('teacherportal/',views.teacherportal,name='teacherportal'),
    path('add_mcq_questions/', views.add_mcq_questions, name='add'),
    path('quiz_list/<int:id>/', views.quiz_list, name='quiz_list'),
    path('quizView/', views.quizView, name='quizView'),
    path('quiz/<int:quiz_id>/', views.quiz, name='quiz'),
    path('result_table/<int:id>/', views.result_table, name='result_table'),
    path('admin_portal/', views.admin_portal, name='admin_portal'),
    path('quiz_list_admin/', views.quiz_list_admin, name='quiz_list_admin'),
    path('reward/', views.reward, name='reward'),
    path('voucher/', views.voucher, name='voucher'),
    path('update_coins/', views.update_coins, name='update_coins'),

    path('summary/',views.summary,name='summary')

]

