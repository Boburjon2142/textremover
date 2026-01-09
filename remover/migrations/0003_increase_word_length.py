from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("remover", "0002_remove_markers_add_words"),
    ]

    operations = [
        migrations.AlterField(
            model_name="removeword",
            name="word",
            field=models.CharField(max_length=10000, unique=True),
        ),
    ]
