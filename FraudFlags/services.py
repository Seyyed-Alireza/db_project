from TabSwitchLogs.models import TabSwitchLog
from ResolutionLogs.models import ResolutionLog
from IPAddressLogs.models import IPAddressLog
from FraudFlags.models import FraudFlag
from LoginSessions.models import LoginSession
from .fraud_weights import FRAUD_WEIGHTS, THRESHOLD


def manual_fraud_check(exam_id, student_id=None):
    sessions = LoginSession.objects.filter(ExamKey=exam_id)
    if student_id:
        sessions = sessions.filter(StudentKey=student_id)
    # print("sessions count =", sessions.count())
    for session in sessions:
        # print("processing session:", session.pk)
        risk_score = 0
        reasons = []

        tab_switches = TabSwitchLog.objects.filter(SessionKey=session).count()
        if tab_switches > 0:    
            score = tab_switches * FRAUD_WEIGHTS['tab_switch']
            risk_score += score
            reasons.append(f"{tab_switches} tab switches detected (+{score})")
        
        res_changes = ResolutionLog.objects.filter(SessionKey=session).count()
        if res_changes > 1: 
            score = (res_changes - 1) * FRAUD_WEIGHTS['resolution_change']
            risk_score += score
            reasons.append(f"{res_changes-1} window resizes detected (+{score})")
        
        ip_count = IPAddressLog.objects.filter(SessionKey=session).count()
        if ip_count > 1:
            risk_score += FRAUD_WEIGHTS['ip_change']
            reasons.append(f"Accessed from {ip_count} different IPs (+{FRAUD_WEIGHTS['ip_change']})")

        status = 'Normal'
        if risk_score >= THRESHOLD:
            status = 'High Risk'
        elif risk_score > 0:
            status = 'Suspicious'

        FraudFlag.objects.update_or_create(
            SessionKey=session,
            defaults={
                'RiskScore': min(risk_score, 100), 
                'Reason': " | ".join(reasons) if reasons else "No suspicious activity",
                'Severity': status,
                'Status': 'Fraud' if status=='High Risk' else 'Normal',

            }
        )

    return f"Processed {sessions.count()} sessions."

# def manual_fraud_check(exam_id, student_id=None):
#     sessions = LoginSession.objects.filter(ExamKey=exam_id)
#     if student_id:
#         sessions = sessions.filter(StudentKey=student_id)

#     print("sessions count =", sessions.count())

#     for session in sessions:
#         print("processing session:", session.pk)
#         risk_score = 0
#         reasons = []

#         tab_switches = TabSwitchLog.objects.filter(SessionKey=session).count()
#         print("tab_switches =", tab_switches)

#         res_changes = ResolutionLog.objects.filter(SessionKey=session).count()
#         print("res_changes =", res_changes)

#         ip_count = IPAddressLog.objects.filter(Session=session).count()
#         print("ip_count =", ip_count)

#         status = 'Normal'
#         if risk_score >= THRESHOLD:
#             status = 'High Risk'
#         elif risk_score > 0:
#             status = 'Suspicious'

#         obj, created = FraudFlag.objects.update_or_create(
#             SessionKey=session,
#             defaults={
#                 'RiskScore': min(risk_score, 100),
#                 'Reason': " | ".join(reasons) if reasons else "No suspicious activity",
#                 'Severity': status,
#                 'Status': 'Fraud' if status == 'High Risk' else 'Normal',
#             }
#         )
#         print("FraudFlag saved:", obj.pk, "created=", created)

#     return f"Processed {sessions.count()} sessions."
