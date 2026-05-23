import pandas as pd
from sklearn.ensemble import IsolationForest
from LoginSessions.models import LoginSession
from TabSwitchLogs.models import TabSwitchLog
from IPAddressLogs.models import IPAddressLog
from BehavioralMetrics.models import BehavioralMetric 
from FraudFlags.models import FraudFlag
from ResolutionLogs.models import ResolutionLog
def run_fraud_detection_ml(exam_id):

    sessions = LoginSession.objects.filter(ExamKey_id=exam_id)
    data = []

    for session in sessions:
        
        tab_switches = TabSwitchLog.objects.filter(SessionKey=session).count()
        ip_count = IPAddressLog.objects.filter(SessionKey=session).values('IPAddress').distinct().count()
        resolution = ResolutionLog.objects.filter(SessionKey=session).last()
        is_fullscreen = 1 if resolution and resolution.ScreenWidth == resolution.WindowWidth and resolution.ScreenHeight == resolution.WindowHeight else 0
        res_changed = 1 if resolution and resolution.ChangeTime else 0
        data.append({
            'SessionKey_id': session.pk,
            'tab_switches': tab_switches,
            'ip_count': ip_count,
            'is_fullscreen': is_fullscreen,
            'res_changed': res_changed
        })

    if not data:
        return

    df = pd.DataFrame(data)

    features = ['tab_switches', 'ip_count', 'is_fullscreen', 'res_changed']
    model = IsolationForest(n_estimators=100, contamination=0.1, random_state=42)
    
    
    df['anomaly_score'] = model.fit_predict(df[features])
    
 
    for _, row in df[df['anomaly_score'] == -1].iterrows():
        session = LoginSession.objects.get(pk=row['SessionKey_id'])
        FraudFlag.objects.update_or_create(
            SessionKey=session,
            defaults={
                'Reason': f"رفتار غیرعادی: تب={row['tab_switches']}, آی‌پی={row['ip_count']}, فول‌اسکرین={row['is_fullscreen']}, رزولوشن={row['res_changed']}",
                'RiskScore': 85,
                'Severity': 'High',
                'Status': 'Cheating'
            }
        )
