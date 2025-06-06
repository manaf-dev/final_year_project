# Generated by Django 5.1.1 on 2024-11-07 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0007_customuser_title"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="title",
            field=models.CharField(
                choices=[
                    ("mr", "Mr."),
                    ("mrs", "Mrs."),
                    ("miss", "Miss"),
                    ("dr", "Dr."),
                    ("prof", "Prof."),
                ],
                max_length=20,
                null=True,
            ),
        ),
    ]
