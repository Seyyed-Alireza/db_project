from django.db import migrations, connection

def create_departments_table(apps, schema_editor):
    vendor = connection.vendor
    if vendor == 'sqlite':
        sql = """
        CREATE TABLE IF NOT EXISTS "Departments" (
            "DepartmentID"   INTEGER PRIMARY KEY AUTOINCREMENT,
            "DepartmentName" TEXT    NOT NULL,
            "Location"       TEXT,
            "Phone"          TEXT
        );
        """

    elif vendor == 'mysql':
        sql = """
        CREATE TABLE IF NOT EXISTS `Departments` (
            `DepartmentID`   INT AUTO_INCREMENT PRIMARY KEY,
            `DepartmentName` VARCHAR(100) NOT NULL,
            `Location`       VARCHAR(200),
            `Phone`          VARCHAR(20)
        ) ENGINE=InnoDB;
        """

    schema_editor.execute(sql)

def drop_departments_table(apps, schema_editor):
    schema_editor.execute('DROP TABLE IF EXISTS "Departments";')

class Migration(migrations.Migration):
    atomic = False
    
    dependencies = [
        ('Departments', '0002_alter_department_table'),
    ]

    operations = [
        migrations.RunPython(create_departments_table, reverse_code=drop_departments_table)
    ]