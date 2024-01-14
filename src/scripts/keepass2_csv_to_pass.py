import argparse
import logging
from subprocess import Popen, PIPE
from pathlib import Path

from hbtools import create_logger, yes_no_prompt

from scripts.types.keepass_csv import CSV_Row, CSVFile


def pass_import_entry(path: str, data: str):
    """Import the entry to pass."""
    proc = Popen(["pass", "insert", "--multiline", path], stdin=PIPE, stdout=PIPE)
    proc.communicate(data.encode("utf-8"))
    proc.wait()


def create_file_path(entry: CSV_Row, to_lower: bool) -> str:
    """ escape the list """
    path = entry.account.replace(" ", "-") \
                        .replace("/", "-") \
                        .replace("&", "and") \
                        .replace("[", "") \
                        .replace("]", "")

    if to_lower:
        path = path.lower()

    return path


def process_csv(csv_path: Path, to_lower: bool = False, verification_prompt: bool = False):
    """Insert all the entries to pass"""
    logger = logging.getLogger(__name__)

    logger.info(f"Importing passwords from: {csv_path}")

    csv_content = CSVFile(csv_path)

    if not len(csv_content):
        logger.warning("No entry found in the CSV file.")
        return

    logger.info(f"Found {len(csv_content)} entries.")

    for entry in csv_content:
        logger.info(f"Importing:\n{entry}")
        if not verification_prompt or yes_no_prompt("Proceed ?"):
            path = create_file_path(entry, to_lower)
            pass_import_entry(path, str(entry))


def main():
    parser = argparse.ArgumentParser(
        description="Script to migrate keepass2 csv data to pass.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("csv_path", type=Path, help="The CSV file to read from.")
    parser.add_argument("--to-lower", "-l", action="store_true", help="Convert account name to lowercase.")
    parser.add_argument("--prompt", "-p", action="store_true", help="Prompt before saving each entry.")
    args = parser.parse_args()

    csv_path: Path = args.csv_path
    to_lower: bool = args.to_lower
    verification_prompt: bool = args.prompt

    logger = create_logger(__name__, verbose_level="debug")

    process_csv(csv_path, to_lower, verification_prompt)

    logger.info("Finished")


if __name__ == "__main__":
    main()
