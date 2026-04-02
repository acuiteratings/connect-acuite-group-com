from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="QuizMatch",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("status", models.CharField(choices=[("invited", "Invited"), ("active", "Active"), ("completed", "Completed"), ("cancelled", "Cancelled")], default="invited", max_length=24)),
                ("difficulty", models.CharField(choices=[("amateur", "Amateur"), ("enthusiast", "Enthusiast"), ("professional", "Professional"), ("expert", "Expert")], max_length=24)),
                ("total_questions", models.PositiveSmallIntegerField(default=10)),
                ("current_question_index", models.PositiveSmallIntegerField(default=0)),
                ("current_question_key", models.CharField(blank=True, max_length=80)),
                ("question_order", models.JSONField(blank=True, default=list)),
                ("question_started_at", models.DateTimeField(blank=True, null=True)),
                ("question_deadline_at", models.DateTimeField(blank=True, null=True)),
                ("started_at", models.DateTimeField(blank=True, null=True)),
                ("completed_at", models.DateTimeField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("host", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="quiz_matches_hosted", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ("-created_at",)},
        ),
        migrations.CreateModel(
            name="QuizParticipant",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("seat", models.PositiveSmallIntegerField()),
                ("status", models.CharField(choices=[("accepted", "Accepted"), ("invited", "Invited"), ("declined", "Declined")], default="invited", max_length=24)),
                ("score", models.PositiveIntegerField(default=0)),
                ("joined_at", models.DateTimeField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("match", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="participants", to="quiz.quizmatch")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="quiz_participations", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ("seat", "created_at")},
        ),
        migrations.CreateModel(
            name="QuizAnswer",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("question_index", models.PositiveSmallIntegerField()),
                ("question_key", models.CharField(max_length=80)),
                ("selected_option", models.CharField(max_length=1)),
                ("is_correct", models.BooleanField(default=False)),
                ("answered_at", models.DateTimeField(auto_now_add=True)),
                ("response_ms", models.PositiveIntegerField(blank=True, null=True)),
                ("match", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="answers", to="quiz.quizmatch")),
                ("participant", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="answers", to="quiz.quizparticipant")),
            ],
            options={"ordering": ("question_index", "answered_at")},
        ),
        migrations.AddConstraint(
            model_name="quizparticipant",
            constraint=models.UniqueConstraint(fields=("match", "user"), name="quiz_unique_participant_per_match"),
        ),
        migrations.AddConstraint(
            model_name="quizparticipant",
            constraint=models.UniqueConstraint(fields=("match", "seat"), name="quiz_unique_seat_per_match"),
        ),
        migrations.AddConstraint(
            model_name="quizanswer",
            constraint=models.UniqueConstraint(fields=("participant", "question_index"), name="quiz_one_answer_per_participant_per_question"),
        ),
    ]
