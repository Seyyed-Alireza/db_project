from django.db import migrations, connection

def create_teachers_table(apps, schema_editor):
    vendor = connection.vendor

    if vendor == 'sqlite':
        sql = """
        CREATE TABLE IF NOT EXISTS "Teachers" (
            "TeacherId"     INTEGER PRIMARY KEY AUTOINCREMENT,
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
        CREATE TABLE IF NOT EXISTS `Teachers` (
            `UserKey`       INT PRIMARY KEY,
            `DepartmentKey` INT,

            CONSTRAINT `fk_teacher_user`
                FOREIGN KEY (`UserKey`) 
                REFERENCES `Users` (`UserID`) 
                ON DELETE CASCADE,

            CONSTRAINT `fk_teacher_department`
                FOREIGN KEY (`DepartmentKey`) 
                REFERENCES `Departments` (`DepartmentID`) 
                ON DELETE SET NULL
        ) ENGINE=InnoDB;
        """
    
    schema_editor.execute(sql)


def drop_teachers_table(apps, schema_editor):
    schema_editor.execute('DROP TABLE IF EXISTS "Teachers";')


class Migration(migrations.Migration):
    atomic = False
    
    dependencies = [
        ('Teachers', '0001_initial'),
        ('Departments', '0003_auto_20260318_1602'),
        ('Users', '0003_alter_user_options'),
    ]

    operations = [
        migrations.RunPython(create_teachers_table, reverse_code=drop_teachers_table)
    ]