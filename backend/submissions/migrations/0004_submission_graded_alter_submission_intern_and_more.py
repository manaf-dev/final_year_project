# Generated by Django 5.1.1 on 2024-11-07 11:26

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("submissions", "0003_alter_portfoliofile_file_type"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="submission",
            name="graded",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="submission",
            name="intern",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="submissions",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="submission",
            name="month",
            field=models.CharField(
                choices=[
                    ("1", "First Month"),
                    ("2", "Second Month"),
                    ("3", "Third Month"),
                    ("4", "Fourth Month"),
                ],
                max_length=10,
            ),
        ),
        migrations.CreateModel(
            name="Grade",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("mark", models.PositiveIntegerField(default=0)),
                ("graded_at", models.DateTimeField(auto_now=True)),
                (
                    "submission",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="grades",
                        to="submissions.submission",
                    ),
                ),
            ],
        ),
    ]
