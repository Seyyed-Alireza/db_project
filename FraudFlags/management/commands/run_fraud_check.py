from django.core.management.base import BaseCommand
from FraudDetection.ml_services import run_fraud_detection_ml

class Command(BaseCommand):
    help = 'اجرای تحلیل هوش مصنوعی برای تشخیص تقلب در یک آزمون خاص'

    def add_arguments(self, parser):
        
        parser.add_argument('exam_id', type=int, help='آیدی آزمون مورد نظر')

    def handle(self, *args, **kwargs):
        exam_id = kwargs['exam_id']
        self.stdout.write(f"در حال تحلیل آزمون شماره {exam_id}...")
        
        try:
            run_fraud_detection_ml(exam_id)
            self.stdout.write(self.style.SUCCESS(f"تحلیل با موفقیت انجام شد! نتایج در FraudFlag ذخیره شدند."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"خطایی رخ داد: {str(e)}"))
