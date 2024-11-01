# Generated by Django 5.1.1 on 2024-10-29 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0004_customuser_phone"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="internschool",
            name="city",
        ),
        migrations.RemoveField(
            model_name="internschool",
            name="town",
        ),
        migrations.AddField(
            model_name="internschool",
            name="district",
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="internschool",
            name="location",
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="mentor",
            name="email",
            field=models.EmailField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name="internschool",
            name="region",
            field=models.CharField(max_length=100, null=True),
        ),
    ]
