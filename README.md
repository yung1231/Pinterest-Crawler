# Pinterest Crawler for Image Downloads
This is a python crawler designed to download images from `Pinterest`. You can specify a search `query` or `username`, and the script will download all available images.

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
python main.py -t <ttype> -s <search>
```

### Using argument
```bash
usage: main.py [-h] -t TTYPE -s SEARCH

optional arguments:
  -h, --help            show this help message and exit
  -t TTYPE, --type TTYPE
                        Search by 'pin' or 'name_created' or 'name_saved'(name is a string starting after @)
  -s SEARCH, --search SEARCH
                        Keyword you want to query
```

## Example
```bash
python main.py -t pin -s "Bocchi The Rock"
```

## Notes
- The script currently supports downloading `.jpg`、`.png` and `.gif` images.
- The script uses multithreading to speed up image downloading..