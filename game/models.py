# accounts/models.py
import django
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db import migrations

from django.db import models

class Question(models.Model):
    text = models.CharField(max_length=255)

    def _str_(self):
        return self.text

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def _str_(self):
        return self.text










class Migration(migrations.Migration):


    dependencies = [
        ('auth', 'xxxx_previous_dependency'),
        ('accounts', 'previous_migration'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='group',
            managers=[
                ('objects', django.contrib.auth.models.GroupManager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='permission',
            managers=[
                ('objects', django.contrib.auth.models.PermissionManager()),
            ],
        ),
        migrations.AlterModelOptions(
            name='group',
            options={'verbose_name': 'group', 'verbose_name_plural': 'groups', 'ordering': ('name',)},
        ),
        migrations.AlterModelOptions(
            name='permission',
            options={'verbose_name': 'permission', 'verbose_name_plural': 'permissions', 'ordering': ('content_type__app_label', 'content_type__model', 'codename')},
        ),
        migrations.AlterField(
            model_name='group',
            name='name',
            field=models.CharField(unique=True, max_length=80, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='permission',
            name='name',
            field=models.CharField(max_length=255, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='permission',
            name='content_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType', verbose_name='content type'),
        ),
        migrations.AlterUniqueTogether(
            name='permission',
            unique_together={('content_type', 'codename')},
        ),
    ]