import pytest
from dotenv import load_dotenv
from src.core.ocr import OCR

load_dotenv()


@pytest.fixture
def ocr():
    return OCR()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_ocr_url(ocr):
    file_url = "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"
    result = await ocr.process(file_url)
    expected_output = {
        "pages": [
            {
                "index": 0,
                "markdown": "# Dummy PDF file",
                "images": [],
                "dimensions": {"dpi": 200, "height": 2339, "width": 1653},
            }
        ],
        "model": "mistral-ocr-2503-completion",
        "usage_info": {"pages_processed": 1, "doc_size_bytes": 13264},
    }
    assert result["pages"] == expected_output["pages"]
