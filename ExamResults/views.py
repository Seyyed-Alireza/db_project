from django.shortcuts import render, redirect, get_object_or_404
from django.db import connection, transaction
from django.contrib import messages
from Exams.models import Exam
from ExamResults.models import ExamResult
from Students.models import Student
from LoginSessions.models import LoginSession
from decimal import Decimal

def get_exam_result_raw(exam_id, student_id):
    
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT TotalScore, Status, Grade
            FROM ExamResults
            WHERE ExamKey = %s AND StudentKey = %s
            LIMIT 1
        """, [exam_id, student_id])

        row = cursor.fetchone()

    if row:
        return {
            "TotalScore": row[0],
            "Status": row[1],
            "Grade": row[2],
        }
    return None

@transaction.atomic
def save_exam_result_raw(exam_id, student_id, score, status, grade):
    with connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO ExamResults (ExamKey, StudentKey, TotalScore, Status, Grade)
            VALUES (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                TotalScore = VALUES(TotalScore),
                Status = VALUES(Status),
                Grade = VALUES(Grade)
        """, [exam_id, student_id, score, status, grade])

def grade_exam_students(request, exam_id):
    user_pk = request.session.get('user_id')
    if not user_pk:
        return redirect("Users:login")
    
    exam = get_object_or_404(Exam, pk=exam_id)

    sessions = LoginSession.objects.filter(
        ExamKey=exam
    ).select_related('StudentKey').distinct()

    students = []
    seen = set()
    for session in sessions:
        student = session.StudentKey
        if student and student.pk not in seen:
            seen.add(student.pk)
            # result = ExamResult.objects.filter(
            #     ExamKey=exam,
            #     StudentKey=student
            # ).first()
            result = get_exam_result_raw(exam.pk, student.pk)
            students.append({
                'student' : student, 
                'result': result
            })

    if request.method == "POST":
        student_id = request.POST.get("student_id")
        score = request.POST.get("score")

        try:
            student = Student.objects.get(pk=student_id)
            score = Decimal(score)

            if score < 0:
                messages.error(request, "نمره نمی‌تواند منفی باشد.")
                return redirect("ExamResults:grade_exam_students", exam_id=exam.pk)

            max_score = float(exam.TotalScore or 0)
            if max_score and score > max_score:
                messages.error(request, f"نمره نمی‌تواند بیشتر از نمره کل آزمون ({max_score}) باشد.")
                return redirect("ExamResults:grade_exam_students", exam_id=exam.pk)
            
            status = score >= (max_score / 2 if max_score else 0)

            if score >= 0.8 * max_score:
                grade = "A"
            elif score >= 0.6 * max_score:
                grade = "B"
            elif score >= 0.4 * max_score:
                grade = "C"
            elif score >= 0.2 * max_score:
                grade = "D"
            else:
                grade = "F"

            # ExamResult.objects.update_or_create(
            #     ExamKey=exam,
            #     StudentKey=student,
            #     defaults={
            #         "TotalScore": score,
            #         "Status": status,
            #         "Grade": grade,
            #     }
            # )
            save_exam_result_raw(
                exam_id=exam.pk,
                student_id=student.pk,
                score=score,
                status=status,
                grade=grade
            )

            messages.success(request, "نمره با موفقیت ثبت شد.")
            return redirect("ExamResults:grade_exam_students", exam_id=exam.pk)
        
        except Student.DoesNotExist:
            messages.error(request, "دانشجو پیدا نشد.")
        except ValueError:
            messages.error(request, "نمره نامعتبر است.")
        except Exception as e:
            messages.error(request, f"خطا در ثبت نمره: {e}")

    scored_students = [item for item in students if item["result"] and item["result"]["TotalScore"] is not None]
    score_values = [float(item["result"]["TotalScore"]) for item in scored_students]

    total_students = len(students)
    graded_count = len(scored_students)
    ungraded_count = total_students - graded_count

    average_score = round(sum(score_values) / graded_count, 2) if graded_count else 0

    if graded_count:
        sorted_scores = sorted(score_values)
        mid = graded_count // 2
        if graded_count % 2 == 0:
            median_score = round((sorted_scores[mid - 1] + sorted_scores[mid]) / 2, 2)
        else:
            median_score = round(sorted_scores[mid], 2)
        highest_score = max(score_values)
        lowest_score = min(score_values)
    else:
        median_score = 0
        highest_score = 0
        lowest_score = 0

    passed_count = sum(1 for item in scored_students if item["result"]["Status"] is True)
    failed_count = sum(1 for item in scored_students if item["result"]["Status"] is False)

    pass_rate = round((passed_count / graded_count) * 100, 2) if graded_count else 0

    student_score_labels = []
    student_score_data = []

    for item in students:
        student = item["student"]
        result = item["result"]
        full_name = f"{student.UserKey.FirstName} {student.UserKey.LastName}"
        student_score_labels.append(full_name)

        if result and result["TotalScore"] is not None:
            student_score_data.append(float(result["TotalScore"]))
        else:
            student_score_data.append(0)

    distribution_labels = ["0-20%", "21-40%", "41-60%", "61-80%", "81-100%"]
    distribution_values = [0, 0, 0, 0, 0]

    max_score = float(exam.TotalScore or 0)

    if max_score > 0:
        for score in score_values:
            percent = (score / max_score) * 100
            if percent <= 20:
                distribution_values[0] += 1
            elif percent <= 40:
                distribution_values[1] += 1
            elif percent <= 60:
                distribution_values[2] += 1
            elif percent <= 80:
                distribution_values[3] += 1
            else:
                distribution_values[4] += 1

    grade_distribution = {
        "A": 0,
        "B": 0,
        "C": 0,
        "D": 0,
        "F": 0,
    }

    for item in scored_students:
        grade = item["result"]["Grade"]
        if grade in grade_distribution:
            grade_distribution[grade] += 1            
    context = {
        'exam': exam,
        "students": students,
        "total_students": total_students,
        "graded_count": graded_count,
        "ungraded_count": ungraded_count,
        "average_score": average_score,
        "median_score": median_score,
        "highest_score": highest_score,
        "lowest_score": lowest_score,
        "passed_count": passed_count,
        "failed_count": failed_count,
        "pass_rate": pass_rate,

        "student_score_labels": student_score_labels,
        "student_score_data": student_score_data,
        "distribution_labels": distribution_labels,
        "distribution_values": distribution_values,
        "grade_labels": list(grade_distribution.keys()),
        "grade_values": list(grade_distribution.values())
    }
    return render(request, "ExamResults/GradeExamStudents.html", context)


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

def student_results(request):
    user_pk = request.session.get('user_id')
    if not user_pk:
        return redirect("Users:login")

    # results = ExamResult.objects.filter(
    #     StudentKey_id=user_pk
    # ).select_related("ExamKey")
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                er.StudentKey,
                er.ExamKey,
                er.TotalScore AS ResultScore,
                er.Status,
                er.Grade,
                er.CalculatedAt,
                e.ExamID,
                e.Title,
                e.StartTime,
                e.EndTime,
                e.Duration,
                e.TotalScore AS ExamTotalScore,
                c.CourseName
            FROM ExamResults er
            INNER JOIN Exams e ON er.ExamKey = e.ExamID
            INNER JOIN Courses c ON c.CourseID = e.CourseKey
            WHERE er.StudentKey = %s
        """, [user_pk])

        columns = [col[0] for col in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    total_exams = len(results)
    passed_exams = sum(1 for r in results if r['Status'])
    failed_exams = total_exams - passed_exams

    total_obtained = 0
    total_possible = 0
    percent_sum = 0
    valid_percent_count = 0

    for r in results:
        score = float(r['ResultScore']) if r['ResultScore'] is not None else 0
        exam_total = float(r['ExamTotalScore']) if r['ExamTotalScore'] is not None else 0

        if exam_total > 0:
            percent = (score / exam_total) * 100
            r['PercentScore'] = round(percent, 2)

            total_obtained += score
            total_possible += exam_total
            percent_sum += percent
            valid_percent_count += 1
        else:
            r['PercentScore'] = None

    overall_percent = round((total_obtained / total_possible) * 100, 2) if total_possible > 0 else 0
    average_percent = round(percent_sum / valid_percent_count, 2) if valid_percent_count > 0 else 0

    chart_labels = []
    chart_scores = []

    for r in results:
        chart_labels.append(r['Title'] if r['Title'] else 'بدون عنوان')
        chart_scores.append(r['PercentScore'] if r['PercentScore'] is not None else 0)

    context = {
        "results": results,
        "stats": {
            "total": total_exams,
            "passed": passed_exams,
            "failed": failed_exams,
            "overall_percent": overall_percent,
            "average_percent": average_percent,
        },
        "chart_labels": chart_labels,
        "chart_scores": chart_scores,
    }
    return render(request, "ExamResults/StudentResults.html", context)
