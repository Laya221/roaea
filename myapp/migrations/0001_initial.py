# Generated by Django 4.0 on 2021-12-20 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FilesModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, null=True)),
                ('path', models.CharField(max_length=100, null=True)),
                ('key_word', models.CharField(max_length=100, null=True)),
                ('file_type', models.CharField(choices=[('text', 'text'), ('video', 'video')], default=('text', 'text'), max_length=50)),
            ],
        ),
    ]