import os
from io import TextIOWrapper


text_to_write = "SomeText"
filename = "someFile.txt"

current_file_path = os.path.abspath(__file__)
current_dir_path = os.path.dirname(current_file_path)
file_path = os.path.realpath(os.path.join(current_dir_path, filename))


# -----Custom, domain-specific exceptions--------
class FileCreationError(Exception):
    """
    A custom domain-specific Exception
    for when a file cannot be created.
    """

    pass

class FileDeletionError(Exception):
    """
    A custom domain-specific Exception
    for when a file cannot be deleted.
    """

    pass


# -----------------------------------------------


# Implementation without context-manager for handling textfiles
class TextfileWriter:
    @staticmethod
    def process_textfile(text_to_write: str, file_path: str):
        file_handle = None
        try:
            # create file in write mode
            file_handle = TextfileWriter._create_file(file_path=file_path, mode="w")

            was_write_succesful = False
            # write to file
            was_write_succesful = TextfileWriter._write_to_file(
                file_handle=file_handle, text_to_write=text_to_write
            )
            print(
                "Writing to file was successful."
                if was_write_succesful
                else "Writing to file was not successful."
            )
        except Exception as e:
            # rollback: if file was already created, delete the file again
            if TextfileWriter._check_for_file_presence(file_path=file_path):
                TextfileWriter._delete_file(file_path=file_path)

            raise e
        finally:
            # cleanup: close the file-handle
            if file_handle is not None:
                if TextfileWriter._check_for_open_file_handle(file_handle=file_handle):
                    was_file_handle_closed = TextfileWriter._close_file_handle(
                        file_handle=file_handle
                    )
                    print(
                        "File_handle was closed."
                        if was_file_handle_closed
                        else "File_handle was not closed."
                    )

    @staticmethod
    def _create_file(file_path: str, mode: str) -> TextIOWrapper:
        try:
            file_handle = open(file=file_path, mode=mode)
        except:
            raise FileCreationError

        return file_handle

    @staticmethod
    def _write_to_file(file_handle: TextIOWrapper, text_to_write: str) -> bool:
        """
        Writes 'text_to_write' to the file passed in as a 'file_handle'.

        Args:
            file_handle (TextIOWrapper): The file-handle in writable-mode where
                                         'text_to_write' shall be written to.
            text_to_write (str): The text that shall be written to the file.

        Returns:
            (bool): True, if the text was successfully written to the file,
                    False otherwise.
        """
        file_handle.write(text_to_write)
        file_handle.flush()

        try:
            os.fsync(file_handle.fileno())
            print("Flushed safely to disk.")
            return True
        except OSError as e:
            print(f"Flush failed. Exception: {e}.")
            return False

    @staticmethod
    def _check_for_file_presence(file_path: str) -> bool:
        """
        Checks if the file specified at the 'file_path' exists.

        Args:
            file_path (str): The absolute file path to check for
                             existance of the file.

        Returns:
            (bool): True, if the file exists at 'file_path',
                    False otherwise.
        """
        if os.path.exists(file_path):
            return True
        else:
            return False

    @staticmethod
    def _delete_file(file_path: str):
        """
        Deletes the file at 'file_path'.

        Args:
            file_path (str): The absolute file path of the file
                             that shall be deleted.
        
        Raises:
            FileDeletionError: If the file could not be deleted.
        """
        try:
            os.remove(path=file_path)
        except:
            raise FileDeletionError


    @staticmethod
    def _check_for_open_file_handle(file_handle: TextIOWrapper) -> bool:
        """
        Checks if the 'file_handle' is open.

        Args:
            file_handle (TextIOWrapper): The file_handle to check.

        Returns:
            (bool): True, if the file_handle is open,
                    False otherwise.
        """
        if not file_handle.closed:
            return True
        else:
            return False

    @staticmethod
    def _close_file_handle(file_handle: TextIOWrapper) -> bool:
        """
        Closes the 'file_handle'.

        Args:
            file_handle (TextIOWrapper): The file_handle to be closed.
                                         The assumption is that file_handle
                                         is opened at the time of calling
                                         this function at hand.

        Returns:
            (bool): True, if the file_handle was closed,
                    False otherwise.
        """
        try:
            file_handle.close()
            return True
        except Exception as e:
            print(f"File handle could not be closed. Exception: {e}.")
            return False


# -----TEST----------
# TextfileWriter.process_textfile(text_to_write=text_to_write, file_path=file_path)
