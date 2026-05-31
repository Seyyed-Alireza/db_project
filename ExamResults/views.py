from django.shortcuts import render, redirect
from django.db import connection

def exam_result(request, exam_id):
    user_pk = request.session.get('user_id')
    if not user_pk:
        return redirect("Users:login")
    
    context = {}
    
    # کوئری SQL برای ExamResult
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT `TotalScore`, `Status`, `Grade`, `CalculatedAt`
            FROM `examresults`
            WHERE `ExamKey` = %s AND `StudentKey` = %s
            LIMIT 1
        """, [exam_id, user_pk])
        
        result_row = cursor.fetchone()
        
        if result_row:
            context['total_score'] = result_row[0]
            context['status'] = result_row[1]
            context['grade'] = result_row[2]
            context['calculated_at'] = result_row[3]
            
            # کوئری SQL برای Exam
            cursor.execute("""
                SELECT `Title`
                FROM `exams`
                WHERE `ExamID` = %s
                LIMIT 1
            """, [exam_id])
            
            exam_row = cursor.fetchone()
            if exam_row:
                context['exam_title'] = exam_row[0]
    
    return render(request, 'ExamResults/ExamResult.html', context)