from bs4 import BeautifulSoup, Tag
import os
import csv
import sys


class SemiannualEvaluation:

    _fieldnames = ["No", "No Control", "Nombre", "P1", "P2", "P3", "Final"]
    _position_cols = [0, 1, 2, 3, 4, 5, 9]

    def __init__(self, path_file_src: str):
        self.content = None
        self.path_name_file = path_file_src
        self._load_file()

    def convert_save_to_csv(self, path_name_file: None | str = None):

        if not path_name_file:
            import uuid

            path_name_file = f"information_{uuid.uuid4()}.csv"
        if self.content:
            with open(path_name_file, "w+") as csv_file:

                writer = csv.DictWriter(csv_file, fieldnames=self._fieldnames)
                writer.writeheader()
                writer.writerows(self.content)
        else:
            raise Exception("No content exist")

    def _get_content_from_td(self, tag: Tag):
        value = ""
        if tag.get_text():
            value = tag.get_text()
        elif tag.find("input") and tag.find("input").get("value"):
            value = tag.find("input").get("value")

        return value.strip()

    def get_content(self):
        return self.content

    def _extract_data(self, html: BeautifulSoup):
        table = html.find_all("table")[10].find("tbody")
        content = []


        for tr in table.find_all("tr")[2:]:
            row = {}
            td = tr.find_all("td")

            for i in range(len(self._fieldnames)):
                row[self._fieldnames[i]] = self._get_content_from_td(
                    td[self._position_cols[i]]
                )

            content.append(row)
        self.content = content

    def _load_file(self):
        with open(self.path_name_file, "r") as html:
            content = BeautifulSoup(html, "html.parser")
            self._extract_data(content)


class BulkSemiannualEvaluation:
    """docstring for BulkSemiannualEvaluation."""

    _name_files_list: list | None = None

    def __init__(self, path_folder="", name_file=True):
        self.path_folder = path_folder
        self.name_file = name_file
        self._get_paths_from_folder()

    def _get_name_file(self, name: str):
        name_with_ext = name.split(os.path.sep)[-1]
        return name_with_ext.split(".")[0]

    def _get_paths_from_folder(self):
        self._name_files_list = [
            f"{self.path_folder}{os.sep}{i}" for i in os.listdir(self.path_folder)
        ]

    def convert_bulk(self):
        for file_path in self._name_files_list:
            SemiannualEvaluation(file_path).convert_save_to_csv(f"{self._get_name_file(file_path)}.csv") #colocar el nombre del archivo



if __name__ == "__main__":

    files_csv = BulkSemiannualEvaluation(os.path.abspath(sys.argv[1]))
    files_csv.convert_bulk()

