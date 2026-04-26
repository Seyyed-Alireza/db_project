from django.db import migrations, connection

def create_answers(apps, schema_editor):
    vendor = connection.vendor

    if vendor == 'sqlite':
        sql = """
            CREATE TABLE IF NOT EXISTS "Answers" (
                "AnswerID"          INTEGER PRIMARY KEY AUTOINCREMENT,
                "AnswerText"        TEXT,
                "IsCorrect"         INTEGER NOT NULL DEFAULT 0,
                "AnswerImage"       TEXT,
                "IsGraded"          INTEGER NOT NULL DEFAULT 0,
                "GivenScore"        REAL,
                "SubmittedAt"       TEXT NOT NULL DEFAULT (datetime('now')),

                "QuestionKey"       INTEGER,
                "StudentKey"        INTEGER NOT NULL,
                "SelectedOptionKey" INTEGER DEFAULT NULL,

                FOREIGN KEY ("QuestionKey")
                REFERENCES "Questions" ("QuestionID")
                ON DELETE SET NULL,

                FOREIGN KEY ("StudentKey")
                REFERENCES "Students" ("StudentID")
                ON DELETE CASCADE

                FOREIGN KEY ("SelectedOptionKey")
                REFERENCES "QuestionOptions" ("OptionID")
                ON DELETE SET NULL
            );
        """
    elif vendor == 'mysql':
        sql = """
        CREATE TABLE IF NOT EXISTS `Answers` (
            `AnswerText`        TEXT,
            `IsCorrect`         BOOLEAN NULL DEFAULT FALSE,
            `AnswerFile`       VARCHAR(200),
            `IsGraded`          TINYINT NOT NULL DEFAULT 0,
            `GivenScore`        DECIMAL(5,2),
            `SubmittedAt`       TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            `QuestionKey`       INT NOT NULL,
            `StudentKey`        INT NOT NULL,
            `SelectedOptionKey` INT NULL,

            PRIMARY KEY (`StudentKey`, `QuestionKey`),

            CONSTRAINT `fk_answer_question`
                FOREIGN KEY (`QuestionKey`)
                REFERENCES `Questions` (`QuestionID`)
                ON DELETE CASCADE,

            CONSTRAINT `fk_answer_student`
                FOREIGN KEY (`StudentKey`)
                REFERENCES `Students` (`UserKey`)
                ON DELETE CASCADE,

            CONSTRAINT `fk_answer_option`
                FOREIGN KEY (`SelectedOptionKey`)
                REFERENCES `QuestionOptions` (`OptionID`)
                ON DELETE SET NULL
        ) ENGINE=InnoDB;
    """

    schema_editor.execute(sql)

def drop_answers(apps, schema_editor):
    schema_editor.execute('DROP TABLE IF EXISTS "Answers";')

class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ('Answers', '0001_initial'),
        ('Questions', '0004_alter_question_options'),
        ('Students', '0005_alter_student_options'),
        ('QuestionOptions', '0003_alter_questionoption_options'),
        ]
    
    operations = [
        migrations.RunPython(create_answers, reverse_code=drop_answers)
    ]

