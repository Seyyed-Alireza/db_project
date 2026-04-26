from django.db import migrations, connection

def create_edustaffs_table(apps, schema_editor):
    vendor = connection.vendor

    if vendor == 'sqlite':
        sql = """
        CREATE TABLE IF NOT EXISTS "EduStaffs" (
            "EduID"         INTEGER PRIMARY KEY AUTOINCREMENT,
            "UserKey"       INTEGER NOT NULL,
            "DepartmentKey" INTEGER,

            FOREIGN KEY ("UserKey") 
            REFERENCES "Users" ("UserID") 
            ON DELETE CASCADE,

            FOREIGN KEY ("DepartmentKey")
            REFERENCES "Departments" ("DepartmentID")
            ON DELETE SET NULL
        );
        """
    elif vendor == 'mysql':
        sql = """
        CREATE TABLE IF NOT EXISTS `EduStaffs` (
            `EduID`         INT AUTO_INCREMENT PRIMARY KEY,
            `UserKey`       INT NOT NULL,
            `DepartmentKey` INT,

            CONSTRAINT `uq_edustaff_user` UNIQUE (`UserKey`),

            CONSTRAINT `fk_edustaff_user`
                FOREIGN KEY (`UserKey`) 
                REFERENCES `Users` (`UserID`) 
                ON DELETE CASCADE,

            CONSTRAINT `fk_edustaff_department`
                FOREIGN KEY (`DepartmentKey`)
                REFERENCES `Departments` (`DepartmentID`)
                ON DELETE SET NULL
        ) ENGINE=InnoDB;
        """

    schema_editor.execute(sql)

def drop_edustaffs_table(apps, schema_editor):
    schema_editor.execute('DROP TABLE IF EXISTS "EduStaffs";')

class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ('EduStaffs', '0001_initial')
    ]

    operations = [
        migrations.RunPython(create_edustaffs_table, reverse_code=drop_edustaffs_table)
    ]