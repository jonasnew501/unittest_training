import argparse

from unittest_training.projects.textfile_writer.textfile_writer import TextfileWriter


def main():
    # Setup the argument parser
    parser = argparse.ArgumentParser(
        description="Simple CLI tool to create text files with rollback on error."
    )

    # Define command-line arguments
    parser.add_argument(
        "--text",
        required=True,
        help="The text content to write into the file"
    )
    parser.add_argument(
        "--filename",
        required=True,
        help="Name of the text file to create (e.g. output.txt)"
    )
    
    args = parser.parse_args()

    # Calling the class
    TextfileWriter.process_textfile(
        text_to_write=args.text,
        file_path=args.filename
    )

    # (optionally): Printing the output of the method-call
    # print(f"✅ File processed successfully: {result}")

if __name__ == '__main__':
    main()