# Generated by Django 4.0.6 on 2024-04-05 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="URLS",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("original_url", models.URLField()),
                ("shortcode", models.CharField(max_length=15, unique=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "db_table": '"shortner"."urls"',
            },
        ),
        migrations.AddIndex(
            model_name="urls",
            index=models.Index(
                fields=["shortcode"], name="shortner_urls_shortcode_idx"
            ),
        ),
    ]
