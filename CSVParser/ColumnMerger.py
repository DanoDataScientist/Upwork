# ColumnMerger - Python 3.5 - Johnathon Kwisses (Kwistech)
import csv


class ColumnMerger:
    """Class for ColumnMerger."""

    def __init__(self):
        """Initialize class variables."""
        # Formats column titles
        self.spacer = ""
        self.header = "/"

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

    def merge_two_cols(self, rows, left_col, right_col, title=None):
        """Merge two columns in rows using left_col and right_col.

        Args:
            rows (list): Rows to be used to merge columns.
            left_col (int): Left column number to merge.
            right_col (int): Right column number to merger.
            title (None; str): Optional custom column title.

        Returns:
            rows (list): Contains rows with merged columns.
        """
        left_col, right_col = self.zero_base_shift(left_col, right_col)
        for i, row in enumerate(rows):
            # No custom title
            if i == 0 and not title:
                cell = row[left_col] + self.header + row[right_col]
            # Custom title
            elif i == 0 and title:
                cell = title
            # i != 0
            else:
                cell = row[left_col] + self.spacer + row[right_col]
            # Sets left_col to merged cell
            row[left_col] = cell
            # Deletes right_col
            row.pop(right_col)
        return rows

    def merge_range(self, rows, left_col, right_col, title=None):
        """Merge columns from left_col to right_col.

        Uses self.merge_two_cols() (right_col - left_col) times.

        Args:
            rows (list): Rows to be used to merge columns.
            left_col (int): Left column number to merge.
            right_col (int): Right column number to merger.
            title (None; str): Optional custom column title.

        Returns:
            rows (list): Contains rows with merged columns."""
        cols = right_col - left_col
        for i in range(cols):
            rows = self.merge_two_cols(rows, left_col, left_col+1,
                                       title=title)
        return rows


def main():
    """Create ColumnMerger object and call its various methods."""
    # Filename string variables
    csv_filename_in = "data.csv"
    csv_filename_out = "data2.csv"

    # Create ColumnMerger and set its variables
    csv_merger = ColumnMerger()
    csv_merger.spacer = "/"

    # Use ColumnMerger's methods
    rows = csv_merger.get_csv_rows(csv_filename_in)
    new_rows = csv_merger.merge_two_cols(rows, 2, 3)
    # new_rows = csv_merger.merge_range(rows, 3, 5)
    csv_merger.set_csv_rows(csv_filename_out, new_rows)

if __name__ == "__main__":
    main()
