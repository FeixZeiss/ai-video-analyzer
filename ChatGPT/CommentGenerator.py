from openai import OpenAI

class CommentGenerator:
    def __init__(self, api_key_path="ChatGPT/key.txt", prompt_template_path="ChatGPT/template.txt"):
        # Key lesen
        with open(api_key_path, "r") as f:
            self.api_key = f.read().strip()

        self.client = OpenAI(api_key=self.api_key)

        # Prompt-Vorlage laden
        with open(prompt_template_path, "r", encoding="utf-8") as f:
            self.template = f.read()

    def generate_comment(self, video_title, statement):
        """
        Erzeugt einen sachlichen Kommentar zu einer Videoaussage.
        """
        prompt = f"""{self.template}

        Video: "{video_title}"
        Aussage: "{statement}"
        Antwort:"""

        response = self.client.chat.completions.create(
            model="gpt-5",
            messages=[
                {"role": "system", "content": "Bitte fassed mir folgende Videos anshand des Namen und Beschreibung zusammen"},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
