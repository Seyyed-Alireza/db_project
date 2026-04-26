from django.db import migrations, connection

def create_fraudflags_table(apps, schema_editor):
    vendor = connection.vendor

    if vendor == 'sqlite':
        sql = """
        CREATE TABLE IF NOT EXISTS "FraudFlags" (
            "FlagID"      INTEGER PRIMARY KEY AUTOINCREMENT,
            "SessionKey" INTEGER,
            "QuestionKey" INTEGER,
            "Reason"      TEXT,
            "RiskScore"   INTEGER NOT NULL DEFAULT 0,
            "Severity"    TEXT NOT NULL,
            "FlagType"    TEXT,
            "Status"      TEXT NOT NULL,
            "GeneratedAt" TEXT NOT NULL DEFAULT (datetime('now')),

            FOREIGN KEY ("SessionKey")
            REFERENCES "LoginSessions" ("SessionID")
            ON DELETE NO ACTION,

            FOREIGN KEY ("QuestionKey")
            REFERENCES "Questions" ("QuestionID")
            ON DELETE CASCADE
        );
        """
    elif vendor == 'mysql':
        sql = """
        CREATE TABLE IF NOT EXISTS `FraudFlags` (
            `FlagID`      INT AUTO_INCREMENT PRIMARY KEY,
            `SessionKey`  INT,
            `QuestionKey` INT,
            `Reason`      TEXT,
            `RiskScore`   SMALLINT UNSIGNED NOT NULL DEFAULT 0,
            `Severity`    VARCHAR(100) NOT NULL,
            `FlagType`    TEXT,
            `Status`      VARCHAR(100) NOT NULL,
            `GeneratedAt` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

            CONSTRAINT `fk_fraudflag_session`
                FOREIGN KEY (`SessionKey`)
                REFERENCES `LoginSessions` (`SessionID`)
                ON DELETE NO ACTION,

            CONSTRAINT `fk_fraudflag_question`
                FOREIGN KEY (`QuestionKey`)
                REFERENCES `Questions` (`QuestionID`)
                ON DELETE CASCADE
        ) ENGINE=InnoDB;
        """

    schema_editor.execute(sql)


def drop_fraudflags_table(apps, schema_editor):
    schema_editor.execute('DROP TABLE IF EXISTS "FraudFlags";')

class Migration(migrations.Migration):
    atomic = False
    
    dependencies = [
        ('FraudFlags', '0001_initial'),
        ('LoginSessions', '0003_alter_loginsession_options'),
    ]

    operations = [
        migrations.RunPython(create_fraudflags_table, reverse_code=drop_fraudflags_table)
    ]