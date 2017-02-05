# URLVerifier - Python 3.5 - Johnathon Kwisses (Kwistech)
import csv
from multiprocessing.pool import ThreadPool
from urllib.request import urlopen


def get_urls(filename):
    """Get URL's from filename.

    Args:
        filename (str): Name of file to get URL's from.

    Returns:
        list: Contains URL's as strings.
    """
    with open(filename) as urls:
        urls = urls.readlines()
    return urls


def fetch_url(url, count=[0]):
    """Fetch url and return results in a tuple.

    Args:
        url (str): URL to be fetched.

    Returns:
        tuple: [0] = url; [1] = string ('Exist' or 'Don't Exist').

    Raises:
        ValueError: If url not a valid url.
        urllib.error.HTTPError: If url not found.
    """
    exist = ""

    try:
        urlopen(url)
    except:
        exist = "Don't Exist"
    else:
        exist = "Exist"
    finally:
        count[0] += 1
        print(count[0], "URL's tested")
        return url, exist


def write_lines_csv(filename, rows, header=None):
    """Write rows to filename (to a .csv file only).

    header should contain strings with header names for
    each column.

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
    """Attempt to fetch URL's and write results to a .csv file.

    Note: A memory error might occur if the number of threads is too high.
    If this occurs, set the threads variable to a smaller integer.
    """
    # String variables
    filename_in = "Links-Sheet.csv"
    filename_out = "Parsed-{}".format(filename_in)

    # Number of threads and chunksize to use. Careful of overload!!!
    threads = 650
    chunksize = 25

    # Get URL's and the fetch results
    urls = get_urls(filename_in)
    thread = ThreadPool(threads)
    results = thread.imap_unordered(fetch_url, urls[1:], chunksize=chunksize)

    # Appends results to output for writing
    output = []
    for url, exists in results:
        output.append([url, exists])
    output.sort()

    # Writes output to filename_out; header is optional
    header = ["HTML-Address", "Exist / Don't Exist"]
    write_lines_csv(filename_out, output, header=header)

if __name__ == "__main__":
    main()
