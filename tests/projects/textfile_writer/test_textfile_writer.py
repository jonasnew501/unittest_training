import pytest

from unittest_training.projects.textfile_writer.textfile_writer import(
    TextfileWriter,
    file_path
)


class TestTextfileWriter:
    """
    This class holds the Unittest-cases for textfile-writer-application
    in 'unittest_training.projects.textfile_writer.textfile_writer.TextfileWriter'.

    In the following, an overview is given about both the happy path and potential,
    realistic unhappy paths of this application and the desired behavior for each.
    This summary/overview is the starting-point for creating the unittests for this
    application.

    - Happy Path:
        *The txt-file is created at the specified path, the specific text is written
         to the buffer, the buffer is flushed (i.e. the text is actually written to
         the file), and the file-handle is closed.
    -Unhappy Paths:
        *The file cannot be created.
            -->Desired behavior: A custom Exception is raised.
        *The writing to the file fails (OSError on flush).
            -->Desired behavior: The rollback is conducted successfully, i.e. if the
                                 file does exist already it is deleted again.
        *The rollback fails, i.e. the file exists, but cannot be deleted.
            -->Desired behavior: A custom Exception is raised.
        *The file-handle cannot be closed.
            -->Desired behavior: A custom Exception is raised.
    """
    @staticmethod
    @pytest.mark.parametrize(
        "text_to_write, file_path",
        [
            ("SomeString", file_path),
            ("", file_path),

        ]
    )
    def test_process_textfile_valid_inputs(text_to_write: str, file_path: str):
        TextfileWriter.process_textfile(text_to_write=text_to_write, file_path=file_path)

        #