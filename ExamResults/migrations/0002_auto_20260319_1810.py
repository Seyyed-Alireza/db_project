from django.db import migrations, connection

def create_examresults_table(apps, schema_editor):
    vendor = connection.vendor

    if vendor == 'sqlite':
        sql = """
        CREATE TABLE IF NOT EXISTS "ExamResults" (
            "ResultID"   INTEGER PRIMARY KEY AUTOINCREMENT,
            "ExamKey"    INTEGER,
            "StudentKey" INTEGER NOT NULL,
            "TotalScore" INTEGER,
            "Status"     INTEGER NOT NULL DEFAULT 1,
            "Grade"      TEXT NOT NULL,
            "CalculatedAt" TEXT NOT NULL DEFAULT (datetime('now')),

            FOREIGN KEY ("ExamKey")
            REFERENCES "Exams" ("ExamID")
            ON DELETE SET NULL,

            FOREIGN KEY ("StudentKey")
            REFERENCES "Students" ("StudentID")
            ON DELETE CASCADE
        );
        """
    elif vendor == 'mysql':
        sql = """
        CREATE TABLE IF NOT EXISTS `ExamResults` (
            `ExamKey`     INT NOT NULL,
            `StudentKey`  INT NOT NULL,
            `TotalScore`  SMALLINT UNSIGNED,
            `Status`      BOOLEAN NOT NULL DEFAULT TRUE,
            `Grade`       VARCHAR(20) NOT NULL,
            `CalculatedAt` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

            PRIMARY KEY (`ExamKey`, `StudentKey`),

            CONSTRAINT `fk_examresult_exam`
                FOREIGN KEY (`ExamKey`)
                REFERENCES `Exams` (`ExamID`)
                ON DELETE CASCADE,

            CONSTRAINT `fk_examresult_student`
                FOREIGN KEY (`StudentKey`)
                REFERENCES `Students` (`UserKey`)
                ON DELETE CASCADE
        ) ENGINE=InnoDB;
        """
   
    schema_editor.execute(sql)

def drop_examresults_table(apps, schema_editor):
    schema_editor.execute('DROP TABLE IF EXISTS "ExamResults";')

class Migration(migrations.Migration):
    atomic = False
    
    dependencies = [
        ('ExamResults', '0001_initial')
    ]

    operations = [
        migrations.RunPython(create_examresults_table, reverse_code=drop_examresults_table)
    ]