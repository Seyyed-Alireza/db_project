from django.db import migrations, connection

def create_students_table(apps, schema_editor):
    vendor = connection.vendor

    if vendor == 'sqlite':
        sql = """
        CREATE TABLE IF NOT EXISTS "Students" (
            "StudentID"      INTEGER PRIMARY KEY AUTOINCREMENT,
            "StudentNumber"  TEXT NOT NULL UNIQUE,
            "UserKey"        INTEGER NOT NULL,
            "DepartmentKey"  INTEGER,

            FOREIGN KEY ("UserKey")
            REFERENCES "Users" ("UserID")
            ON DELETE CASCADE

            FOREIGN KEY ("DepartmentKey")
            REFERENCES "Departments" ("DepartmentID")
            ON DELETE SET NULL
        );
        """

    elif vendor == 'mysql':
        sql = """
        CREATE TABLE IF NOT EXISTS `Students` (
            `StudentNumber`  VARCHAR(20) NOT NULL UNIQUE,
            `UserKey`        INT PRIMARY KEY,
            `DepartmentKey`  INT NULL,

            CONSTRAINT `fk_student_user`
                FOREIGN KEY (`UserKey`)
                REFERENCES `Users` (`UserID`)
                ON DELETE CASCADE,

            CONSTRAINT `fk_student_department`
                FOREIGN KEY (`DepartmentKey`)
                REFERENCES `Departments` (`DepartmentID`)
                ON DELETE SET NULL
        ) ENGINE=InnoDB;
        """

    schema_editor.execute(sql)

def drop_students_table(apps, schema_editor):
    schema_editor.execute('DROP TABLE IF EXISTS "Students";')

class Migration(migrations.Migration):
    atomic = False
    
    dependencies = [
        ('Students', '0002_alter_student_options_alter_student_table'),
        ('Departments', '0003_auto_20260318_1602'),
        ('Users', '0003_alter_user_options'),
    ]

    operations = [
        migrations.RunPython(create_students_table, reverse_code=drop_students_table)
    ]