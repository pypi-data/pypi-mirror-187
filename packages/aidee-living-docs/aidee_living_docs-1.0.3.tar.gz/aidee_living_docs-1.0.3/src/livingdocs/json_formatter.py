"""Behave JSONFormatter."""
import json
from os import path

from .collecting_formatter import CollectingFormatter


class JSONFormatter(CollectingFormatter):
    """Main class used by Behave framework."""

    def __init__(self, stream_opener, config):
        super().__init__(stream_opener, config)

        self.outputDirectory = path.join(
            config.base_dir, config.userdata["behave.formatter.customjson.path"]
        )

        if "behave.formatter.customjson.single_file" in config.userdata:
            self.singleFile = (
                config.userdata["behave.formatter.customjson.single_file"] == "True"
            )
        else:
            self.singleFile = False

        self.features = []

    def eof(self):
        """End of file reached."""
        super().eof()

        if self.singleFile:
            self.features.append(self.current_feature)
        else:
            (_, file_name) = path.split(self.current_feature.file_name)
            (file_name, _) = path.splitext(file_name)
            file_path = path.join(self.outputDirectory, file_name + ".json")

            with open(file_path, "w") as file:
                json.dump(
                    self.current_feature, file, default=lambda o: o.__dict__, indent=2
                )

    def close(self):
        """Dump content to file on close."""
        super().close()

        if self.singleFile:
            file_path = path.join(self.outputDirectory, "behave_test_results.json")
            with open(file_path, "w") as file:
                json.dump(self.features, file, default=lambda o: o.__dict__, indent=2)
