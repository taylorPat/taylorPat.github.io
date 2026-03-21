from pathlib import Path
import shutil

from jinja2 import Environment, FileSystemLoader, select_autoescape
import yaml

BASE_PATH = Path(__file__).resolve().parent
PROFILE_FILE = BASE_PATH / "data" / "profile.yml"

TEMPLATES_DIR = BASE_PATH / "templates"
OUTPUT_DIR = BASE_PATH.parent / "docs"
OUTPUT_FILE = OUTPUT_DIR / "index.html"


def load_data(file_path: Path) -> yaml.YAMLObject:
    print(f"Loading YAML from: {file_path}")
    print(f"Exists: {file_path.exists()}")
    print(f"Size: {file_path.stat().st_size if file_path.exists() else 'N/A'}")

    with file_path.open("r", encoding="utf-8") as file:
        content = file.read()
        print("RAW CONTENT:")
        print(content)
        return yaml.safe_load(content)


def render_template(yaml_data, templates_dir, template_name: str):
    env = Environment(
        loader=FileSystemLoader(searchpath=str(templates_dir)),
        autoescape=select_autoescape(["html", "xml"]),
    )
    template = env.get_template(name=template_name)
    return template.render(yaml_data)


def write_output(html: str, save_path: Path):
    save_path.parent.mkdir(parents=True, exist_ok=True)
    with save_path.open("w", encoding="utf-8") as file:
        file.write(html)


def copy_static():
    static_src = BASE_PATH / "static"
    static_dst = OUTPUT_DIR / "static"
    if static_dst.exists():
        shutil.rmtree(static_dst)
    shutil.copytree(static_src, static_dst)


def create_empty_docs_dir():
    shutil.rmtree(path=OUTPUT_DIR, ignore_errors=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=False)


def build():
    data = load_data(PROFILE_FILE)
    html = render_template(data, TEMPLATES_DIR, "index.html.jinja")
    create_empty_docs_dir()
    write_output(html, OUTPUT_FILE)
    copy_static()
    print(f"Wrote {OUTPUT_FILE}")


if __name__ == "__main__":
    build()
