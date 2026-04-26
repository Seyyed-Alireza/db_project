from django.db import migrations, connection

def create_questionviewlogs_table(apps, schema_editor):
    vendor = connection.vendor

    if vendor == 'sqlite':
        sql = """
        CREATE TABLE IF NOT EXISTS "QuestionViewLogs" (
            "ViewLogID"      INTEGER PRIMARY KEY AUTOINCREMENT,
            "SessionKey"     INTEGER,
            "QuestionKey"    INTEGER,
            "ViewStartTime"  TEXT,
            "ViewEndTime"    TEXT,
            "Duration"       INTEGER,

            FOREIGN KEY ("SessionKey")
            REFERENCES "LoginSessions" ("SessionID")
            ON DELETE NO ACTION,

            FOREIGN KEY ("QuestionKey")
            REFERENCES "Questions" ("QuestionID")
            ON DELETE NO ACTION
        );
        """
    elif vendor == 'mysql':
        sql = """
        CREATE TABLE IF NOT EXISTS `QuestionViewLogs` (
            `SessionKey`     INT,
            `QuestionKey`    INT,
            `ViewStartTime`  TIMESTAMP NULL,
            `ViewEndTime`    TIMESTAMP NULL,
            `Duration`       INT NULL,

            PRIMARY KEY (`SessionKey`, `QuestionKey`),

            CONSTRAINT `fk_questionviewlog_session`
                FOREIGN KEY (`SessionKey`)
                REFERENCES `LoginSessions` (`SessionID`)
                ON DELETE CASCADE,

            CONSTRAINT `fk_questionviewlog_question`
                FOREIGN KEY (`QuestionKey`)
                REFERENCES `Questions` (`QuestionID`)
                ON DELETE CASCADE
        ) ENGINE=InnoDB;
        """

    schema_editor.execute(sql)

def drop_questionviewlogs_table(apps, schema_editor):
    schema_editor.execute('DROP TABLE IF EXISTS "QuestionViewLogs";')

class Migration(migrations.Migration):
    atomic = False
    
    dependencies = [
        ('QuestionViewLogs', '0001_initial'),
        ('LoginSessions', '0003_alter_loginsession_options'),
    ]

    operations = [
        migrations.RunPython(create_questionviewlogs_table, reverse_code=drop_questionviewlogs_table)
    ]