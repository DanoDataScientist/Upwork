# CSVParser - Johnathon Kwisses (Kwistech)
"""CSVParser finds all of the .csv files in a directory. It then reads each
file and gets the rows from that file. After this, it then parses all of the
rows to find specific information (cell data) and returns all instances of the
found data. Once this is done, the data, which will contain all the hits from
all of the found .csv files in a directory, is then written to one .csv file
thereby merging all of the found data in all of the found .csv files into
one .csv file.
"""
import csv
import os


def get_filenames(exclude, directory=".", file_extension=".csv"):
    """Get filenames with file_extension from directory - exclude.

    Args:
        exclude (str): Filename to exclude.
        directory (str): Directory to search.
        file_extension (str): File extension to search for.

    Returns:
        list: Contains filenames from directory.
    """
    filenames = []

    for file in os.listdir(directory):
        if file != exclude and file_extension in file:
            filenames.append(file)

    return filenames


def get_lines(filenames):
    """Get lines from filename.

    Args:
        filenames (list): Names of file to get lines from.

    Returns:
        list: Contains lines from filename.
    """
    lines = []

    for filename in filenames:
        with open(filename) as f:
            f = f.readlines()
        lines.append(f)

    return lines


def row_column_selector(sheets, item_to_find, rows=False, columns=False):
    """Switch between different parser functions for rows or columns.

   Args:
        sheets (list): Contains sheets to be parsed.
        item_to_find (str): Item to find in sheets.
        rows (bool): If True, sheets are parsed by rows.
        columns (bool): If True, sheets are parsed by columns.

    Returns:
        list: Contains parsed sheets.
    """
    parsed_sheets = []

    if rows:
        for sheet in sheets:
            parsed_sheet = parse_sheet_columns(sheet, item_to_find)
            parsed_sheets.append(parsed_sheet)
    elif columns:
        for sheet in sheets:
            parsed_sheet = parse_sheet_rows(sheet, item_to_find)
            parsed_sheets.append(parsed_sheet)

    return parsed_sheets


def parse_sheet_rows(sheet, item_to_find, separator=","):
    """Parse sheet rows to find an item.

    Args:
        sheet (list): Contains rows from a spreadsheet.
        item_to_find (str): Item to find in sheet.
        separator (str): Split row by this symbol.

    Returns:
        list: Contains all item_to_find rows in sheet.
    """
    found_items = []

    for row in sheet:
        # Solves for different column separators
        separator = separator if separator in row else ";"
        row = row.split(separator)
        row = [cell.strip("\n").lower() for cell in row]

        if item_to_find.lower() in row:
            for cell in row:
                found_items.append(cell)

    return found_items


def parse_sheet_columns(sheet, item_to_find, separator=","):
    """Parse sheet columns to find an item.

    Args:
        sheet (list): Contains rows from a spreadsheet.
        item_to_find (str): Item to find in sheet.
        separator (str): Split row by this symbol.

    Returns:
        list: Contains all item_to_find rows in sheet."""
    found_items = []
    index = 0

    for row in sheet:
        # Solves for different column separators
        separator = separator if separator in row else ";"
        row = row.split(separator)
        row = [cell.strip("\n").lower() for cell in row]

        if not index and item_to_find.lower() in row:
            index = row.index(item_to_find)

        found_items.append(row[index])

    return found_items[1:]


def get_unique_cells(parsed_sheets):
    """Get unique entries from parsed_sheets.

    Args:
        parsed_sheets (list): Parsed sheets to be searched.

     Returns:
         list: Unique entries in all of the parsed_sheets.
        """
    unique_cells = []

    for i in range(1, len(parsed_sheets)):
        comped_sheets = compare_sheets(parsed_sheets[0], parsed_sheets[i])
        for item in comped_sheets:
            unique_cells.append(item)

    return unique_cells


def compare_sheets(sheet1, sheet2):
    """Compare two sheets and return items not in both sheets.

    Args:
        sheet1 (list): Contains rows from spreadsheet1.
        sheet2 (list): Contains rows from spreadsheet2.

    Returns:
        list: Contains items not in both sheets.
    """
    unique_cells = []
    sheet1, sheet2 = set(sheet1), set(sheet2)

    for row in sheet1:
        if row not in unique_cells and row not in sheet2:
            unique_cells.append(row)

    for row in sheet2:
        if row not in unique_cells and row not in sheet1:
            unique_cells.append(row)

    return unique_cells


def write_lines(filename, rows, header=None):
    """Write rows to filename (to a .csv file only).

    Args:
        filename (str): Name of file to be written to (postfix=.csv).
        rows (list): Contains items to be written to filename.
        header (list): Header to be written to filename.
    """
    with open(filename, "w", newline='') as f:
        writer = csv.writer(f)
        if header:
            writer.writerow(header)
        writer.writerows(rows)

    print("Successfully written rows to '{}'!".format(filename))


def main():
    """Run multiple functions to get, parse, and write .csv data."""
    # String variables (set the output filename and search item below)
    output_filename = "parsed_csv_files.csv"
    item_to_find = "t"

    # Get dirty data
    filenames = get_filenames(output_filename)
    sheets = get_lines(filenames)

    # Clean data from either rows or columns (set rows or columns to True)
    parsed_sheets = row_column_selector(sheets, item_to_find, columns=True)

    # Get unique output for output file
    unique_cells = get_unique_cells(parsed_sheets)

    # Puts data in natural order and adds item_to_find to first column
    output = sorted(set(unique_cells))
    output = [[item_to_find, x] for x in output]

    # Write output to output_filename
    write_lines(output_filename, output)

if __name__ == "__main__":
    main()
