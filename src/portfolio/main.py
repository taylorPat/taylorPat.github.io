from pathlib import Path
from typing import Annotated
import typer

from src.portfolio.generate_html import DEFAULT_PROFILE_YAML_PATH

app = typer.Typer()

@app.command()
def create(template_path: Annotated[Path, typer.Argument()] = DEFAULT_PROFILE_YAML_PATH):
    print(f"Template path: {template_path}")