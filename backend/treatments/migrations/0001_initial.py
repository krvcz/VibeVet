# Generated by Django 4.2.20 on 2025-05-07 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="TreatmentGuide",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("query", models.TextField()),
                ("result", models.TextField()),
                ("factors", models.JSONField()),
            ],
            options={
                "verbose_name": "Treatment Guide",
                "verbose_name_plural": "Treatment Guides",
                "db_table": "treatment_guide",
            },
        ),
    ]
