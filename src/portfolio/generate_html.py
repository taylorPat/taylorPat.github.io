from pathlib import Path
import shutil

from jinja2 import Environment, FileSystemLoader, select_autoescape
import yaml


def load_data(file_path: Path) -> yaml.YAMLObject:
    print(f"Loading YAML from: {file_path}")
    print(f"Exists: {file_path.exists()}")
    print(f"Size: {file_path.stat().st_size if file_path.exists() else 'N/A'}")

    with file_path.open("r", encoding="utf-8") as file:
        content = file.read()
        print("RAW CONTENT:")
        print(content)
        return yaml.safe_load(content)


def render_template(yaml_data):
    templates_dir = Path().cwd() / "src" / "portfolio" / "FE" / "templates"
    env = Environment(
        loader=FileSystemLoader(searchpath=str(templates_dir)),
        autoescape=select_autoescape(["html", "xml"]),
    )
    template = env.get_template(name="index.html.jinja")
    return template.render(yaml_data)


def write_output(html: str, output_path: Path):
    _create_empty_docs_dir(output_path=output_path)
    html_file = output_path / "index.html"
    with html_file.open("w", encoding="utf-8") as file:
        file.write(html)
    _copy_static(output_path=output_path)


def _copy_static(output_path: Path):
    static_src = Path().cwd() / "src" / "portfolio" / "FE" / "static"
    static_dst = output_path / "static"
    shutil.copytree(static_src, static_dst)


def _create_empty_docs_dir(output_path: Path):
    shutil.rmtree(path=output_path, ignore_errors=True)
    output_path.mkdir(parents=True, exist_ok=False)


def build(file_path: Path | None = None, output_path: Path | None = None):
    file_path = file_path or Path().cwd() / "src" / "profile.yml"
    yaml_data = load_data(file_path=file_path)

    html = render_template(yaml_data=yaml_data)

    output_path = output_path or Path().cwd() / "docs"
    write_output(html=html, output_path=output_path)


if __name__ == "__main__":
    build()
