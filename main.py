from utils.utils import read_yaml,yaml_dot,url_to_imagebit,imagebit_to_string
import newspaper
from rich import pretty, box
from rich.table import Table, Column
from rich.console import Console
from rich.progress import Progress, BarColumn, TextColumn

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
with progress:
    task_ = progress.add_task("[red]Getting news...[/red]",total=len(url_list)*yaml_dot(configs,"number_of_news"))
    for url in url_list:
        news_paper = newspaper.build(url,memoize_articles=yaml_dot(configs,"memoize_articles"))
        for article in news_paper.articles[0:yaml_dot(configs,"number_of_news")]: #! Add Skipped list of Urls
            try:
                article.download()
                article.parse()
            except Exception as e:
                continue
            if yaml_dot(configs,"use_images"):
                try:
                    image = url_to_imagebit(article.top_image)
                    added_text = f"{article.publish_date} \n [green bold]{article.title}[/green bold] \n [blue]{article.url}[/blue] \n{imagebit_to_string(image,100)} \n \n"
                    progress.update(task_,description=f"[blue]{url}[/blue] \n {article.title} \n\n{imagebit_to_string(image,70)}", advance=1)
                    progress.refresh()
                except:
                    added_text = f"{article.publish_date} \n [green bold]{article.title}[/green bold] \n [blue]{article.url}[/blue] \n \n "
                    progress.update(task_,description=f"[blue]{url}[/blue] \n {article.title}", advance=1)
                    progress.refresh()
            else: 
                added_text = f"{article.publish_date} \n [green bold]{article.title}[/green bold] \n [blue]{article.url}[/blue] \n \n "
                progress.update(task_,description=f"[blue]{url}[/blue] \n {article.title}", advance=1)
                progress.refresh()
            table.add_row(added_text + article.text)
console.print(table)