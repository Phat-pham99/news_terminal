# Simple news aggregator in Python

Sample `config.yml` file
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


![GIF](./asset/screen_recording.gif)
