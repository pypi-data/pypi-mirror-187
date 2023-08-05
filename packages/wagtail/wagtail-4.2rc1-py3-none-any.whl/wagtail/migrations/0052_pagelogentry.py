# Generated by Django 3.0.5 on 2020-07-09 21:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("wagtailcore", "0051_taskstate_comment"),
    ]

    operations = [
        migrations.CreateModel(
            name="PageLogEntry",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("label", models.TextField()),
                ("action", models.CharField(blank=True, db_index=True, max_length=255)),
                ("data_json", models.TextField(blank=True)),
                ("timestamp", models.DateTimeField(verbose_name="timestamp (UTC)")),
                ("content_changed", models.BooleanField(db_index=True, default=False)),
                ("deleted", models.BooleanField(default=False)),
                (
                    "content_type",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="contenttypes.ContentType",
                        verbose_name="content type",
                    ),
                ),
                (
                    "page",
                    models.ForeignKey(
                        db_constraint=False,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to="wagtailcore.Page",
                    ),
                ),
                (
                    "revision",
                    models.ForeignKey(
                        blank=True,
                        db_constraint=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to="wagtailcore.PageRevision",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        db_constraint=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "page log entry",
                "verbose_name_plural": "page log entries",
                "ordering": ["-timestamp", "-id"],
            },
        ),
    ]
