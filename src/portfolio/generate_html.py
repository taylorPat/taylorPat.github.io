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


DEFAULT_TEMPLATE_FOLDER_PATH = Path().cwd() / "data" / "FE" / "templates"


def render_template(
    yaml_data, template_folder_path: Path, html_template_file_name: str
):
    env = Environment(
        loader=FileSystemLoader(searchpath=str(template_folder_path)),
        autoescape=select_autoescape(["html", "xml"]),
    )
    template = env.get_template(name=html_template_file_name)
    return template.render(yaml_data)


def write_output(html: str, output_path: Path):
    _create_empty_docs_dir(output_path=output_path)
    html_file = output_path / "index.html"
    with html_file.open("w", encoding="utf-8") as file:
        file.write(html)
    _copy_static(output_path=output_path)


def _copy_static(output_path: Path):
    static_src = Path().cwd() / "data" / "FE" / "static"
    static_dst = output_path / "static"
    shutil.copytree(static_src, static_dst)


def _create_empty_docs_dir(output_path: Path):
    shutil.rmtree(path=output_path, ignore_errors=True)
    output_path.mkdir(parents=True, exist_ok=False)


DEFAULT_PROFILE_YAML_PATH = Path().cwd() / "data" / "profile.yml"
DEFAULT_HTML_TEMPLATE_FILE_NAME = "index.html.jinja"


def build(
    profile_yaml_path: Path | None = None,
    template_folder_path: Path | None = None,
    html_template_file_name: str | None = None,
):
    profile_yaml_path = profile_yaml_path or DEFAULT_PROFILE_YAML_PATH
    yaml_data = load_data(file_path=profile_yaml_path)

    template_folder_path = template_folder_path or DEFAULT_TEMPLATE_FOLDER_PATH
    html_template_file_name = html_template_file_name or DEFAULT_HTML_TEMPLATE_FILE_NAME
    html = render_template(
        yaml_data=yaml_data,
        template_folder_path=template_folder_path,
        html_template_file_name=html_template_file_name,
    )

    output_path = Path().cwd() / "docs"
    write_output(html=html, output_path=output_path)


if __name__ == "__main__":
    build()
