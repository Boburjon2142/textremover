from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("remover", "0003_increase_word_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="AccessLog",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("ip_address", models.CharField(blank=True, max_length=45)),
                ("user_agent", models.CharField(blank=True, max_length=300)),
                ("input_length", models.PositiveIntegerField(default=0)),
                ("output_length", models.PositiveIntegerField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
