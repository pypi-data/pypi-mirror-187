"""Create Sphinx compatible feature page."""
import pathlib
import sys
from glob import glob
from os import path

from jinja2 import Environment
from jinja2 import FileSystemLoader

from .collecting_formatter import CollectedStep
from .feature_file import load_feature_file
from .feature_file import status_to_style


current_directory = pathlib.Path(__file__).parent.resolve()
env = Environment(
    autoescape=True, loader=FileSystemLoader(current_directory, followlinks=True)
)
template = env.get_template("feature.jinja2")


def screenshots_from_step(step: CollectedStep):
    """Step screenshot."""
    screenshots = []
    for line in step.text:
        line_text: str = line.strip()
        line_split = line_text.split("'")
        if len(line_split) == 3 and line_split[0] == "Save screenshot ":
            screenshots.append(line_split[1])
    return screenshots


def main(args=None):
    """Entry point when running as script."""
    if args is None:
        args = sys.argv

    if len(args) != 2:
        print(
            "Invalid command format, format is:\n {a[0]} <json feature result>\n".format(
                a=args
            )
        )
        exit(1)

    feature = load_feature_file(args[1])

    context = {
        "feature": feature,
        "status_to_style": status_to_style,
        "screenshots_from_step": screenshots_from_step,
    }

    (file_name, _) = path.splitext(args[1])
    file_name += ".rst"

    with open(file_name, "w") as file:
        file.write(template.render(**context))


def process_files_in_current_directory():
    """Process files."""
    files = glob(path.join(path.curdir, "*.json"))

    for file in files:
        print(f"Converting {file}")
        feature = load_feature_file(file)

        context = {
            "feature": feature,
            "status_to_style": status_to_style,
            "screenshots_from_step": screenshots_from_step,
        }

        (file_name, _) = path.splitext(file)
        file_name += ".rst"

        with open(file_name, "w") as file:
            file.write(template.render(**context))


if __name__ == "__main__":
    """If invoked directly as script, relay to main() method."""
    main()
