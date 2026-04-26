from django.db import migrations, connection

def create_questionoptions_table(apps, schema_editor):
    vendor = connection.vendor

    if vendor == 'sqlite':
        sql = """
        CREATE TABLE IF NOT EXISTS "QuestionOptions" (
            "OptionID"    INTEGER PRIMARY KEY AUTOINCREMENT,
            "QuestionKey" INTEGER NOT NULL,
            "OptionText"  TEXT,
            "OptionLabel" TEXT NOT NULL,
            "IsCorrect"   INTEGER NOT NULL DEFAULT 0,

            FOREIGN KEY ("QuestionKey")
            REFERENCES "Questions" ("QuestionID")
            ON DELETE CASCADE
        );
        """
    elif vendor == 'mysql':
        sql = """
        CREATE TABLE IF NOT EXISTS `QuestionOptions` (
            `OptionID`    INT AUTO_INCREMENT PRIMARY KEY,
            `QuestionKey` INT NOT NULL,
            `OptionText`  TEXT,
            `OptionLabel` VARCHAR(100) NOT NULL,
            `IsCorrect`   BOOLEAN NOT NULL DEFAULT FALSE,

            CONSTRAINT `fk_questionoption_question`
                FOREIGN KEY (`QuestionKey`)
                REFERENCES `Questions` (`QuestionID`)
                ON DELETE CASCADE
        ) ENGINE=InnoDB;
        """

    schema_editor.execute(sql)


def drop_questionoptions_table(apps, schema_editor):
    schema_editor.execute('DROP TABLE IF EXISTS "QuestionOptions";')


class Migration(migrations.Migration):
    atomic = False
    
    dependencies = [
        ('QuestionOptions', '0001_initial'),
        ('Questions', '0004_alter_question_options'),
    ]

    operations = [
        migrations.RunPython(create_questionoptions_table, reverse_code=drop_questionoptions_table)
    ]