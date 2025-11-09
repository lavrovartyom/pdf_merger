import io

import pytest
from pypdf import PdfReader, PdfWriter

from app.merger import merge_pdfs


@pytest.fixture
def pdf_files():
    """Создает 3 PDF-файла в памяти, по одной странице в каждом."""
    files = []
    for i in range(3):
        buf = io.BytesIO()
        writer = PdfWriter()
        writer.add_blank_page(width=200, height=200)
        writer.write(buf)
        buf.seek(0)
        files.append(buf)
    return files


def test_merge_pdfs_returns_valid_pdf(pdf_files):
    """Проверяет, что merge_pdfs возвращает корректный PDF с нужным количеством страниц."""
    result = merge_pdfs(pdf_files)

    assert isinstance(result, io.BytesIO)

    assert result.getbuffer().nbytes > 100  # примерная проверка размера

    reader = PdfReader(result)
    assert len(reader.pages) == len(pdf_files)

    for page in reader.pages:
        assert page.mediabox.width > 0
        assert page.mediabox.height > 0


def test_merge_pdfs_handles_empty_input():
    """Проверяет, что при пустом списке выбрасывается ошибка."""
    with pytest.raises(ValueError):
        merge_pdfs([])


def test_merge_pdfs_combines_content(pdf_files):
    """Проверяет, что после объединения все страницы из исходных файлов попали в результат."""
    modified_files = []
    for i, file in enumerate(pdf_files, start=1):
        buf = io.BytesIO()
        writer = PdfWriter()
        writer.add_blank_page(width=200, height=200)
        writer.add_metadata({"/Title": f"Page {i}"})
        writer.write(buf)
        buf.seek(0)
        modified_files.append(buf)

    result = merge_pdfs(modified_files)
    reader = PdfReader(result)

    assert len(reader.pages) == len(modified_files)
    assert reader.metadata is not None
