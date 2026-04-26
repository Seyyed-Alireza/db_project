from django.db import migrations, connection

def create_resolutionlogs_table(apps, schema_editor):
    vendor = connection.vendor

    if vendor == 'sqlite':
        sql = """
        CREATE TABLE IF NOT EXISTS "ResolutionLogs" (
            "LogID"        INTEGER PRIMARY KEY AUTOINCREMENT,
            "SessionKey"   INTEGER,
            "ScreenWidth"  INTEGER,
            "ScreenHeight" INTEGER,
            "WindowWidth"  INTEGER,
            "WindowHeight" INTEGER,
            "ChangeTime"   TEXT NOT NULL DEFAULT (datetime('now')),

            FOREIGN KEY ("SessionKey")
            REFERENCES "LoginSessions" ("SessionID")
            ON DELETE NO ACTION
        );
        """
    elif vendor == 'mysql':
        sql = """
        CREATE TABLE IF NOT EXISTS `ResolutionLogs` (
            `LogID`        INT AUTO_INCREMENT PRIMARY KEY,
            `SessionKey`   INT,
            `ScreenWidth`  SMALLINT UNSIGNED NULL,
            `ScreenHeight` SMALLINT UNSIGNED NULL,
            `WindowWidth`  SMALLINT UNSIGNED NULL,
            `WindowHeight` SMALLINT UNSIGNED NULL,
            `ChangeTime`   TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

            CONSTRAINT `fk_resolutionlog_session`
                FOREIGN KEY (`SessionKey`)
                REFERENCES `LoginSessions` (`SessionID`)
                ON DELETE CASCADE
        ) ENGINE=InnoDB;
        """
   
    schema_editor.execute(sql)


def drop_resolutionlogs_table(apps, schema_editor):
    schema_editor.execute('DROP TABLE IF EXISTS "ResolutionLogs";')

class Migration(migrations.Migration):
    atomic = False
    
    dependencies = [
        ('ResolutionLogs', '0001_initial'),
        ('LoginSessions', '0003_alter_loginsession_options'),
    ]

    operations = [
        migrations.RunPython(create_resolutionlogs_table, reverse_code=drop_resolutionlogs_table)
    ]