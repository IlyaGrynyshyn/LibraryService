# Generated by Django 5.0.1 on 2024-02-06 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("borrowings", "0003_alter_borrowing_actual_return_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="borrowing",
            name="borrow_date",
            field=models.DateField(auto_now_add=True),
        ),
    ]
