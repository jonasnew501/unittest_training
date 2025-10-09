import os
from io import TextIOWrapper
import pytest

from unittest_training.projects.textfile_writer.textfile_writer import (
    TextfileWriter,
    FileCreationError,
    FileDeletionError,
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

    # -----unittests for helper-functions--------
    @staticmethod
    def test_close_file_handle(tmp_path):
        file_path = tmp_path / "Testfile.txt"

        with open(file_path, "w") as f:
            assert not f.closed
            TextfileWriter._close_file_handle(file_handle=f)
            assert f.closed

    # -------------------------------------------

    # -----unittests for the happy-path----------
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

        # This patching is done resp. belongs to checking for a closed file-handle
        # - Option B below in this function at hand
        mock_file_handle_close = mocker.patch.object(
            TextfileWriter,
            "_close_file_handle",
            wraps=TextfileWriter._close_file_handle,
        )

        TextfileWriter.process_textfile(
            text_to_write=text_to_write, file_path=file_path
        )

        # checking if the generated file actually exists in the desired location
        # checking for the full path
        assert os.path.exists(path=file_path)

        # checking if the .txt-file actually exists in the specified directory
        assert filename.split(".")[1] == "txt" and filename in os.listdir(tmp_path)

        # checking if the specified text was actually written to the .txt-file
        with open(file_path, "r") as f:
            file_content = f.read()
            assert file_content == text_to_write

        # checking if the file-handle is closed
        # Option A:
        # Trying to re-open the file in write-mode would lead to an exception
        # if the file-handle was originally opened in write-mode and not closed
        # yet again (at least on Windows). If re-opening that file in write-mode
        # does work here, and if this test is ran on a Windows-operated machine,
        # it can be inferred that the file-handle has been closed previously
        # inside ('TextfileWriter.process_textfile').
        try:
            with open(file_path, "w") as f:
                pass
        except Exception as e:
            pytest.fail(f"The file-handle was not closed properly: {e}")

        # Option B:
        # It is checked, whether the helper-function for closing the file-handle
        # ("TextfileWriter._close_file_handle") was actually called.
        # This is done by mocking this exact function with itself, so actually,
        # the function is still called normally witout any changed behavior,
        # but it´s call(s) are recorded.
        # Note!: It is important to note that checking the call of
        #       "TextfileWriter._close_file_handle" is of course only a proxy
        #       for checking for a closed file handle. It could be that
        #       "TextfileWriter._close_file_handle" itself is buggy,
        #       i.e. fails silently, but actually does not close the open
        #       file-handle.
        #       So this option B of course is only valid if the helper-function
        #       (i.e. "TextfileWriter._close_file_handle") itself is tested
        #       successfully by one (or more) unittests.

        mock_file_handle_close.assert_called_once()

    # -------------------------------------------

    # -----unittests for the unhappy-paths-------
    @staticmethod
    def test_process_textfile_file_cannot_be_created(mocker, tmp_path):
        # mocking the builtin-function "open" to fail,
        # i.e. not creating the file but raise an exception
        mocker.patch("builtins.open", side_effect=OSError("cannot create file"))

        file_path = tmp_path / "testfile.txt"

        # checking if on the level of "TextfileWriter.process_textfile" the expected
        # custom, domain-specific error occurs
        with pytest.raises(FileCreationError):
            TextfileWriter.process_textfile(
                text_to_write="Some text", file_path=file_path
            )

    @staticmethod
    def test_process_textfile_check_rollback_functionality(mocker, tmp_path):
        file_path = tmp_path / "testfile.txt"

        # mocking the "flush"-function of "TextIOWrapper" to fail
        # However, this doesn´t work for technical reasons. This is why an alternative
        # (see below) was necessary.
        # flush_fail = mocker.patch.object(TextIOWrapper, "flush", side_effect=OSError("flush failed"))

        # Alternatively to mocking the "flush"-function of "TextIOWrapper" directly:
        # Creating an own mock-object, setting the return_value of "write" to None,
        # setting the side_effect on "flush", and then passing this whole mock-object
        # as a fake file-handle to "_create_file".
        # Reason: In the main-method "process_textfile" "_create_file" returns a
        #        file-handle, which is then passed on to "_write_to_file".
        #        "_write_to_file" will call "write()" and "flush()" on this file-handle.
        #        If however, now instead of a real file-handle this fake file-handle
        #        with the retrn_value resp. side_effect set for "write" and "flush"
        #        is returned from "_create_file" and thus subsequently passed on to
        #        "_write_to_file", inside "_write_to_file" the call to "file_handle.flush()"
        #        will raise the OSError set here as a side_effect. This OSError will propagate
        #        up to "process_textfile" and this Exception is then expected to trigger
        #        the rollback (i.e. file-deletion) part, which is then checked for here
        #        further below.
        mock_flush = mocker.Mock()
        mock_flush.write.return_value = None
        mock_flush.flush.side_effect = OSError("flush failed")
        mocker.patch.object(TextfileWriter, "_create_file", return_value=mock_flush)

        # because with the mock above "_create_file" will actually never be ran
        # and thus the textfile will actually never be created in the first place,
        # the file is created at this point manually. Only then it is ensured,
        # that the rollback-action itself (i.e. the file-deletion) actually
        # works correctly (see the assert for the non-existing path below
        # after the rollback was conducted).
        file_path.touch()

        # calling the main-function
        # At this point, it is expected that the file is created inside "tmp_path",
        # but no contents are written to it, since the flush is simulated to fail
        with pytest.raises(OSError):
            TextfileWriter.process_textfile(
                text_to_write="Some text", file_path=file_path
            )

        # Checking if the mock-objects were actually called as expected
        mock_flush.write.assert_called_once_with("Some text")
        mock_flush.flush.assert_called_once()

        # checking if the the rollback was actually conducted, i.e. whether the file
        # was actually deleted again.
        assert not os.path.exists(file_path)

    @staticmethod
    def test_process_textfile_file_cannot_be_deleted(mocker, tmp_path):
        file_path = tmp_path / "testfile.txt"

        # mocking "os.remove" to raise a OSError instead of actually deleting
        # the object passed in
        mocker.patch("os.remove", side_effect=OSError("File cannot be deleted"))

        # mocking "_create_file" again (as in "test_process_textfile_check_rollback_functionality")
        # to simulate a failing flush and thereby envoke a rollback-behavior
        mock_flush = mocker.Mock()
        mock_flush.write.return_value = None
        mock_flush.flush.side_effect = OSError("flush failed")
        mocker.patch.object(TextfileWriter, "_create_file", return_value=mock_flush)

        # manually creating the file
        file_path.touch()

        # expecting "process_textfile" to raise resp. to receive the
        # custom exception "FileDeletionError".
        # Note that before this exception, the OSError from the "flush"
        # was raised, however, this FileDeletionError was actually raised
        # after that from inside "_delete_file", which is why this (latest)
        # exception needs be expected here.
        with pytest.raises(FileDeletionError):
            TextfileWriter.process_textfile(
                text_to_write="Some text", file_path=file_path
            )

        # Checking if the mock-objects were actually called as expected
        mock_flush.write.assert_called_once_with("Some text")
        mock_flush.flush.assert_called_once()

        # expecting "process_textfile" to raise resp. to receive the
        # custom Exception
        # with pytest.raises(FileDeletionError):

        # checking if the file still exists at the file_path
        assert os.path.exists(file_path)

    # -------------------------------------------
