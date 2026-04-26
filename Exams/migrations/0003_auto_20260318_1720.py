from django.db import migrations, connection

def create_exams_table(apps, schema_editor):
    vendor = connection.vendor

    if vendor == 'sqlite':
        sql = """
        CREATE TABLE IF NOT EXISTS "Exams" (
            "ExamID"      INTEGER PRIMARY KEY AUTOINCREMENT,
            "CourseKey"   INTEGER NOT NULL,
            "TeacherKey"  INTEGER NOT NULL,
            "Title"       TEXT    NOT NULL,
            "StartTime"   TEXT    NOT NULL,
            "EndTime"     TEXT    NOT NULL,
            "Duration"    INTEGER,
            "Description" TEXT,
            "TotalScore"  REAL,

            FOREIGN KEY ("CourseKey")
                REFERENCES "Courses" ("CourseID")
                ON DELETE CASCADE,

            FOREIGN KEY ("TeacherKey")
                REFERENCES "Teachers" ("TeacherID")
                ON DELETE CASCADE
        );
        """

    elif vendor == 'mysql':
        sql = """
        CREATE TABLE IF NOT EXISTS `Exams` (
            `ExamID`      INT AUTO_INCREMENT PRIMARY KEY,
            `CourseKey`   INT NOT NULL,
            `TeacherKey`  INT NOT NULL,
            `Title`       VARCHAR(200) NOT NULL,
            `StartTime`   TIMESTAMP NOT NULL,
            `EndTime`     TIMESTAMP NOT NULL,
            `Duration`    INT NULL,
            `Description` TEXT,
            `TotalScore`  DECIMAL(5,2) NULL DEFAULT 0,

            CONSTRAINT `fk_exam_course`
                FOREIGN KEY (`CourseKey`)
                REFERENCES `Courses` (`CourseID`)
                ON DELETE CASCADE,

            CONSTRAINT `fk_exam_teacher`
                FOREIGN KEY (`TeacherKey`)
                REFERENCES `Teachers` (`UserKey`)
                ON DELETE CASCADE
        ) ENGINE=InnoDB;
        """

    schema_editor.execute(sql)

def drop_exams_table(apps, schema_editor):
    schema_editor.execute('DROP TABLE IF EXISTS "Exams";')

class Migration(migrations.Migration):
    atomic = False
    
    dependencies = [
        ('Exams', '0002_alter_exam_table'),
        ('Teachers', '0004_alter_teacher_options'),
        ('Courses', '0003_auto_20260318_1625'),
    ]

    operations = [
        migrations.RunPython(create_exams_table, reverse_code=drop_exams_table)
    ]