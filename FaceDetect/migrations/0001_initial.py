# Generated by Django 5.1 on 2024-09-30 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EyeModel',
            fields=[
                ('eye_id', models.AutoField(primary_key=True, serialize=False)),
                ('eye_name', models.CharField(max_length=255)),
                ('eye_image', models.ImageField(upload_to='eye_image/')),
            ],
        ),
    ]
