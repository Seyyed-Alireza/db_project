from django.db import migrations, connection

def create_courses_table(apps, schema_editor):
    vendor = connection.vendor

    if vendor == 'sqlite':
        sql = """
        CREATE TABLE IF NOT EXISTS "Courses" (
            "CourseID"            INTEGER PRIMARY KEY AUTOINCREMENT,
            "CourseName"          TEXT    NOT NULL,
            "CourseCode"          TEXT    NOT NULL UNIQUE,
            "Units"               INTEGER NOT NULL,
            "CoursePasswordHash"  TEXT,
            "DepartmentKey"       INTEGER NOT NULL,
            "TeacherKey"          INTEGER,

            FOREIGN KEY ("DepartmentKey")
                REFERENCES "Departments" ("DepartmentID")
                ON DELETE CASCADE

            FOREIGN KEY ("TeacherKey")
                REFERENCES "Teachers" ("TeacherID")
                ON DELETE SET NULL
        );
        """

    elif vendor == 'mysql':
        sql = """
        CREATE TABLE IF NOT EXISTS `Courses` (
            `CourseID`            INT AUTO_INCREMENT PRIMARY KEY,
            `CourseName`          VARCHAR(100) NOT NULL,
            `CourseCode`          VARCHAR(20)  NOT NULL UNIQUE,
            `Units`               SMALLINT UNSIGNED NOT NULL,
            `CoursePasswordHash`  VARCHAR(255),
            `DepartmentKey`       INT NOT NULL,
            `TeacherKey`          INT,

            CONSTRAINT `fk_course_department`
                FOREIGN KEY (`DepartmentKey`)
                REFERENCES `Departments` (`DepartmentID`)
                ON DELETE CASCADE,

            CONSTRAINT `fk_course_teacher`
                FOREIGN KEY (`TeacherKey`) 
                REFERENCES `Teachers` (`UserKey`)
                ON DELETE SET NULL
        ) ENGINE=InnoDB;
        """

    schema_editor.execute(sql)


def drop_courses_table(apps, schema_editor):
    schema_editor.execute('DROP TABLE IF EXISTS "Courses";')


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ('Courses', '0002_alter_course_table'),
        ('Departments', '0003_auto_20260318_1602'),
        ('Teachers', '0004_alter_teacher_options'),
    ]

    operations = [
        migrations.RunPython(create_courses_table, reverse_code=drop_courses_table)
    ]