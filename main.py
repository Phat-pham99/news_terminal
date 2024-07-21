from utils.utils import read_yaml,yaml_dot,url_to_imagebit,imagebit_to_string
import newspaper
import nltk
# nltk.download('punkt')
from rich import print, pretty
from rich.table import Table
from rich.console import Console
from rich import box
from rich.progress import track,Progress, BarColumn, TextColumn
from rich.table import Column
from PIL import Image
import requests

pretty.install()
console = Console()

table = Table(
box=box.DOUBLE,
show_lines=True
)
table.add_column(header='News',
                justify="justified", style="white")
console = Console()
text_column = TextColumn("{task.description}", table_column=Column(ratio=1))
bar_column = BarColumn(bar_width=None, table_column=Column(ratio=2))
progress = Progress(text_column, bar_column, expand=True)

configs = read_yaml("configs/configs.yaml")
url_list = yaml_dot(configs,"news.urls")
with progress:
    task_ = progress.add_task("[red]Getting news...[/red]",total=len(url_list)*yaml_dot(configs,"number_of_news"))
    for url in url_list:
        news_paper = newspaper.build(url,memoize_articles=False)
        for article in news_paper.articles[0:yaml_dot(configs,"number_of_news")]:
            article.download()
            article.parse()
            if yaml_dot(configs,"use_images"):
                image = url_to_imagebit(article.top_image)
                try:
                    added_text = f"[magneta]{article.publish_date}[/magneta] \n [green]{article.title}[/green] \n [blue]{article.url}[/blue] \n {imagebit_to_string(image,150)} \n"
                    progress.update(task_,description=f"{url} \n {article.title}",advance=1)
                except:
                    added_text = f"[magneta]{article.publish_date}[/magneta] \n [green]{article.title}[/green] \n [blue]{article.url}[/blue] \n "
                    progress.update(task_,description=f"{url} \n {article.title}",advance=1)
            else: 
                added_text = f"[magneta]{article.publish_date}[/magneta] \n [green]{article.title}[/green] \n [blue]{article.url}[/blue] \n "
                progress.update(task_,description=f"{url} \n {article.title}",advance=1)
            table.add_row(added_text + article.text)
    console.print(table)