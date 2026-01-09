from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("remover", "0001_initial"),
    ]

    operations = [
        migrations.DeleteModel(
            name="MarkerConfig",
        ),
        migrations.CreateModel(
            name="RemoveWord",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("word", models.CharField(max_length=100, unique=True)),
                ("active", models.BooleanField(default=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
