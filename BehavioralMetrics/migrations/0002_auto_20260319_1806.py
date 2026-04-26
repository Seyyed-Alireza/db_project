from django.db import migrations, connection

def create_behavioralmetrics_table(apps, schema_editor):
    vendor = connection.vendor

    if vendor == 'sqlite':
        sql = """
        CREATE TABLE IF NOT EXISTS "BehavioralMetrics" (
            "MetricID"        INTEGER PRIMARY KEY AUTOINCREMENT,
            "SessionKey"      INTEGER,
            "QuestionKey"     INTEGER,
            "TotalTimeSpent"  INTEGER NOT NULL DEFAULT 0,
            "VisitCount"      INTEGER NOT NULL DEFAULT 1,
            "TabSwitchCount"  INTEGER NOT NULL DEFAULT 0,
            "CopyPasteCount"  INTEGER NOT NULL DEFAULT 0,
            "IdleTime"        INTEGER NOT NULL DEFAULT 0,

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
        CREATE TABLE IF NOT EXISTS `BehavioralMetrics` (
            `SessionKey`      INT,
            `QuestionKey`     INT,
            `TotalTimeSpent`  INT NOT NULL DEFAULT 0,
            `VisitCount`      SMALLINT UNSIGNED NOT NULL DEFAULT 1,
            `TabSwitchCount`  SMALLINT UNSIGNED NOT NULL DEFAULT 0,
            `CopyPasteCount`  SMALLINT UNSIGNED NOT NULL DEFAULT 0,
            `IdleTime`        INT NOT NULL DEFAULT 0,

            PRIMARY KEY (`SessionKey`, `QuestionKey`),

            CONSTRAINT `fk_behavioralmetric_session`
                FOREIGN KEY (`SessionKey`)
                REFERENCES `LoginSessions` (`SessionID`)
                ON DELETE NO ACTION,

            CONSTRAINT `fk_behavioralmetric_question`
                FOREIGN KEY (`QuestionKey`)
                REFERENCES `Questions` (`QuestionID`)
                ON DELETE NO ACTION
        ) ENGINE=InnoDB;
        """
    
    schema_editor.execute(sql)

def drop_behavioralmetrics_table(apps, schema_editor):
    schema_editor.execute('DROP TABLE IF EXISTS "BehavioralMetrics";')

class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ('BehavioralMetrics', '0001_initial'),
        ('LoginSessions', '0003_alter_loginsession_options'),
    ]

    operations = [
        migrations.RunPython(create_behavioralmetrics_table, reverse_code=drop_behavioralmetrics_table)
    ]