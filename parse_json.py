import collections
import json
from datetime import datetime

import xlsxwriter  # type: ignore


def get_headers(json_file: dict) -> tuple:
    """
    Returns parsed headers and
    columns dictionary where key is 'X' field
    and value is actual column in table
    """
    headers_row = []
    columns = {}

    # collecting all headers into one list
    for entry in json_file["headers"]:
        headers_row.append(
            {
                "X": entry["properties"]["X"],
                "header_text": entry["properties"]["QuickInfo"],
            }
        )
    # sorting list in order to place headers correctly in table
    headers_row.sort(key=lambda x: int(x["X"]))

    # creating dict for filling right fields with values
    col = 0
    for header in headers_row:
        columns[header["X"]] = col
        col += 1

    return (headers_row, columns)


def get_table_rows(json_file: dict) -> dict:
    """
    Return ordered dictionarty where key is a row
    and value is list of values
    """
    values_dict = {}
    for entry in json_file["values"]:
        value = {
            "X": entry["properties"]["X"],
            "Y": entry["properties"]["Y"],
            "value_text": entry["properties"]["Text"],
        }
        if entry["properties"]["Y"] not in values_dict:
            values_dict[entry["properties"]["Y"]] = [value]
        else:
            values_dict[entry["properties"]["Y"]].append(value)

    # sort dictionary so rows will appear in order
    return collections.OrderedDict(sorted(values_dict.items()))


def write_headers(
    worksheet: xlsxwriter.worksheet.Worksheet, headers_row: list, formatting: dict
) -> None:
    """
    fills headers in table
    """
    col = 0
    row = 0

    for header in headers_row:
        worksheet.write(row, col, header["header_text"], formatting)
        col += 1


def write_values(
    worksheet: xlsxwriter.worksheet.Worksheet, columns: dict, table_rows: dict
) -> None:
    """
    fills values in table
    """
    row = 1

    for table_row in table_rows.values():
        for element in table_row:
            worksheet.write(row, columns[element["X"]], element["value_text"])
        row += 1


def main() -> None:
    test_files = ["test1", "test2", "test3"]

    workbook = xlsxwriter.Workbook("results.xlsx")
    bold = workbook.add_format({"bold": 1, "align": "center"})

    for file_name in test_files:
        workbook.add_worksheet(file_name)

    for worksheet in workbook.worksheets():
        worksheet.set_column(0, 3, 25)

        # worksheets are named after file names
        json_file = json.load(open(f"./json_files/{worksheet.name}.json"))

        headers_row, columns = get_headers(json_file)
        table_rows = get_table_rows(json_file)
        write_headers(worksheet, headers_row, bold)
        write_values(worksheet, columns, table_rows)

    workbook.close()


if __name__ == "__main__":
    main()
