# Generated by Django 5.0.1 on 2024-02-04 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Book",
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
                ("title", models.CharField(max_length=244)),
                ("author", models.CharField(max_length=244)),
                (
                    "cover",
                    models.CharField(
                        choices=[("Hard", "Hard"), ("Soft", "Soft")], max_length=4
                    ),
                ),
                ("inventory", models.PositiveIntegerField()),
                ("daily_fee", models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
    ]
