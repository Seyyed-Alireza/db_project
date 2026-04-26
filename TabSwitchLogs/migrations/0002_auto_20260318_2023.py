from django.db import migrations, connection

def create_tabswitchlogs_table(apps, schema_editor):
    vendor = connection.vendor

    if vendor == 'sqlite':
        sql = """
        CREATE TABLE IF NOT EXISTS "TabSwitchLogs" (
            "LogID"       INTEGER PRIMARY KEY AUTOINCREMENT,
            "SessionKey"  INTEGER,
            "QuestionKey" INTEGER,
            "EventTime"   TEXT NOT NULL DEFAULT (datetime('now')),
            "EventType"   INTEGER,
            "Duration"    REAL,

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
        CREATE TABLE IF NOT EXISTS `TabSwitchLogs` (
            `LogID`       INT AUTO_INCREMENT PRIMARY KEY,
            `SessionKey`  INT,
            `QuestionKey` INT,
            `EventTime`   TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            `EventType`   SMALLINT,
            `Duration`    DECIMAL(65,2),

            CONSTRAINT `fk_tabswitchlog_session`
                FOREIGN KEY (`SessionKey`)
                REFERENCES `LoginSessions` (`SessionID`)
                ON DELETE CASCADE,

            CONSTRAINT `fk_tabswitchlog_question`
                FOREIGN KEY (`QuestionKey`)
                REFERENCES `Questions` (`QuestionID`)
                ON DELETE CASCADE
        ) ENGINE=InnoDB;
        """
    
    schema_editor.execute(sql)


def drop_tabswitchlogs_table(apps, schema_editor):
    schema_editor.execute('DROP TABLE IF EXISTS "TabSwitchLogs";')

class Migration(migrations.Migration):
    atomic = False
    
    dependencies = [
        ('TabSwitchLogs', '0001_initial'),
        ('LoginSessions', '0003_alter_loginsession_options'),
    ]

    operations = [
        migrations.RunPython(create_tabswitchlogs_table, reverse_code=drop_tabswitchlogs_table)
    ]