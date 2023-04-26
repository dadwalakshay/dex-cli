import typer
from dotenv import load_dotenv

from .client import MangaDexClient

app = typer.Typer()


@app.command()
def search(title: str):
    client_obj = MangaDexClient()

    return client_obj.search(title)


@app.command()
def list_chapters(manga: str):
    client_obj = MangaDexClient()

    return client_obj.list_chapters(manga)


@app.command()
def download(chapter: str):
    client_obj = MangaDexClient()

    return client_obj.download_chapter(chapter)


if __name__ == "__main__":
    load_dotenv()

    app()
