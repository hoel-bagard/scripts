from pathlib import Path
from typing import ClassVar, Iterator, Literal, NewType
from dataclasses import dataclass
import csv

Password = NewType("Password", str)


@dataclass(frozen=True, slots=True)
class CSV_Row:
    account: str
    login_name: str
    password: Password
    website: str
    comments: str

    def __str__(self) -> str:
        data = f"{self.password}\n"

        if self.login_name:
            data += f"username: {self.login_name}\n"

        if self.account:
            data += f"account: {self.account}\n"

        if self.website:
            data += f"website: {self.website}\n"

        if self.comments:
            data += f"notes: {self.comments}\n"

        return data


class CSVFile:
    """Keepass2 CSV file.

    Args:
        csv_path: Keepass2 can export data as a csv where each line has the following format:
                  Account,Login Name,Password,Web Site,Comments
    """

    def __init__(self, csv_path: Path) -> None:
        self.rows: list[CSV_Row] = []
        with csv_path.open(encoding="utf-8") as csv_file:
            for i, row in enumerate(csv.reader(csv_file, dialect="excel")):
                # skip first line (header)
                if i == 0:
                    continue
                # skip sample entry
                if i == 1 and row[0] == "Sample Entry":
                    continue

                self.rows.append(CSV_Row(
                    account=row[0],
                    login_name=row[1],
                    password=Password(row[2]),
                    website=row[3],
                    comments=row[4],
                ))

    def __len__(self) -> int:
        return len(self.rows)

    def __iter__(self) -> Iterator[CSV_Row]:
        yield from self.rows

    def __getitem__(self, item: int) -> CSV_Row:
        return self.rows[item]

