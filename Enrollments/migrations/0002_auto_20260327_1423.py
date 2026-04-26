from django.db import migrations, connection

def create_enrollments_table(apps, schema_editor):
    vendor = connection.vendor
    if vendor == 'sqlite':
        sql = """
        CREATE TABLE IF NOT EXISTS "Enrollments" (
            "EnrollmentID" INTEGER PRIMARY KEY AUTOINCREMENT,
            "StudentKey"    INTEGER NOT NULL,
            "CourseKey"     INTEGER NOT NULL,
            "EnrolledAt"   TEXT NOT NULL DEFAULT (datetime('now')),
            "Grade"        TEXT,
            "Status"       TEXT NOT NULL DEFAULT 'active',

            FOREIGN KEY ("StudentKey")
            REFERENCES "Students" ("StudentID")
            ON DELETE CASCADE,

            FOREIGN KEY ("CourseKey")
            REFERENCES "Courses" ("CourseID")
            ON DELETE CASCADE,

            UNIQUE ("StudentKey", "CourseKey")
        );
        """
    elif vendor == 'mysql':
        sql = """
        CREATE TABLE IF NOT EXISTS `Enrollments` (
            `StudentKey`    INT NOT NULL,
            `CourseKey`     INT NOT NULL,
            `EnrolledAt`    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            `Grade`         VARCHAR(5),
            `Status`        VARCHAR(20) NOT NULL DEFAULT 'active',

            PRIMARY KEY (`StudentKey`, `CourseKey`),

            CONSTRAINT `fk_enrollment_student`
                FOREIGN KEY (`StudentKey`)
                REFERENCES `Students` (`UserKey`)
                ON DELETE CASCADE,

            CONSTRAINT `fk_enrollment_course`
                FOREIGN KEY (`CourseKey`)
                REFERENCES `Courses` (`CourseID`)
                ON DELETE CASCADE
        ) ENGINE=InnoDB;
        """

    schema_editor.execute(sql)

def drop_enrollments_table(apps, schema_editor):
    schema_editor.execute('DROP TABLE IF EXISTS "Enrollments";')

class Migration(migrations.Migration):
    atomic = False
    
    dependencies = [
        ('Enrollments', '0001_initial')
    ]

    operations = [
        migrations.RunPython(create_enrollments_table, reverse_code=drop_enrollments_table)
    ]