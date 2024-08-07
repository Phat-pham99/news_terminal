# Simple news aggregator in Python

Sample `configs/configs.yml` file
```
news:
  urls:
    - https://www.coindesk.com/
  block_list : 
    - "#"
    - "comment"
number_of_news: 10
use_images: True
memoize_articles: False
```
Parameters:
- `news.urls`: List of urls from which you want to get news from
- `block_list`: List of keywords that you want to exclude in your news search
- `number_of_news`: Number of news per url
- `memoirize_articles`: Set to `True` if you want the news not to get duplicated each script run.  

On the other hand, you can also pass in CLI argument to overwrite initial config : 
```
(news_venv) news_terminal> python .\main.py -h
usage: main.py [-h] [--url URL] [--block_list BLOCK_LIST] [--numb_news NUMB_NEWS] [--image] [--memoize MEMOIZE]

Simple news aggregator right in your terminal !

options:
  -h, --help            show this help message and exit
  --url URL, -u URL     additional news url
  --block_list BLOCK_LIST, -b BLOCK_LIST
                        list of keywords to exclude
  --numb_news NUMB_NEWS, -n NUMB_NEWS
                        number of news per url
  --image, -im          Set this flag to show image
  --memoize MEMOIZE, -me MEMOIZE
                        Set to False for unduplicated 
  ```

## Usage:
```
python main.py --image -u "https://theinvestor.vn"
```
<img src="./asset/screen_recording.gif"/>