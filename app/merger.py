from io import BytesIO

from pypdf import PdfReader, PdfWriter


def merge_pdfs(files: list[BytesIO]) -> BytesIO:
    """Объединяет несколько PDF в один и возвращает BytesIO."""
    if not files:
        raise ValueError("Список файлов пуст")

    writer = PdfWriter()

    for f in files:
        reader = PdfReader(f)
        for page in reader.pages:
            writer.add_page(page)

    buffer = BytesIO()
    writer.write(buffer)
    buffer.seek(0)
    return buffer
