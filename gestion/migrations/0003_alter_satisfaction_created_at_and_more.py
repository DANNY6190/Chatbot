# Generated by Django 4.2.4 on 2023-09-27 09:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("gestion", "0002_satisfaction"),
    ]

    operations = [
        migrations.AlterField(
            model_name="satisfaction",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name="satisfaction",
            name="recommandation",
            field=models.BooleanField(default=True),
        ),
    ]
