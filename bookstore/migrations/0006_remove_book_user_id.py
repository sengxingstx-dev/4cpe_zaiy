# Generated by Django 3.2.15 on 2023-06-26 12:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookstore', '0005_remove_book_uploaded_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='user_id',
        ),
    ]
