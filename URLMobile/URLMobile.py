# URLMobile - Python 2.7 - Johnathon Kwisses (Kwistech)
"""This script is used to check URL's if they are compatible with
smartphones or tablets. It does so by checking for 'viewport' in the
head metadata HTML return of the URL.

A boolean value is returned from the search and is then written to
a .csv file using specified settings defined in main()."""
from BeautifulSoup import BeautifulSoup
import csv
from multiprocessing.pool import ThreadPool
import requests


def get_urls(filename, parsed=True):
    """Get URL's from filename.

    Args:
        filename (str): Name of file to get URL's from.
        parsed (bool): If urls should be parsed.

    Returns:
        list: Contains URL's as strings.
    """
    with open(filename) as urls:
        urls = urls.readlines()
    if parsed:
        parsed_urls = parse_urls(urls)
        return parsed_urls
    else:
        return urls


def parse_urls(urls, separator=";"):
    """Parse urls by splitting them using separator.

    Args:
        urls (list): Contains urls to be parsed.
        separator (str): Symbol to use to split urls.

    Returns:
        list: parsed urls.
    """
    parsed_urls = []
    urls = [url.split(separator) for url in urls]
    for url in urls:
        parsed_urls.append(url[0])
    return parsed_urls


def fetch_urls(url, tag="meta", check=b"viewport", count=[0]):
    """Fetch url and return results in a tuple.

    Args:
        url (str): URL to be fetched.
        tag (str): Tag to be searched in HTML.
        check (str): To be searched in tag.
        count (list): Used to output url count to console.

    Returns:
        tuple: [0] = url; [1] = string ('Exist' or 'Don't Exist').

    Raises:
        ValueError: If url not a valid url.
        urllib.error.HTTPError: If url not found.
    """
    viewport = False
    try:
        response = requests.get(url)
    except:
        return url, "Don't exist"
    else:
        results = response.content
        soup = BeautifulSoup(results).findAll(tag)
        for result in soup:
            if check in str(result):
                viewport = True
    finally:
        count[0] += 1
        print count[0], "URL's checked"
        return url, viewport


def get_output(results):
    """Get output from results.

    Args:
        results (generator): Holds results from URL.

    Returns:
        list: Contains output from results.
    """
    output = []
    for url, exists in results:
        output.append([url, exists])
    output.sort()
    return output


def write_lines_csv(filename, rows, header=None):
    """Write rows to filename (to a .csv file only).

    header should contain strings with header names for
    each column.

    Args:
        filename (str): Name of file to be written to (postfix=.csv).
        rows (list): Contains items to be written to filename.
        header (list): Header to be written to filename.
    """
    with open(filename, "wb") as f:
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
    # Program variables
    filename_in = "Domain_names.csv"
    filename_out = "Parsed-{}".format(filename_in)
    header = ["URL's", "Responsive for Smartphones / Tablets (viewport)"]

    # Number of threads and chunksize to use. Careful of overload!!!
    threads = 650
    chunksize = 25

    # Get URL's and the fetch results
    urls = get_urls(filename_in)
    thread = ThreadPool(threads)
    results = thread.imap_unordered(fetch_urls, urls[1:], chunksize=chunksize)

    # Appends results to output for writing
    output = get_output(results)

    # Writes output to filename_out; header is optional
    write_lines_csv(filename_out, output, header=header)

if __name__ == "__main__":
    main()
