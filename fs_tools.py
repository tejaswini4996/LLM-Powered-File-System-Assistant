import os
import re

from pathlib import Path
from PyPDF2 import PdfReader
from docx import Document


def read_file(filepath: str) -> dict:

    try:

        path = Path(filepath)

        if not path.exists():
            return {
                "success": False,
                "error": "File not found"
            }

        ext = path.suffix.lower()

        content = ""

        if ext == ".txt":

            with open(path, "r", encoding="utf-8") as f:
                content = f.read()

        elif ext == ".pdf":

            pdf = PdfReader(filepath)

            for page in pdf.pages:
                text = page.extract_text()

                if text:
                    content += text + "\n"

        elif ext == ".docx":

            doc = Document(filepath)

            for para in doc.paragraphs:
                content += para.text + "\n"

        else:

            return {
                "success": False,
                "error": "Unsupported file type"
            }

        return {
            "success": True,
            "filename": path.name,
            "extension": ext,
            "size": path.stat().st_size,
            "content": content
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }


def list_files(directory: str, extension: str = None):

    files = []

    for file in Path(directory).iterdir():

        if file.is_file():

            if extension and file.suffix != extension:
                continue

            files.append(
                {
                    "name": file.name,
                    "size": file.stat().st_size,
                    "modified": file.stat().st_mtime
                }
            )

    return files


def write_file(filepath: str, content: str):

    try:

        path = Path(filepath)

        path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

        return {
            "success": True,
            "filepath": filepath
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }


def search_in_file(
    filepath: str,
    keyword: str
):

    result = read_file(filepath)

    if not result["success"]:
        return result

    content = result["content"]

    matches = []

    pattern = re.finditer(
        keyword,
        content,
        re.IGNORECASE
    )

    for match in pattern:

        start = max(0, match.start() - 40)
        end = min(
            len(content),
            match.end() + 40
        )

        matches.append(
            content[start:end]
        )

    return {
        "success": True,
        "keyword": keyword,
        "count": len(matches),
        "matches": matches
    }