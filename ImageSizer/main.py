# ImageSizer - Johnathon Kwisses (Kwistech)
from io import BytesIO
from os import listdir
from PIL import Image
from requests import get as request


class DataRetriever(object):
    """House local data retrieving methods."""

    def local_data(self, filename, parse=False):
        """Get local data from filename.

        Args:
            filename (str): Name of file to be opened.
            parse (bool): Switch for parsing data.

        Returns:
            list: Contains lines from filename.
        """
        with open(filename) as f:
            f = f.readlines()
        if parse:
            f = self.parse_local_data(f)
        return f

    @staticmethod
    def parse_local_data(data):
        """Parse local data (used in .csv file reading).

        Args:
            data (list): Data to be parsed.

        Returns:
            list: Parsed data.
        """
        parsed_data = []
        for line in data:
            url, width, height = line.split(";")
            image_name = url.split('/')[-1]
            size = int(width), int(height)
            parsed_data.append([url, size, image_name])
        return parsed_data


class ImageRetriever(object):
    """House local and global image retrieving methods."""

    def __init__(self):
        """Initialize class variables."""
        self.image_types = ["png", "jpg"]

    def local_images(self, directory):
        """Get images from a local directory.

        Args:
            directory (str): Directory to search.

        Returns:
            list: Contains images and their filenames.
        """
        images = []
        files = listdir(directory)
        for file in files:
            for image_type in self.image_types:
                if image_type in file:
                    directory = "{}/{}".format(directory, file)
                    image = Image.open(directory)
                    images.append([image, file])
        return images

    def url_image(self, url):
        """Get image from a URL.

        Args:
            url (str): URL to get image from.

        Returns:
            tuple: [0] = image; [1] = image's postfix.
        """
        response = request(url)
        image = Image.open(BytesIO(response.content))
        image_type = self.url_image_type(image)
        return image, image_type

    def url_image_type(self, image):
        """Get image's postfix (type).

        Args:
            image (PIL): Image object.

        Returns:
            str: Image postfix (type).
        """
        image = str(image).lower()
        for image_type in self.image_types:
            if image_type == "jpg":
                if "jpeg" in image:
                    return image_type
            elif image_type in image:
                return image_type


class ImageSizer(object):
    """ImageSizer object."""

    @staticmethod
    def run(image, image_name, image_type, size, save_directory):
        """Resize image to size and save it to save_directory.

        Args:
            image (PIL): Image object.
            image_name (str): Name of image.
            image_type (str): Image postfix (type).
            size (tuple): Size to resize image to.
            save_directory (str): Directory to save image to.
        """
        image_name = image_name.split(".")[0]
        image = image.resize(size, Image.ANTIALIAS)
        directory = "{}/{}.{}".format(save_directory, image_name, image_type)
        image.save(directory)


class Selector(object):
    """Command prompt selector UI."""

    def __init__(self, csv_filename, open_directory, save_directory):
        """Initialize class variables and class objects."""
        self.csv_filename = csv_filename
        self.open_directory = open_directory
        self.save_directory = save_directory

        self.data_retriever = DataRetriever()
        self.image_retriever = ImageRetriever()
        self.image_sizer = ImageSizer()

    @staticmethod
    def interface():
        """Print output to console for user-interaction."""
        options = "\nOptions:\n"
        option1 = "\n1. Resize URL images in a .csv file\n"
        option2 = "2. Resize images on a local drive\n"
        print(options + option1 + option2)

    def option1(self):
        """Resize URL images in a .csv file."""
        data = self.data_retriever.local_data(self.csv_filename, parse=True)
        for line in data:
            url, size, image_name = line
            image, image_type = self.image_retriever.url_image(url)
            self.image_sizer.run(image, image_name, image_type, size,
                                 self.save_directory)

    def option2(self, size):
        """Resize images on a local drive.

        Args:
            size (tuple): Size to resize image(s) to.
        """
        data = self.image_retriever.local_images(self.open_directory)
        for line in data:
            image, image_filename = line
            image_name, image_type = image_filename.split(".")
            self.image_sizer.run(image, image_name, image_type, size,
                                 self.save_directory)

    def run(self, cmd=None):
        """Run command prompt selector."""
        if not cmd:
            self.interface()
            cmd = input("Enter command: ")

        if cmd == "1":
            self.option1()
        elif cmd == "2":
            size = input("Enter width, height: ").split(", ")
            size = tuple([int(x) for x in size])
            self.option2(size)
        else:
            print("\nERROR!!!")

        print("\nSuccessfully resized image(s)!")


def main():
    """Set filename(s) and directories and run command-prompt selector."""
    # Filenames for local files
    csv_filename = input("Enter filename of .csv file: ")

    # Directories to open / save locally
    open_directory = input("Enter name of open directory: ")
    save_directory = input("Enter name of save directory: ")

    # Activates command prompt selector
    selector = Selector(csv_filename, open_directory, save_directory)
    selector.run()

    # To skip the command prompt selector:
    # - comment out the above selector.run()
    # - uncomment a single cmd variable of your choosing
    # - uncomment the below selector.run(cmd=cmd)
    # --------------------------------------------
    # cmd = "1"  # option1() =
    # cmd = "2"  # option2() =
    # selector.run(cmd=cmd)


if __name__ == "__main__":
    main()
