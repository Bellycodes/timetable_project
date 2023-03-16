# Generated by Django 4.1.6 on 2023-03-16 08:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Course",
            fields=[
                (
                    "code",
                    models.CharField(max_length=7, primary_key=True, serialize=False),
                ),
                ("title", models.CharField(max_length=40)),
                ("max_numb_students", models.CharField(max_length=65)),
            ],
        ),
        migrations.CreateModel(
            name="Department",
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
                ("dept_name", models.CharField(max_length=50)),
                ("courses", models.ManyToManyField(to="ttgen.course")),
            ],
        ),
        migrations.CreateModel(
            name="Lecturer",
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
                ("uid", models.CharField(max_length=6)),
                ("name", models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name="LectureRoom",
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
                ("r_number", models.CharField(max_length=6)),
                ("seating_capacity", models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name="Level",
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
                ("level", models.CharField(blank=True, max_length=6)),
            ],
        ),
        migrations.CreateModel(
            name="TimeSlot",
            fields=[
                (
                    "pid",
                    models.CharField(max_length=4, primary_key=True, serialize=False),
                ),
                (
                    "time",
                    models.CharField(
                        choices=[
                            ("9:30 - 10:30", "9:30 - 10:30"),
                            ("10:30 - 11:30", "10:30 - 11:30"),
                            ("11:30 - 12:30", "11:30 - 12:30"),
                            ("12:30 - 1:30", "12:30 - 1:30"),
                            ("2:30 - 3:30", "2:30 - 3:30"),
                            ("3:30 - 4:30", "3:30 - 4:30"),
                            ("4:30 - 5:30", "4:30 - 5:30"),
                        ],
                        default="11:30 - 12:30",
                        max_length=50,
                    ),
                ),
                (
                    "day",
                    models.CharField(
                        choices=[
                            ("Monday", "Monday"),
                            ("Tuesday", "Tuesday"),
                            ("Wednesday", "Wednesday"),
                            ("Thursday", "Thursday"),
                            ("Friday", "Friday"),
                            ("Saturday", "Saturday"),
                        ],
                        max_length=15,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Section",
            fields=[
                (
                    "section_id",
                    models.CharField(max_length=25, primary_key=True, serialize=False),
                ),
                ("num_class_in_week", models.IntegerField(default=0)),
                (
                    "course",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="ttgen.course",
                    ),
                ),
                (
                    "department",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="ttgen.department",
                    ),
                ),
                (
                    "lecturer",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="ttgen.lecturer",
                    ),
                ),
                (
                    "level",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="ttgen.level",
                    ),
                ),
                (
                    "room",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="ttgen.lectureroom",
                    ),
                ),
                (
                    "time",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="ttgen.timeslot",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="department",
            name="level",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="ttgen.level"
            ),
        ),
        migrations.AddField(
            model_name="course",
            name="lecturer",
            field=models.ManyToManyField(to="ttgen.lecturer"),
        ),
    ]
