from django.db import migrations, connection

def create_questions_table(apps, schema_editor):
    vendor = connection.vendor

    if vendor == 'sqlite':
        sql = """
        CREATE TABLE IF NOT EXISTS "Questions" (
            "QuestionID"    INTEGER PRIMARY KEY AUTOINCREMENT,
            "ExamKey"       INTEGER NOT NULL,
            "QuestionType"  INTEGER NOT NULL,
            "QuestionText"  TEXT NOT NULL,
            "QuestionImage" TEXT,
            "Score"         REAL NOT NULL,

            FOREIGN KEY ("ExamKey")
            REFERENCES "Exams" ("ExamID")
            ON DELETE CASCADE
        );
        """
    elif vendor == 'mysql':
        sql = """
        CREATE TABLE IF NOT EXISTS `Questions` (
            `QuestionID`    INT AUTO_INCREMENT PRIMARY KEY,
            `ExamKey`       INT NOT NULL,
            `QuestionType`  INT NOT NULL,
            `QuestionText`  TEXT NOT NULL,
            `QuestionImage` VARCHAR(200),
            `Score`         DECIMAL(5,2) NOT NULL,
            `Order`         INT NOT NULL DEFAULT 1,

            CONSTRAINT `fk_question_exam`
                FOREIGN KEY (`ExamKey`)
                REFERENCES `Exams` (`ExamID`) 
                ON DELETE CASCADE
        ) ENGINE=InnoDB;
        """

    schema_editor.execute(sql)

def drop_questions_table(apps, schema_editor):
    schema_editor.execute('DROP TABLE IF EXISTS "Questions";')

class Migration(migrations.Migration):
    atomic = False
    
    dependencies = [
        ('Questions', '0002_alter_question_options_alter_question_table'),
        ('Exams', '0003_auto_20260318_1720'),
    ]

    operations = [
        migrations.RunPython(create_questions_table, reverse_code=drop_questions_table)
    ]