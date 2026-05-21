from FraudFlags.models import FraudFlag
from .fraud_weights import FRAUD_WEIGHTS, THRESHOLD


def register_event(student, exam, event_type):

    weight = FRAUD_WEIGHTS.get(event_type, 0)

    flag, created = FraudFlag.objects.get_or_create(
        StudentKey=student,
        ExamKey=exam,
        defaults={"Score": 0, "IsFraud": False}
    )

    flag.Score += weight

    if flag.Score >= THRESHOLD:
        flag.IsFraud = True

    flag.save()

    return flag
