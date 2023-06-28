from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views



urlpatterns = [

    # Shared URL's
    path('', views.login_form, name='home'),
    path('login/', views.loginView, name='login'),
    path('logout/', views.logoutView, name='logout'),
    path('regform/', views.register_form, name='regform'),
    path('register/', views.registerView, name='register'),

    # Librarian URL's
    path('librarian/', views.librarian, name='librarian'),
    path('labook_form/', views.labook_form, name='labook_form'),
    path('labook/', views.labook, name='labook'),
    path('llbook/', views.LBookListView.as_view(), name='llbook'),
    # path('ldrequest/', views.LDeleteRequest.as_view(), name='ldrequest'),
    path('lsearch/', views.lsearch, name='lsearch'),
    path('ldbook/<int:pk>', views.LDeleteBook.as_view(), name='ldbook'),
    path('lmbook/', views.LManageBook.as_view(), name='lmbook'),
    path('ldbookk/<int:pk>', views.LDeleteView.as_view(), name='ldbookk'),
    path('lvbook/<int:pk>', views.LViewBook.as_view(), name='lvbook'),
    path('lebook/<int:pk>', views.LEditView.as_view(), name='lebook'),
    # path('lcchat/', views.LCreateChat.as_view(), name='lcchat'),
    # path('llchat/', views.LListChat.as_view(), name='llchat'),

    path('confirm-download/<int:pk>/', views.confirm_download, name='confirm-download'),
    path('udbook/<int:pk>/', views.udbook, name='udbook'),

    # Publisher URL's
    # path('ucchat/', views.UCreateChat.as_view(), name='ucchat'),
    # path('ulchat/', views.UListChat.as_view(), name='ulchat'),
    # path('delete_request/', views.delete_request, name='delete_request'),
    # path('send_feedback/', views.send_feedback, name='send_feedback'),
    path('abstract/<int:pk>/', views.abstract, name='abstract'),
    path('publisher/', views.UBookListView.as_view(), name='publisher'),
    path('uabook_form/', views.uabook_form, name='uabook_form'),
    path('uabook/', views.uabook, name='uabook'),
    path('request_form/', views.request_form, name='request_form'),
    path('feedback_form/', views.feedback_form, name='feedback_form'),
    path('department/', views.department, name='department'),
    path('major/', views.major, name='major'),
    path('about/', views.about, name='about'),
    path('usearch/', views.usearch, name='usearch'),

    # Admin URL's
    path('dashboard/', views.dashboard, name='dashboard'),
    # path('acchat/', views.ACreateChat.as_view(), name='acchat'),
    # path('alchat/', views.AListChat.as_view(), name='alchat'),
    path('aabook_form/', views.aabook_form, name='aabook_form'),
    path('aabook/', views.aabook, name='aabook'),
    path('albook/', views.ABookListView.as_view(), name='albook'),
    path('ambook/', views.AManageBook.as_view(), name='ambook'),
    path('adbook/<int:pk>', views.ADeleteBook.as_view(), name='adbook'),
    path('avbook/<int:pk>', views.AViewBook.as_view(), name='avbook'),
    path('aebook/<int:pk>', views.AEditView.as_view(), name='aebook'),
    # path('adrequest/', views.ADeleteRequest.as_view(), name='adrequest'),
    # path('afeedback/', views.AFeedback.as_view(), name='afeedback'),
    path('asearch/', views.asearch, name='asearch'),
    path('adbookk/<int:pk>', views.ADeleteBookk.as_view(), name='adbookk'),
    path('create_user_form/', views.create_user_form, name='create_user_form'),
    path('create_teacher_form/', views.create_teacher_form, name='create_teacher_form'),
    path('create_student_form/', views.create_student_form, name='create_student_form'),
    path('aluser/', views.ListUserView.as_view(), name='aluser'),
    path('alteacher/', views.ListTeacherView.as_view(), name='alteacher'),
    path('alstudent/', views.ListStudentView.as_view(), name='alstudent'),
    path('create_use/', views.create_user, name='create_user'),
    path('create_teacher/', views.create_teacher, name='create_teacher'),
    path('create_student/', views.create_student, name='create_student'),
    path('alvuser/<int:pk>', views.ALViewUser.as_view(), name='alvuser'),
    path('alvteacher/<int:pk>', views.ALViewTeacher.as_view(), name='alvteacher'),
    path('alvstudent/<int:pk>', views.ALViewStudent.as_view(), name='alvstudent'),
    path('aeteacher/<int:pk>', views.AEditTeacher.as_view(), name='aeteacher'),
    path('aestudent/<int:pk>', views.AEditStudent.as_view(), name='aestudent'),
    path('aeuser/<int:pk>', views.AEditUser.as_view(), name='aeuser'),
    path('adteacher/<int:pk>', views.ADeleteTeacher.as_view(), name='adteacher'),
    path('adstudent/<int:pk>', views.ADeleteStudent.as_view(), name='adstudent'),
    path('aduser/<int:pk>', views.ADeleteUser.as_view(), name='aduser'),
]