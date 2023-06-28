from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.urls import reverse




#User = get_user_model()


class Department(models.Model):
    depname_la = models.CharField(max_length=100, null=True, blank=True)
    depname_en = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f'{self.depname_en} ({self.depname_la})'


class Major(models.Model):
    majname_la = models.CharField(max_length=100, null=True, blank=True)
    majname_en = models.CharField(max_length=100, null=True, blank=True)
    dep = models.ForeignKey(Department, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.majname_en} ({self.majname_la})'


class Teacher(models.Model):
    full_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=(('Male', 'Male'), ('Female', 'Female')), default='Male')
    telephone = models.CharField(max_length=12)
    email = models.EmailField(max_length=255)
    dep = models.ForeignKey(Department, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.full_name}'


class Student(models.Model):
    full_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=(('Male', 'Male'), ('Female', 'Female')), default='Male')
    dob = models.DateField()
    village = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    telephone = models.CharField(max_length=12)
    email = models.EmailField(max_length=255)
    major = models.ForeignKey(Major, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.full_name}'


class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_publisher = models.BooleanField(default=False)
    is_librarian = models.BooleanField(default=False)
    teacher = models.ForeignKey(Teacher, null=True, blank=True, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        swappable = 'AUTH_USER_MODEL'


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    advisor = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True, blank=True)
    year = models.CharField(max_length=100)
    desc = models.CharField(max_length=1000)
    pdf = models.FileField(upload_to='bookapp/pdfs/')
    cover = models.ImageField(upload_to='bookapp/covers/', null=True, blank=True)
    major = models.ForeignKey(Major, null=True, blank=True, on_delete=models.CASCADE)
    thesis_date = models.DateField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        self.pdf.delete()
        self.cover.delete()
        super().delete(*args, **kwargs)        


class Download(models.Model):
    download_date = models.DateTimeField(auto_now_add=True)
    price = models.FloatField(default=0)
    thesis_amount = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    thesis = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.thesis}'


class Payment(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.FloatField(default=0)
    bin_img = models.ImageField(upload_to='bookapp/downloads/')
    download = models.ForeignKey(Download, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.download}'

