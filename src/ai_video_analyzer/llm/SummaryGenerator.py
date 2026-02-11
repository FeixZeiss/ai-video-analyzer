from pathlib import Path
from typing import List, Optional

from openai import OpenAI

from ai_video_analyzer.config import get_secrets_dir, require_file


class CommentGenerator:
    """
    Uses OpenAI to generate German video summaries (or short comments) based on
    title/description/metadata. Loads OpenAI key + template from your secrets dir.
    Expected files in secrets/:
      - openai_key.txt
      - template.txt
    """

    def __init__(
        self,
        model: str = "gpt-5",
        api_key_filename: str = "openai_key.txt",
        template_filename: str = "template.txt",
        secrets_dir: Optional[Path] = None,
    ):
        self.model = model
        self.secrets_dir = secrets_dir or get_secrets_dir()

        key_path = require_file(self.secrets_dir / api_key_filename, api_key_filename)
        template_path = require_file(self.secrets_dir / template_filename, template_filename)

        self.client = OpenAI(api_key=key_path.read_text(encoding="utf-8").strip())
        self.template = template_path.read_text(encoding="utf-8").strip()

    def generate_summary(
        self,
        video_title: str,
        description: str = "",
        tags: Optional[List[str]] = None,
        output_format: str = "paragraph",
    ) -> str:
        """
        Generates a structured, neutral German summary.
        """
        tags_str = ", ".join(tags) if tags else "Keine"

        format_overrides = {
            "paragraph": "",
            "sections": (
                "Ausgabeformat (ueberschreibt nur die Form):\n"
                "Liefere exakt drei Zeilen:\n"
                "Thema: <ein Satz>\n"
                "Kernpunkte: <zwei bis vier kurze Saetze>\n"
                "Fazit: <ein kurzer Satz>\n"
                "Keine Aufzaehlungszeichen."
            ),
        }
        if output_format not in format_overrides:
            raise ValueError(f"Unsupported output_format: {output_format}")

        user_prompt = f"""
        Video-Titel:
        {video_title}

        Beschreibung:
        {description or "Keine Beschreibung vorhanden."}

        Tags:
        {tags_str}

        Aufgabe:
        Fasse den Inhalt des Videos gemaess den oben beschriebenen Regeln zusammen.
        """.strip()

        input_messages = [{"role": "developer", "content": self.template}]
        if format_overrides[output_format]:
            input_messages.append({"role": "developer", "content": format_overrides[output_format]})
        input_messages.append({"role": "user", "content": user_prompt})

        response = self.client.responses.create(
            model=self.model,
            input=input_messages,
        )

        return (response.output_text or "").strip()
