import re
from pathlib import Path

from jinja2 import Environment, FileSystemLoader


class TemplateHandler:
    def __init__(self):
        self.env = Environment(
            loader=FileSystemLoader("config/templates"),
            trim_blocks=True,
            lstrip_blocks=True
        )

    def render(self, template_name: str, data: dict) -> str:
        """Render template with data"""
        template = self.env.get_template(template_name)
        return template.render(**data)

    def save(self, file_path: str, content: str) -> None:
        """Save rendered content to file"""
        output_path = Path(file_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Remove comments and empty lines after comment removal
        filtered_content = []
        for line in content.splitlines():
            line = re.sub(r'#.*$', '', line).rstrip()
            if line:
                filtered_content.append(line)

        cleaned_content = '\n'.join(filtered_content)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(cleaned_content)
