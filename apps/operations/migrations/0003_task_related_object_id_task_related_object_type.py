# Generated by Django 5.2.1 on 2025-05-24 10:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("operations", "0002_taskreport_alter_fertilization_options_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="task",
            name="related_object_id",
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="task",
            name="related_object_type",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="contenttypes.contenttype",
            ),
        ),
    ]
