# Generated by Django 3.2.15 on 2023-06-28 10:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookstore', '0008_book_advisor'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='publisher',
        ),
    ]
