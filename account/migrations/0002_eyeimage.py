# Generated by Django 5.0.7 on 2024-10-09 05:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EyeImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('left_eye_image', models.ImageField(upload_to='eye_images/')),
                ('right_eye_image', models.ImageField(upload_to='eye_images/')),
            ],
        ),
    ]
