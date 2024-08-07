from utils.utils import read_yaml,yaml_dot,url_to_imagebit,imagebit_to_string
import newspaper
from rich import pretty, box
from rich.table import Table, Column
from rich.console import Console
from rich.progress import Progress, BarColumn, TextColumn
import re
import argparse

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
progress = Progress(text_column, bar_column, transient=True, expand=True, auto_refresh=False)

configs = read_yaml("configs/configs.yaml")
url_list = yaml_dot(configs,"news.urls")

description = """
Simple news aggregator right in your terminal !
"""
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--url", "-u", help="additional news url")
    parser.add_argument("--block_list","-b", help="list of keywords to exclude")
    parser.add_argument("--numb_news","-n", help="number of news per url")
    parser.add_argument("--image","-im",action='store_true', help="Set this flag to show image")
    parser.add_argument("--memoize","-me", help="Set to False for unduplicated news")
    args = parser.parse_args()
    number_of_news = int(args.numb_news) if args.numb_news \
        else yaml_dot(configs,"number_of_news")
    memoize_articles =  args.memoize if args.memoize \
        else yaml_dot(configs,"memoize_articles")
    if args.url:
        url_list.append(args.url)
    with progress:
        task_ = progress.add_task("[red]Getting news...[/red]",
                        total=len(url_list)*number_of_news)
        for url in url_list:
            news_paper = newspaper.build(url,
                        memoize_articles=memoize_articles)
            block_list = yaml_dot(configs,"news.block_list")
            if args.block_list:
                block_list.append(args.block_list)
            for article in news_paper.articles:
                for block_item in block_list:
                    if re.search(block_item,article.url) :
                        try:
                            news_paper.articles.remove(article)
                        except ValueError:
                            pass
                    else:
                        continue
            for article in news_paper.articles[0:number_of_news]:
                try:
                    article.download()
                    article.parse()
                except Exception as e:
                    continue
                use_images = args.image if args.image \
                    else yaml_dot(configs,"use_images")
                if use_images:
                    try:
                        image = url_to_imagebit(article.top_image)
                        added_text = f"""{article.publish_date}\n
                        [green bold]{article.title}\n[/green bold]\n{imagebit_to_string(image,100)}\n
                        [blue]{article.url}[/blue] \n\n"""
                        progress.update(task_,description=f"""[blue]{url}[/blue]\n{article.title}\n\n{imagebit_to_string(image,70)}""",advance=1)
                        progress.refresh()
                    except:
                        added_text = f"""{article.publish_date}\n
                        [green bold]{article.title}[/green bold]\n 
                        [blue]{article.url}[/blue]\n\n"""
                        progress.update(task_,description=f"""[blue]{url}[/blue]\n {article.title}""", advance=1)
                        progress.refresh()
                else:
                    added_text = f"""{article.publish_date}\n 
                    [green bold]{article.title}[/green bold]\n
                    [blue]{article.url}[/blue]\n\n """
                    progress.update(task_,description=f"""[blue]{url}[/blue]\n
                                {article.title}""", advance=1)
                    progress.refresh()
                table.add_row(added_text + article.text)
    console.print(table)
