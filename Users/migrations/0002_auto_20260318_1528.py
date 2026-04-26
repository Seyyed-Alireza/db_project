from django.db import migrations, connection

def create_user_table(apps, schema_editor):
    vendor = connection.vendor

    if vendor == 'sqlite':
        sql = """
        CREATE TABLE IF NOT EXISTS "Users" (
            "UserID"       INTEGER PRIMARY KEY AUTOINCREMENT,
            "Username"     TEXT    NOT NULL UNIQUE,
            "FirstName"    TEXT    NOT NULL,
            "LastName"     TEXT    NOT NULL,
            "PasswordHash" TEXT    NOT NULL,
            "Role"         TEXT    NOT NULL,
            "Email"        TEXT,
            "PhoneNumber"  TEXT,
            "CreatedAt"    TEXT    NOT NULL DEFAULT (datetime('now')),
            "IsLoggedIn"   INTEGER NOT NULL DEFAULT 0
        );
        """

    elif vendor == 'mysql':
        sql = """
        CREATE TABLE IF NOT EXISTS `Users` (
            `UserID`       INT AUTO_INCREMENT PRIMARY KEY,
            `Username`     VARCHAR(150) NOT NULL UNIQUE,
            `FirstName`    VARCHAR(100) NOT NULL,
            `LastName`     VARCHAR(100) NOT NULL,
            `PasswordHash` VARCHAR(255) NOT NULL,
            `Role`         VARCHAR(50)  NOT NULL,
            `Email`        VARCHAR(254),
            `PhoneNumber`  VARCHAR(15),
            `CreatedAt`    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            `IsLoggedIn`   BOOLEAN NOT NULL DEFAULT FALSE
        ) ENGINE=InnoDB;
        """

    schema_editor.execute(sql)

def drop_user_table(apps, schema_editor):
    schema_editor.execute('DROP TABLE IF EXISTS "Users";')

class Migration(migrations.Migration):
    atomic = False
    
    dependencies = [
        ('Users', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_user_table, reverse_code=drop_user_table)
    ]