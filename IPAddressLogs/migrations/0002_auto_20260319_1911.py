from django.db import migrations, connection

def create_ipaddresslogs_table(apps, schema_editor):
    vendor = connection.vendor

    if vendor == 'sqlite':
        sql = """
        CREATE TABLE IF NOT EXISTS "IPAddressLogs" (
            "LogID"      INTEGER PRIMARY KEY AUTOINCREMENT,
            "SessionKey" INTEGER,
            "IPAddress"  TEXT,
            "LogTime"    TEXT NOT NULL DEFAULT (datetime('now')),
            "Location"   TEXT,

            FOREIGN KEY ("SessionKey")
            REFERENCES "LoginSessions" ("SessionID")
            ON DELETE NO ACTION
        );
        """
    elif vendor == 'mysql':
        sql = """
        CREATE TABLE IF NOT EXISTS `IPAddressLogs` (
            `LogID`      INT AUTO_INCREMENT PRIMARY KEY,
            `SessionKey` INT,
            `IPAddress`  VARCHAR(45) NULL,
            `LogTime`    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            `Location`   VARCHAR(200) NULL,
            
            CONSTRAINT `fk_ipaddresslog_session`
                FOREIGN KEY (`SessionKey`)
                REFERENCES `LoginSessions` (`SessionID`)
                ON DELETE CASCADE
        ) ENGINE=InnoDB;
        """
    
    schema_editor.execute(sql)

def drop_ipaddresslogs_table(apps, schema_editor):
    """Удалить таблицу при откате миграции."""
    schema_editor.execute('DROP TABLE IF EXISTS "IPAddressLogs";')

class Migration(migrations.Migration):
    atomic = False
    
    dependencies = [
        ('IPAddressLogs', '0001_initial'),
        ('LoginSessions', '0003_alter_loginsession_options'),
    ]

    operations = [
        migrations.RunPython(create_ipaddresslogs_table, reverse_code=drop_ipaddresslogs_table)
    ]