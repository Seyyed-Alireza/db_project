from django.db import models
from Exams.models import Exam
from main.constant import EventType
from Exams.models import Exam
from django.db import models, connection, transaction

class Question(models.Model):
    class QuestionTypeChoices(models.IntegerChoices):
        MULTIPLE_CHOICE = EventType.QUESTION_MULTIPLE_CHOICE, 'چند گزینه‌ای'
        DESCRIPTIVE = EventType.QUESTION_DESCRIPTIVE, 'تشریحی'
    
    QuestionID = models.AutoField(primary_key=True, verbose_name="شناسه سوال")
    
    ExamKey = models.ForeignKey(
        Exam, 
        on_delete=models.CASCADE,
        db_column="ExamKey",
        verbose_name="شناسه امتحان",
    )
    QuestionType = models.PositiveSmallIntegerField(verbose_name="نوع سوال", choices=QuestionTypeChoices)

    QuestionText = models.TextField(verbose_name="متن سوال")

    QuestionImage = models.ImageField(max_length=200, upload_to='question_images/', blank=True, null=True, verbose_name="تصویر سوال")
    
    Score = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="نمره")

    Order = models.IntegerField(default=1, verbose_name='جایگاه سوال')

    def save(self, *args, **kwargs):
        is_new = self.pk is None

        if is_new and self.Order == 1:
            last_question = Question.objects.filter(
                ExamKey=self.ExamKey
            ).order_by('-Order').first()

            if last_question:
                self.Order = last_question.Order + 1
            else:
                self.Order = 1

        super().save(*args, **kwargs)

    # CorrectAnswer = models.PositiveSmallIntegerField(blank=True, verbose_name="پاسخ صحیح")

    class Meta:
        managed = False
        db_table = 'Questions'
        ordering = ['Order']

    @classmethod
    def rebalance_orders(cls, exam):
        """
        بازنشانی Order ها به ۱, ۲, ۳, ...
        بهینه‌ترین روش برای MySQL 8.0+
        """
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE Questions AS q
                INNER JOIN (
                    SELECT 
                        QuestionID, 
                        ROW_NUMBER() OVER (PARTITION BY ExamKey ORDER BY `Order`) AS new_order
                    FROM Questions
                    WHERE ExamKey = %s
                ) AS ranked ON q.QuestionID = ranked.QuestionID
                SET q.`Order` = ranked.new_order
                WHERE q.ExamKey = %s
            """, [exam.pk, exam.pk])
            
            return cursor.rowcount