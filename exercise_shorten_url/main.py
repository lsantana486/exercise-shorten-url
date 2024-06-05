from pathlib import Path
from urllib.parse import quote
from typing import Generator
from time import sleep

import requests
from typing_extensions import Annotated

import typer

app = typer.Typer()
_cached_urls = {}


def get_urls_from_file(file_path: Path) -> Generator:
    for line in file_path.open():
        yield line.strip()


def generate_short_url(url: str) -> str:
    url_encoded = quote(url)
    short_url_generator_service = (
        f"https://is.gd/create.php?format=simple&url={url_encoded}"
    )
    response = requests.get(short_url_generator_service)
    if response.status_code == requests.codes.ok:
        return response.text

    elif response.status_code == requests.codes.bad_gateway:
        sleep(60)
        return generate_short_url(url)

    else:
        raise Exception(f"Error while generating short URL for {url}")


def get_short_url(url: str) -> tuple[bool, str]:
    if url in _cached_urls:
        return True, _cached_urls[url]
    else:
        short_url = generate_short_url(url)
        _cached_urls[url] = short_url
        return False, short_url


@app.command()
def cli(
    urls_file: Annotated[
        Path,
        typer.Option(
            exists=True,
            file_okay=True,
            dir_okay=False,
            writable=False,
            readable=True,
            resolve_path=True,
        ),
    ]
):
    for url in get_urls_from_file(urls_file):
        try:
            from_cached, short_url = get_short_url(url)
            if not from_cached:
                typer.echo(f"{short_url}, {url}")
        except Exception as e:
            typer.echo(f"Error: {e}", err=True)


if __name__ == "__main__":
    app()
