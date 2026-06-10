import re

class TextSeparator:
    """
    Cleans and normalizes raw text before chunking & embedding
    """

    @staticmethod
    def clean_text(text: str) -> str:
        if not text:
            return ""

        # Remove multiple newlines
        text = re.sub(r"\n{2,}", "\n", text)

        # Remove multiple spaces
        text = re.sub(r"\s{2,}", " ", text)

        # Remove page numbers (PDF noise)
        text = re.sub(r"\bPage\s+\d+\b", "", text, flags=re.IGNORECASE)

        # Remove headers/footers patterns (customize if needed)
        text = re.sub(r"©.*", "", text)
        text = re.sub(r"All rights reserved.*", "", text, flags=re.IGNORECASE)

        return text.strip()

    @staticmethod
    def separate_by_type(
        content: str,
        source_type: str
    ) -> str:
        """
        Apply source-specific cleaning
        """

        content = TextSeparator.clean_text(content)

        if source_type == "pdf":
            return content

        if source_type == "txt":
            return content

        if source_type == "excel":
            # Excel rows must stay compact
            return content.replace("\n", " ")

        return content
