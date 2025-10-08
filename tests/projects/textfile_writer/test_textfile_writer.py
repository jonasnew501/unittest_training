import os
import pytest

from unittest_training.projects.textfile_writer.textfile_writer import (
    TextfileWriter,
    FileCreationError,
    text_to_write,
    filename,
    current_dir_path,
    file_path,
)


class TestTextfileWriter:
    """
    This class holds the Unittest-cases for the textfile-writer-application
    in 'unittest_training.projects.textfile_writer.textfile_writer.TextfileWriter'.

    In the following, an overview is given about both the happy path and potential,
    realistic unhappy paths of this application and the desired behavior for each.
    This summary/overview is the starting-point for creating the unittests for this
    application.

    - Happy Path:
        *The txt-file is created at the specified path, the specific text is written
         to the buffer, the buffer is flushed (i.e. the text is actually written to
         the file), and the file-handle is closed.
    - Unhappy Paths:
        *The file cannot be created.
            -->Desired behavior: A custom Exception is raised.
        *The writing to the file fails (OSError on flush).
            -->Desired behavior: The rollback is conducted successfully, i.e. if the
                                 file does exist already it is deleted again.
        *The rollback fails, i.e. the file exists, but cannot be deleted.
            -->Desired behavior: A custom Exception is raised.
        *The file-handle cannot be closed.
            -->Desired behavior: A custom Exception is raised.

    It is important to specify the conceptualization of the textfile_writer-application:
    There is one "main"-function "process_textfile", and multiple helper-functions (with
    a leading "_" in their name). Process_textfile brings together all those helper-functions
    in a sensible way. The only function to be called by a user is "process_textfile", the
    helper-functions are not intended to be called from the outside of the class "TextfileWriter".
    """

    #-----unittests for helper-functions--------
    @staticmethod
    def test_close_file_handle(tmp_path):
        file_path = tmp_path / "Testfile.txt"

        with open(file_path, "w") as f:
            assert not f.closed
            TextfileWriter._close_file_handle(file_handle=f)
            assert f.closed
    #-------------------------------------------

    #-----unittests for the happy-path----------
    @staticmethod
    @pytest.mark.parametrize(
        "text_to_write",
        [
            ("SomeString"),
            (""),
        ],
    )
    def test_process_textfile_valid_inputs(mocker, tmp_path, text_to_write: str):
        file_path = tmp_path / filename

        #This patching is done resp. belongs to checking for a closed file-handle
        # - Option B below in this function at hand
        mock_file_handle_close = mocker.patch.object(TextfileWriter, "_close_file_handle", wraps=TextfileWriter._close_file_handle)

        TextfileWriter.process_textfile(
            text_to_write=text_to_write, file_path=file_path
        )

        #checking if the generated file actually exists in the desired location
        #checking for the full path
        assert os.path.exists(path=file_path)

        #checking if the .txt-file actually exists in the specified directory
        assert filename.split(".")[1] == "txt" and \
            filename in os.listdir(tmp_path)
        
        #checking if the specified text was actually written to the .txt-file
        with open(file_path, "r") as f:
            file_content = f.read()
            assert file_content == text_to_write
        
        #checking if the file-handle is closed
        #Option A:
        #Trying to re-open the file in write-mode would lead to an exception
        #if the file-handle was originally opened in write-mode and not closed
        #yet again (at least on Windows). If re-opening that file in write-mode
        #does work here, and if this test is ran on a Windows-operated machine,
        #it can be inferred that the file-handle has been closed previously
        #inside ('TextfileWriter.process_textfile').
        try:
            with open(file_path, "w") as f:
                pass
        except Exception as e:
            pytest.fail(f"The file-handle was not closed properly: {e}")
        
        #Option B:
        #It is checked, whether the helper-function for closing the file-handle
        #("TextfileWriter._close_file_handle") was actually called.
        #This is done by mocking this exact function with itself, so actually,
        #the function is still called normally witout any changed behavior,
        #but it´s call(s) are recorded.
        #Note!: It is important to note that checking the call of
        #       "TextfileWriter._close_file_handle" is of course only a proxy
        #       for checking for a closed file handle. It could be that
        #       "TextfileWriter._close_file_handle" itself is buggy,
        #       i.e. fails silently, but actually does not close the open
        #       file-handle.
        #       So this option B of course is only valid if the helper-function
        #       (i.e. "TextfileWriter._close_file_handle") itself is tested
        #       successfully by one (or more) unittests.

        mock_file_handle_close.assert_called_once()


    #-------------------------------------------



    #-----unittests for the unhappy-paths-------
    @staticmethod
    def test_process_textfile_file_cannot_be_created(mocker, tmp_path):
        #mocking the builtin-function "open" to fail,
        #i.e. not creating the file but raise an exception
        mocker.patch("builtins.open", side_effect=OSError("cannot create file"))

        file_path = tmp_path / "testfile.txt"

        #checking if on the level of "TextfileWriter.process_textfile" the expected
        #custom, domain-specific error occurs
        with pytest.raises(FileCreationError):
            TextfileWriter.process_textfile(text_to_write="Some text", file_path=file_path)


    #-------------------------------------------