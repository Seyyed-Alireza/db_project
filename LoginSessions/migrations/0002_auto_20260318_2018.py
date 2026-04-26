from django.db import migrations, connection

def create_loginsessions_table(apps, schema_editor):
    vendor = connection.vendor

    if vendor == 'sqlite':
        sql = """
        CREATE TABLE IF NOT EXISTS "LoginSessions" (
            "SessionID"   INTEGER PRIMARY KEY AUTOINCREMENT,
            "StudentKey"  INTEGER NOT NULL,
            "ExamKey"     INTEGER,
            "LoginTime"   TEXT,
            "LogoutTime"  TEXT,
            "IsActive"    INTEGER NOT NULL DEFAULT 1,

            FOREIGN KEY ("StudentKey")
            REFERENCES "Students" ("StudentID")
            ON DELETE CASCADE,

            FOREIGN KEY ("ExamKey")
            REFERENCES "Exams" ("ExamID")
            ON DELETE SET NULL
        );
        """
    elif vendor == 'mysql':
        sql = """
        CREATE TABLE IF NOT EXISTS `LoginSessions` (
            `SessionID`   INT AUTO_INCREMENT PRIMARY KEY,
            `StudentKey`  INT NOT NULL,
            `ExamKey`     INT,
            `LoginTime`   TIMESTAMP NULL,
            `LogoutTime`  TIMESTAMP NULL,
            `IsActive`    BOOLEAN NOT NULL DEFAULT TRUE,

            CONSTRAINT `fk_loginsession_student`
                FOREIGN KEY (`StudentKey`)
                REFERENCES `Students` (`UserKey`)
                ON DELETE CASCADE,

            CONSTRAINT `fk_loginsession_exam`
                FOREIGN KEY (`ExamKey`)
                REFERENCES `Exams` (`ExamID`)
                ON DELETE SET NULL
        ) ENGINE=InnoDB;
        """
    
    schema_editor.execute(sql)

def drop_loginsessions_table(apps, schema_editor):
    schema_editor.execute('DROP TABLE IF EXISTS "LoginSessions";')

class Migration(migrations.Migration):
    atomic = False
    
    dependencies = [
        ('LoginSessions', '0001_initial')
    ]

    operations = [
        migrations.RunPython(create_loginsessions_table, reverse_code=drop_loginsessions_table)
    ]