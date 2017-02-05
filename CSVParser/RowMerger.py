# RowMerger - Python 3.5 - Johnathon Kwisses (Kwistech)
import csv
from itertools import zip_longest


class RowMerger:
    """Class for RowMerger."""

    def __init__(self):
        """Initialize class variables."""
        # Formats row data
        self.spacer = "/"

    @staticmethod
    def get_csv_rows(csv_filename):
        """Get rows from csv_filename.

        Args:
            csv_filename (str): Name of csv file to be opened.

        Returns:
            list: Contains rows from csv_filename.
        """
        with open(csv_filename) as csv_f:
            rows = list(csv.reader(csv_f))
        return rows

    @staticmethod
    def set_csv_rows(csv_filename, rows):
        """Set rows to csv_filename.

        Args:
            csv_filename (str): Name of csv file to write to.
            rows (list): Rows to be written to csv_filename.
        """
        with open(csv_filename, "w", newline='') as csv_f:
            writer = csv.writer(csv_f)
            writer.writerows(rows)
        output = "Successfully set rows to '{}'!"
        print(output.format(csv_filename))

    @staticmethod
    def zero_base_shift(*args):
        """Shift args to zero-based numbering.

        Args:
            *args (tuple): Arguments to be shifted.

        Returns:
            list: Shifted arguments.
        """
        return [arg - 1 for arg in args]

    def merge_two_rows(self, rows, up_row, down_row):
        """Merge two rows using up_row and down_row.

        Args:
            rows (list): Rows to be used to merge columns.
            up_row (int): First row to be merged to.
            down_row (int): Last row to be merged.

        Returns:
            rows (list): Contains rows with merged rows.
        """
        up_row, down_row = self.zero_base_shift(up_row, down_row)
        merged_row = []
        for row in zip_longest(rows[up_row], rows[down_row]):
            merged_row.append(self.spacer.join(row))
        # Replaces up_row with the merged row
        rows[up_row] = merged_row
        # Deletes the down_row
        rows.pop(down_row)
        return rows

    def merge_range(self, rows, up_row, down_row):
        """Merge rows from up_row to down_row.

        Uses self.merge_two_rows() (down_row - up_row) times.

        Args:
            rows (list): Rows to be used to merge columns.
            up_row (int): First row to be merged to.
            down_row (int): Last row to be merged.

        Returns:
            rows (list): Contains rows with merged rows.
        """
        num_rows = down_row - up_row
        for i in range(num_rows):
            rows = self.merge_two_rows(rows, up_row, up_row+1)
        return rows


def main():
    """Create RowMerger object and call its various methods."""
    # Filename string variables
    csv_filename_in = "data.csv"
    csv_filename_out = "data3.csv"

    # Create RowMerger and set its variables
    csv_merger = RowMerger()
    csv_merger.spacer = "/"

    # Use RowMerger's methods
    rows = csv_merger.get_csv_rows(csv_filename_in)
    new_rows = csv_merger.merge_two_rows(rows, 3, 4)
    # new_rows = csv_merger.merge_range(rows, 3, 5)
    csv_merger.set_csv_rows(csv_filename_out, new_rows)

if __name__ == "__main__":
    main()
