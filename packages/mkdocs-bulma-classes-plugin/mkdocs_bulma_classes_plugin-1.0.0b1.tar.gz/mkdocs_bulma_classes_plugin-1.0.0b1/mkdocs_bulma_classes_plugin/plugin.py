import re
from typing import Optional
from mkdocs.config import config_options
from mkdocs.plugins import BasePlugin


class BulmaClassesPlugin(BasePlugin):
    config_scheme = {
        ("param", config_options.Type(str, default="")),
    }

    regex_dict = {
        "<table>": '<table class="table">',
        "<h1 id=\"(.*)\">": '<h1 id=\"\g<1>\" class="title is-1 has-text-light">',
        "<h2 id=\"(.*)\">": '<h2 id=\"\g<1>\" class="title is-2 has-text-light">',
        "<h3 id=\"(.*)\">": '<h3 id=\"\g<1>\" class="title is-3 has-text-light">',
        "<h4 id=\"(.*)\">": '<h4 id=\"\g<1>\" class="title is-4 has-text-light">',
        "<h5 id=\"(.*)\">": '<h5 id=\"\g<1>\" class="title is-5 has-text-light">',
        "<h6 id=\"(.*)\">": '<h6 id=\"\g<1>\" class="title is-6 has-text-light">',
    }

    def __init__(self):
        self.enabled = True
        self.total_time = 0

    def on_post_page(self, output: str, *, page, config) -> Optional[str]:
        for key, value in self.regex_dict.items():
            output = re.sub(re.compile(key), value, output)
        return output
