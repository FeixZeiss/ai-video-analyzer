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
    ) -> str:
        """
        Generates a structured, neutral German summary.
        """
        tags_str = ", ".join(tags) if tags else "Keine"

        user_prompt = f"""
Video-Titel:
{video_title}

Beschreibung:
{description or "Keine Beschreibung vorhanden."}

Tags:
{tags_str}

Aufgabe:
Fasse den Inhalt des Videos gemäß den oben beschriebenen Regeln zusammen.
""".strip()

        response = self.client.responses.create(
            model=self.model,
            input=[
                {"role": "developer", "content": self.template},
                {"role": "user", "content": user_prompt},
            ],
        )

        return (response.output_text or "").strip()

    def generate_comment(
        self,
        video_title: str,
        statement: str,
    ) -> str:
        """
        Generates a short, factual German comment responding to a statement.
        (Uses the same template file; adjust template if you want a different style.)
        """
        user_prompt = f"""
Video-Titel:
{video_title}

Aussage:
{statement}

Aufgabe:
Schreibe einen kurzen, sachlichen, respektvollen Kommentar zur Aussage.
Keine Beleidigungen, keine unbelegten Behauptungen.
""".strip()

        response = self.client.responses.create(
            model=self.model,
            input=[
                {"role": "developer", "content": self.template},
                {"role": "user", "content": user_prompt},
            ],
        )

        return (response.output_text or "").strip()
