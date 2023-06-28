from django.contrib import admin
from .models import (
    User, Book,
    Teacher, Student,
    Department, Major,
    Download, Payment
)



admin.site.register(User)
admin.site.register(Book)
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Department)
admin.site.register(Major)
admin.site.register(Download)
admin.site.register(Payment)

