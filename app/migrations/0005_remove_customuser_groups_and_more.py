# Generated by Django 4.1.6 on 2024-05-16 09:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0004_exerciserecord_delete_option"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="customuser",
            name="groups",
        ),
        migrations.RemoveField(
            model_name="customuser",
            name="user_permissions",
        ),
        migrations.DeleteModel(
            name="MyModel",
        ),
        migrations.AlterField(
            model_name="exerciserecord",
            name="description",
            field=models.TextField(blank=True),
        ),
        migrations.DeleteModel(
            name="CustomUser",
        ),
    ]
