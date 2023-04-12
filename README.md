# Pinterest Crawler for Image Downloads
This is a python crawler designed to download images from `Pinterest`. It can search for and download images from `pin` or `name`. The script uses a headless Selenium driver to simulate a web browser to get the page source and then extract image URLs from the search )

## Installation
1. Clone the repository & Install the required dependencies

```bash
git clone https://github.com/yung1231/Pinterest-Crawler.git

pip install -r requirements.txt
```

2. chromedriver
   - Download the Chrome Driver from [official website](https://chromedriver.chromium.org/downloads). Make sure to download the version that matches your Chrome browser version.

## Usage
1. Modify the configuration file `config.cfg` to specify the download path for the images.

2. Run the script `main.py` with the following command

```bash
python main.py -tt <ttype> -s <search> -t <times>
```

### Using argument
```bash
usage: main.py [-h] -tt TTYPE -s SEARCH -t TIMES

optional arguments:
  -h, --help            show this help message and exit
  -tt TTYPE, --ttype TTYPE
                        Search by 'pin' or 'name'(name is a string starting after @)
  -s SEARCH, --search SEARCH
                        Keyword you want to query
  -t TIMES, --times TIMES
                        Number of page scrolls
```

## Example
```bash
python main.py -tt pin -s "cute animals" -t 5
```

## Notes
- The script currently supports downloading `.jpg`、`.png` and `.gif` images.
- The script uses multithreading to speed up image downloading..