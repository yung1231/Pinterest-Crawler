# Pinterest Crawler for Image Downloads
This is a python crawler designed to download images from `Pinterest`. The script uses the Selenium webdriver to automate scrolling through the Pinterest search results and retrieves the original image URLs. 

The images are then downloaded using thread pool to enable faster downloads.

The following formats are available for download：`jpg`、`png`、`gif`

## Installation
1. Clone the repository & Install the required dependencies

```bash
git clone https://github.com/yung1231/Pinterest-Crawler.git

pip install -r requirements.txt
```

2. chromedriver
   - Download the appropriate ChromeDriver for your system from the [official website](https://chromedriver.chromium.org/downloads)

## Usage
1. Modify the configuration file `config.cfg` to specify the download path for the images.

2. Run the script `main.py` with the following command

```bash
python main.py -q <query> -s <scroll>
```

### Using argument
```bash
usage: main.py [-h] -q QUERY -s SCROLL

optional arguments:
  -h, --help            show this help message and exit
  -q QUERY, --query QUERY
                        Keyword you want to query
  -s SCROLL, --scroll-times SCROLL
                        Number of page scrolls
```

## Example
```bash
python main.py -q "cute animals" -s 5
```