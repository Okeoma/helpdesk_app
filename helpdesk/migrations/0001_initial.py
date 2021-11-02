# Generated by Django 3.0.8 on 2021-10-08 22:24

import datetime
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('access', models.CharField(choices=[('Regular', 'Regular'), ('Standard', 'Standard'), ('Admin', 'Admin')], default='Admin', max_length=15, verbose_name='access')),
                ('role', models.CharField(max_length=60)),
                ('location', models.CharField(blank=True, max_length=120)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer', models.CharField(max_length=30, unique=True)),
                ('firstname', models.CharField(max_length=30)),
                ('lastname', models.CharField(max_length=30)),
                ('email', models.CharField(max_length=30)),
                ('phone_no', models.CharField(max_length=20)),
                ('company', models.CharField(max_length=30)),
                ('location', models.CharField(blank=True, max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='Dynamics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images')),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('text', models.CharField(default=None, max_length=500)),
                ('date', models.DateTimeField(default=datetime.datetime.now)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images')),
                ('closed', models.BooleanField(default=False)),
                ('comments', models.ManyToManyField(blank=True, related_name='comments_ticket', to='helpdesk.Comment')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='client', to='helpdesk.Customer')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trouble_ticket', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='images')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='image_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Ticketrank',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticket', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='helpdesk.Ticket')),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('ticket', 'user')},
            },
        ),
        migrations.CreateModel(
            name='Senior',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('junior', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='junior', to=settings.AUTH_USER_MODEL)),
                ('senior', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='senior', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('senior', 'junior')},
            },
        ),
    ]