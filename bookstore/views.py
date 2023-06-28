from django.shortcuts import redirect, render
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views import generic
from bootstrap_modal_forms.mixins import PassRequestMixin
from .models import User, Book
from django.contrib import messages
from django.db.models import Sum
from django.views.generic import CreateView, DetailView, DeleteView, UpdateView, ListView
from .forms import BookForm, UserForm
from . import models
import operator
import itertools
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, logout
from django.contrib import auth, messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.db.models import Q




# Shared Views
def login_form(request):
    return render(request, 'bookstore/login.html')


def logoutView(request):
    logout(request)
    return redirect('home')


def loginView(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            if user.is_admin or user.is_superuser:
                return redirect('dashboard')
            elif user.is_librarian:
                return redirect('librarian')
            else:
                return redirect('publisher')
        else:
            messages.info(request, "Invalid username or password")
            return redirect('home')


def register_form(request):
    return render(request, 'bookstore/register.html')


def registerView(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password = make_password(password)

        a = User(username=username, email=email, password=password, is_publisher=True)
        a.save()
        messages.success(request, 'Account was created successfully')
        return redirect('home')
    else:
        messages.error(request, 'Registration fail, try again later')
        return redirect('regform')


# Publisher views
@login_required
def publisher(request):
    return render(request, 'publisher/home.html')


@login_required
def uabook_form(request):
    return render(request, 'publisher/add_book.html')


@login_required
def request_form(request):
    return render(request, 'publisher/delete_request.html')


@login_required
def feedback_form(request):
    return render(request, 'publisher/send_feedback.html')


@login_required
def department(request):
    deps = models.Department.objects.all()
    return render(request, 'publisher/department.html', {'deps': deps})


@login_required
def major(request):
    majors = models.Major.objects.all()
    return render(request, 'publisher/major.html', {'majors': majors})


@login_required
def about(request):
    return render(request, 'publisher/about.html')	


@login_required
def confirm_download(request, pk):
    pk = pk
    return render(request, 'publisher/confirm_download.html', {'pk': pk})


@login_required
def usearch(request):
    query = request.GET['query']
    print(type(query))

    #data = query.split()
    data = query
    print(len(data))
    if( len(data) == 0):
        return redirect('publisher')
    else:
        a = data

        # Searching for It
        qs5 = models.Book.objects.filter(id__iexact=a).distinct()
        qs6 = models.Book.objects.filter(id__exact=a).distinct()

        qs7 = models.Book.objects.all().filter(id__contains=a)
        qs8 = models.Book.objects.select_related().filter(id__contains=a).distinct()
        qs9 = models.Book.objects.filter(id__startswith=a).distinct()
        qs10 = models.Book.objects.filter(id__endswith=a).distinct()
        qs11 = models.Book.objects.filter(id__istartswith=a).distinct()
        qs12 = models.Book.objects.all().filter(id__icontains=a)
        qs13 = models.Book.objects.filter(id__iendswith=a).distinct()

        files = itertools.chain(qs5, qs6, qs7, qs8, qs9, qs10, qs11, qs12, qs13)

        res = []
        for i in files:
            if i not in res:
                res.append(i)

        # word variable will be shown in html when user click on search button
        word="Searched Result :"
        print("Result")

        print(res)
        files = res

        page = request.GET.get('page', 1)
        paginator = Paginator(files, 10)
        try:
            files = paginator.page(page)
        except PageNotAnInteger:
            files = paginator.page(1)
        except EmptyPage:
            files = paginator.page(paginator.num_pages)

        if files:
            return render(request,'publisher/result.html',{'files':files,'word':word})
        return render(request,'publisher/result.html',{'files':files,'word':word})


# @login_required
# def delete_request(request):
#     if request.method == 'POST':
#         book_id = request.POST['delete_request']
#         current_user = request.user
#         user_id = current_user.id
#         username = current_user.username
#         user_request = username + "  want book with id  " + book_id + " to be deleted"

#         a = DeleteRequest(delete_request=user_request)
#         a.save()
#         messages.success(request, 'Request was sent')
#         return redirect('request_form')
#     else:
#         messages.error(request, 'Request was not sent')
#         return redirect('request_form')


# @login_required
# def send_feedback(request):
#     if request.method == 'POST':
#         feedback = request.POST['feedback']
#         current_user = request.user
#         user_id = current_user.id
#         username = current_user.username
#         feedback = username + " " + " says " + feedback

#         a = Feedback(feedback=feedback)
#         a.save()
#         messages.success(request, 'Feedback was sent')
#         return redirect('feedback_form')
#     else:
#         messages.error(request, 'Feedback was not sent')
#         return redirect('feedback_form')


class UBookListView(LoginRequiredMixin,ListView):
    model = Book
    template_name = 'publisher/book_list.html'
    context_object_name = 'books'
    paginate_by = 10

    def get_queryset(self):
        return Book.objects.order_by('-id')

@login_required
def uabook(request):
    if request.method == 'POST':
        title = request.POST['title']
        author = request.POST['author']
        year = request.POST['year']
        publisher = request.POST['publisher']
        desc = request.POST['desc']
        cover = request.FILES['cover']
        pdf = request.FILES['pdf']
        current_user = request.user
        user_id = current_user.id
        username = current_user.username

        a = Book(title=title, author=author, year=year, publisher=publisher, 
            desc=desc, cover=cover, pdf=pdf, uploaded_by=username, user_id=user_id)
        a.save()
        messages.success(request, 'Book was uploaded successfully')
        return redirect('publisher')
    else:
        messages.error(request, 'Book was not uploaded successfully')
        return redirect('uabook_form')	


@login_required
def udbook(request, pk):
    if request.method == 'POST':
        price = float(request.POST['price'])
        amount = float(request.POST['amount'])
        bin_img = request.FILES['qr']
        current_user = request.user
        user_id = current_user.id
        username = current_user.username
        thesis = Book.objects.get(pk=pk)

        download = models.Download(price=price, thesis_amount=amount, user=current_user, thesis=thesis)
        payment = models.Payment(total_amount=price, bin_img=bin_img, download=download)
        download.save()
        payment.save()
        messages.success(request, 'Book was downloaded successfully')
        pdf_url = f'http://localhost:8000{thesis.pdf.url}'
        return redirect(pdf_url)
    else:
        messages.error(request, 'Book was not downloaded successfully')
        return redirect('confirm-download')	


# class UCreateChat(LoginRequiredMixin, CreateView):
#     form_class = ChatForm
#     model = Chat
#     template_name = 'publisher/chat_form.html'
#     success_url = reverse_lazy('ulchat')

#     def form_valid(self, form):
#         self.object = form.save(commit=False)
#         self.object.user = self.request.user
#         self.object.save()
#         return super().form_valid(form)


# class UListChat(LoginRequiredMixin, ListView):
#     model = Chat
#     template_name = 'publisher/chat_list.html'

#     def get_queryset(self):
#         return Chat.objects.filter(posted_at__lt=timezone.now()).order_by('posted_at')


# Librarian views
def librarian(request):
    book = Book.objects.all().count()
    user = User.objects.all().count()
    downloads = models.Download.objects.all().count()

    context = {'book':book, 'user':user, 'downloads': downloads}

    return render(request, 'librarian/home.html', context)


@login_required
def labook_form(request):
    return render(request, 'librarian/add_book.html')


@login_required
def labook(request):
    if request.method == 'POST':
        title = request.POST['title']
        author = request.POST['author']
        year = request.POST['year']
        publisher = request.POST['publisher']
        desc = request.POST['desc']
        cover = request.FILES['cover']
        pdf = request.FILES['pdf']
        current_user = request.user
        user_id = current_user.id
        username = current_user.username

        a = Book(title=title, author=author, year=year, publisher=publisher, 
            desc=desc, cover=cover, pdf=pdf, uploaded_by=username, user_id=user_id)
        a.save()
        messages.success(request, 'Book was uploaded successfully')
        return redirect('llbook')
    else:
        messages.error(request, 'Book was not uploaded successfully')
        return redirect('llbook')


class LBookListView(LoginRequiredMixin,ListView):
    model = Book
    template_name = 'librarian/book_list.html'
    context_object_name = 'books'
    paginate_by = 10

    def get_queryset(self):
        return Book.objects.order_by('-id')


class LManageBook(LoginRequiredMixin,ListView):
    model = Book
    template_name = 'librarian/manage_books.html'
    context_object_name = 'books'
    paginate_by = 10

    def get_queryset(self):
        return Book.objects.order_by('-id')


# class LDeleteRequest(LoginRequiredMixin,ListView):
#     model = DeleteRequest
#     template_name = 'librarian/delete_request.html'
#     context_object_name = 'feedbacks'
#     paginate_by = 3

#     def get_queryset(self):
#         return DeleteRequest.objects.order_by('-id')


class LViewBook(LoginRequiredMixin,DetailView):
    model = Book
    template_name = 'librarian/book_detail.html'

    
class LEditView(LoginRequiredMixin,UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'librarian/edit_book.html'
    success_url = reverse_lazy('lmbook')
    success_message = 'Data was updated successfully'


class LDeleteView(LoginRequiredMixin,DeleteView):
    model = Book
    template_name = 'librarian/confirm_delete.html'
    success_url = reverse_lazy('lmbook')
    success_message = 'Data was deleted successfully'


class LDeleteBook(LoginRequiredMixin,DeleteView):
    model = Book
    template_name = 'librarian/confirm_delete2.html'
    success_url = reverse_lazy('librarian')
    success_message = 'Data was dele successfully'


@login_required
def lsearch(request):
    query = request.GET['query']
    print(type(query))

    #data = query.split()
    data = query
    print(len(data))
    if( len(data) == 0):
        return redirect('publisher')
    else:
        a = data

        # Searching for It
        qs5 =models.Book.objects.filter(id__iexact=a).distinct()
        qs6 =models.Book.objects.filter(id__exact=a).distinct()

        qs7 =models.Book.objects.all().filter(id__contains=a)
        qs8 =models.Book.objects.select_related().filter(id__contains=a).distinct()
        qs9 =models.Book.objects.filter(id__startswith=a).distinct()
        qs10 =models.Book.objects.filter(id__endswith=a).distinct()
        qs11 =models.Book.objects.filter(id__istartswith=a).distinct()
        qs12 =models.Book.objects.all().filter(id__icontains=a)
        qs13 =models.Book.objects.filter(id__iendswith=a).distinct()

        files = itertools.chain(qs5, qs6, qs7, qs8, qs9, qs10, qs11, qs12, qs13)

        res = []
        for i in files:
            if i not in res:
                res.append(i)

        # word variable will be shown in html when user click on search button
        word="Searched Result :"
        print("Result")

        print(res)
        files = res

        page = request.GET.get('page', 1)
        paginator = Paginator(files, 10)
        try:
            files = paginator.page(page)
        except PageNotAnInteger:
            files = paginator.page(1)
        except EmptyPage:
            files = paginator.page(paginator.num_pages)

        if files:
            return render(request,'librarian/result.html',{'files':files,'word':word})
        return render(request,'librarian/result.html',{'files':files,'word':word})


# class LCreateChat(LoginRequiredMixin, CreateView):
#     form_class = ChatForm
#     model = Chat
#     template_name = 'librarian/chat_form.html'
#     success_url = reverse_lazy('llchat')

#     def form_valid(self, form):
#         self.object = form.save(commit=False)
#         self.object.user = self.request.user
#         self.object.save()
#         return super().form_valid(form)


# class LListChat(LoginRequiredMixin, ListView):
#     model = Chat
#     template_name = 'librarian/chat_list.html'

#     def get_queryset(self):
#         return Chat.objects.filter(posted_at__lt=timezone.now()).order_by('posted_at')


# Admin views

def dashboard(request):
    book = Book.objects.all().count()
    user = User.objects.all().count()
    downloads = models.Download.objects.all().count()

    context = {'book':book, 'user':user, 'downloads': downloads}

    return render(request, 'dashboard/home.html', context)

def create_user_form(request):
    choice = ['1', '0', 'Publisher', 'Admin', 'Librarian']
    choice = {'choice': choice}

    return render(request, 'dashboard/add_user.html', choice)


def create_teacher_form(request):
    departments = models.Department.objects.all()

    return render(request, 'dashboard/add_teacher.html', {'departments': departments})


def create_student_form(request):
    majors = models.Major.objects.all()

    return render(request, 'dashboard/add_student.html', {'majors': majors})


class ADeleteUser(SuccessMessageMixin, DeleteView):
    model = User
    template_name='dashboard/confirm_delete3.html'
    success_url = reverse_lazy('aluser')
    success_message = "Data successfully deleted"


class ADeleteTeacher(SuccessMessageMixin, DeleteView):
    model = models.Teacher
    template_name='dashboard/confirm_delete4.html'
    success_url = reverse_lazy('alteacher')
    success_message = "Data successfully deleted"


class ADeleteStudent(SuccessMessageMixin, DeleteView):
    model = models.Student
    template_name='dashboard/confirm_delete5.html'
    success_url = reverse_lazy('alstudent')
    success_message = "Data successfully deleted"


class AEditTeacher(SuccessMessageMixin, UpdateView): 
    model = models.Teacher
    fields = ['full_name', 'gender', 'telephone', 'email', 'dep']
    template_name = 'dashboard/edit_teacher.html'
    success_url = reverse_lazy('alteacher')
    success_message = "Data successfully updated"


class AEditStudent(SuccessMessageMixin, UpdateView): 
    model = models.Student
    fields = [
        'full_name', 'gender', 'dob', 'village',
        'district', 'province', 'telephone', 'email', 'major'
    ]
    template_name = 'dashboard/edit_student.html'
    success_url = reverse_lazy('alstudent')
    success_message = "Data successfully updated"


class AEditUser(SuccessMessageMixin, UpdateView): 
    model = User
    # form_class = UserForm
    fields = ['username', 'first_name', 'last_name', 'email', 'is_publisher', 'is_librarian']
    template_name = 'dashboard/edit_user.html'
    success_url = reverse_lazy('aluser')
    success_message = "Data successfully updated"


class ListUserView(generic.ListView):
    model = User
    template_name = 'dashboard/list_users.html'
    context_object_name = 'users'
    paginate_by = 10

    def get_queryset(self):
        return User.objects.order_by('-id')


class ListTeacherView(generic.ListView):
    model = models.Teacher
    template_name = 'dashboard/list_teachers.html'
    context_object_name = 'teachers'
    paginate_by = 10


class ListStudentView(generic.ListView):
    model = models.Student
    template_name = 'dashboard/list_students.html'
    context_object_name = 'students'
    paginate_by = 10


def create_teacher(request):
    if request.method == 'POST':
        full_name=request.POST['full_name']
        gender=request.POST['gender']
        telephone=request.POST['telephone']
        email=request.POST['email']
        dep=request.POST['dep']

        # Retrieve the Department instance based on the dep_id
        department = get_object_or_404(models.Department, id=dep)

        teacher = models.Teacher(full_name=full_name, gender=gender, telephone=telephone, email=email, dep=department)
        teacher.save()
        messages.success(request, 'Teacher was created successfully!')
        return redirect('alteacher')
    else:
        return redirect('create_teacher_form')


def create_student(request):
    if request.method == 'POST':
        full_name=request.POST['full_name']
        gender=request.POST['gender']
        dob=request.POST['dob']
        village=request.POST['village']
        district=request.POST['district']
        province=request.POST['province']
        telephone=request.POST['telephone']
        email=request.POST['email']
        major=request.POST['major']

        # Retrieve the Major instance based on the dep_id
        major = get_object_or_404(models.Major, id=major)

        student = models.Student(
            full_name=full_name, gender=gender, dob=dob,
            village=village, district=district, province=province,
            telephone=telephone, email=email, major=major
        )
        student.save()
        messages.success(request, 'Student was created successfully!')
        return redirect('alstudent')
    else:
        return redirect('create_student_form')


def create_user(request):
    choice = ['1', '0', 'Publisher', 'Admin', 'Librarian']
    choice = {'choice': choice}
    if request.method == 'POST':
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        username=request.POST['username']
        userType=request.POST['userType']
        email=request.POST['email']
        password=request.POST['password']
        password = make_password(password)
        print("User Type")
        print(userType)

        if userType == "Publisher":
            a = User(first_name=first_name, last_name=last_name, username=username, email=email, password=password, is_publisher=True)
            a.save()
            messages.success(request, 'Member was created successfully!')
            return redirect('aluser')
        elif userType == "Admin":
            a = User(first_name=first_name, last_name=last_name, username=username, email=email, password=password, is_admin=True)
            a.save()
            messages.success(request, 'Member was created successfully!')
            return redirect('aluser')
        elif userType == "Librarian":
            a = User(first_name=first_name, last_name=last_name, username=username, email=email, password=password, is_librarian=True)
            a.save()
            messages.success(request, 'Member was created successfully!')
            return redirect('aluser')    
        else:
            messages.success(request, 'Member was not created')
            return redirect('create_user_form')
    else:
        return redirect('create_user_form')


class ALViewUser(DetailView):
    model = User
    template_name='dashboard/user_detail.html'


class ALViewTeacher(DetailView):
    model = models.Teacher
    template_name='dashboard/teacher_detail.html'


class ALViewStudent(DetailView):
    model = models.Student
    template_name='dashboard/student_detail.html'


# class ACreateChat(LoginRequiredMixin, CreateView):
#     form_class = ChatForm
#     model = Chat
#     template_name = 'dashboard/chat_form.html'
#     success_url = reverse_lazy('alchat')


    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


# class AListChat(LoginRequiredMixin, ListView):
#     model = Chat
#     template_name = 'dashboard/chat_list.html'

#     def get_queryset(self):
#         return Chat.objects.filter(posted_at__lt=timezone.now()).order_by('posted_at')


@login_required
def aabook_form(request):
    majors = models.Major.objects.all()
    teachers = models.Teacher.objects.all()
    students = models.Student.objects.all()
    return render(request, 'dashboard/add_book.html', {'majors': majors, 'teachers': teachers, 'students': students})


@login_required
def aabook(request):
    if request.method == 'POST':
        title = request.POST['title']
        year = request.POST['year']
        desc = request.POST['desc']
        cover = request.FILES['cover']
        pdf = request.FILES['pdf']
        current_user = request.user
        user_id = current_user.id
        username = current_user.username
        author_id = request.POST['author']
        major_id = request.POST['major']
        teacher_id = request.POST['teacher']

        # Retrieve the Major instance based on the dep_id
        major = get_object_or_404(models.Major, id=major_id)
        advisor = get_object_or_404(models.Teacher, id=teacher_id)
        author = get_object_or_404(models.Student, id=author_id)

        a = Book(title=title, author=author, year=year, advisor=advisor,
            desc=desc, cover=cover, pdf=pdf, major=major
        )
        a.save()
        messages.success(request, 'Book was uploaded successfully')
        return redirect('albook')
    else:
        messages.error(request, 'Book was not uploaded successfully')
        return redirect('aabook_form')


class ABookListView(LoginRequiredMixin,ListView):
    model = Book
    template_name = 'dashboard/book_list.html'
    context_object_name = 'books'
    paginate_by = 10

    def get_queryset(self):
        return Book.objects.order_by('-id')


class AManageBook(LoginRequiredMixin,ListView):
    model = Book
    template_name = 'dashboard/manage_books.html'
    context_object_name = 'books'
    paginate_by = 10

    # def get_queryset(self):
    #     return Book.objects.order_by('-id')

    def get_queryset(self):
        queryset = Book.objects.order_by('-id')

        # Retrieve the selected major and year from the request
        major = self.request.GET.get('major')
        year = self.request.GET.get('year')

        # Apply filtering based on selected major and year
        if major or year:
            queryset = queryset.filter(Q(major=major) | Q(year=year))

        return queryset


class ADeleteBook(LoginRequiredMixin,DeleteView):
    model = Book
    template_name = 'dashboard/confirm_delete2.html'
    success_url = reverse_lazy('ambook')
    success_message = 'Data was dele successfully'


class ADeleteBookk(LoginRequiredMixin,DeleteView):
    model = Book
    template_name = 'dashboard/confirm_delete.html'
    success_url = reverse_lazy('dashboard')
    success_message = 'Data was dele successfully'


class AViewBook(LoginRequiredMixin,DetailView):
    model = Book
    template_name = 'dashboard/book_detail.html'


class AEditView(LoginRequiredMixin,UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'dashboard/edit_book.html'
    success_url = reverse_lazy('ambook')
    success_message = 'Data was updated successfully'


# class ADeleteRequest(LoginRequiredMixin,ListView):
#     model = DeleteRequest
#     template_name = 'dashboard/delete_request.html'
#     context_object_name = 'feedbacks'
#     paginate_by = 3

#     def get_queryset(self):
#         return DeleteRequest.objects.order_by('-id')


# class AFeedback(LoginRequiredMixin,ListView):
#     model = Feedback
#     template_name = 'dashboard/feedback.html'
#     context_object_name = 'feedbacks'
#     paginate_by = 3

#     def get_queryset(self):
#         return Feedback.objects.order_by('-id')


@login_required
def asearch(request):
    query = request.GET['query']
    print(type(query))

    #data = query.split()
    data = query
    print(len(data))
    if( len(data) == 0):
        return redirect('dashborad')
    else:
        a = data

        # Searching for It
        qs5 =models.Book.objects.filter(id__iexact=a).distinct()
        qs6 =models.Book.objects.filter(id__exact=a).distinct()

        qs7 =models.Book.objects.all().filter(id__contains=a)
        qs8 =models.Book.objects.select_related().filter(id__contains=a).distinct()
        qs9 =models.Book.objects.filter(id__startswith=a).distinct()
        qs10 =models.Book.objects.filter(id__endswith=a).distinct()
        qs11 =models.Book.objects.filter(id__istartswith=a).distinct()
        qs12 =models.Book.objects.all().filter(id__icontains=a)
        qs13 =models.Book.objects.filter(id__iendswith=a).distinct()

        files = itertools.chain(qs5, qs6, qs7, qs8, qs9, qs10, qs11, qs12, qs13)

        res = []
        for i in files:
            if i not in res:
                res.append(i)

        # word variable will be shown in html when user click on search button
        word="Searched Result :"
        print("Result")

        print(res)
        files = res

        page = request.GET.get('page', 1)
        paginator = Paginator(files, 10)
        try:
            files = paginator.page(page)
        except PageNotAnInteger:
            files = paginator.page(1)
        except EmptyPage:
            files = paginator.page(paginator.num_pages)

        if files:
            return render(request,'dashboard/result.html',{'files':files,'word':word})
        return render(request,'dashboard/result.html',{'files':files,'word':word})


def abstract(request, pk):
    books = models.Book.objects.get(id=pk)
    return render(request, 'publisher/abstract.html', {'books': books})
