# Generated by Django 4.2 on 2024-02-02 21:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='uploads/', verbose_name='file')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True, verbose_name='upload time')),
                ('processed', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'File',
                'verbose_name_plural': 'Files',
                'ordering': ('uploaded_at',),
            },
        ),
    ]
