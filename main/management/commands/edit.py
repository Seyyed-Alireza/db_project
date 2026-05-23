from django.core.management.base import BaseCommand
import random
from FraudFlags.models import FraudFlag
from LoginSessions.models import LoginSession
from Questions.models import Question
from BehavioralMetrics.models import BehavioralMetric
from main.views import get_time_now
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = "Fill database with sample data"
    

    def handle(self, *args, **options):
        # FraudFlag.objects.all().delete()
        # login_sessions = LoginSession.objects.all()
        # questions = Question.objects.all()
        # FraudFlag.objects.create(
        #     SessionKey=login_sessions[0],
        #     QuestionKey=random.choice(questions),
        #     Reason='reason1',
        #     RiskScore=20,
        #     Severity='severity1',
        #     FlagType='flag1',
        #     Status='normal',
        #     GeneratedAt=get_time_now()-timedelta(hours=2, minutes=23),
        # )
        # FraudFlag.objects.create(
        #     SessionKey=login_sessions[1],
        #     QuestionKey=random.choice(questions),
        #     Reason='reason1',
        #     RiskScore=50,
        #     Severity='severity1',
        #     FlagType='flag1',
        #     Status='suspicious',
        #     GeneratedAt=get_time_now()-timedelta(hours=2, minutes=47),
        # )
        # FraudFlag.objects.create(
        #     SessionKey=login_sessions[10],
        #     QuestionKey=random.choice(questions),
        #     Reason='reason1',
        #     RiskScore=80,
        #     Severity='severity1',
        #     FlagType='flag1',
        #     Status='definite',
        #     GeneratedAt=get_time_now(),
        # )
        BehavioralMetric.objects.all().delete()
        login_sessions = LoginSession.objects.all()
        questions = Question.objects.all()
        behaviorals = []
        for question in questions:
            time_spent=random.randint(200, 1000)
            behaviorals.append(
                BehavioralMetric.objects.create(
                    SessionKey=random.choice(login_sessions),
                    QuestionKey=question,
                    TotalTimeSpent=time_spent,
                    TabSwitchCount=random.choice([0, 0, 1, 2, 3, 4, 6, 6, 6, 7, 7, 8, 8]),
                    CopyPasteCount=random.choice([0, 0, 0, 0, 0, 0, 1, 2, 3, 4]),
                    IdleTime=time_spent-20,
                )
            )

        self.stdout.write(self.style.SUCCESS(f"Edited successfully"))
            