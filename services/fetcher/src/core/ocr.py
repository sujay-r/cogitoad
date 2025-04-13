import json
import os
from pathlib import Path
from typing import Any, Dict, Optional, Union

from dotenv import load_dotenv
from mistralai import DocumentURLChunk, Mistral

from ..config import OCR_MODEL

load_dotenv()


class OCR:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("MISTRAL_API_KEY")
        if not self.api_key:
            raise ValueError(
                "Mistral API key not provided and not found in environment"
            )
        self.client = Mistral(api_key=self.api_key)

    def _parse_ocr_response_to_markdown_str(self, ocr_response: Dict[str, Any]) -> str:
        return "".join([page["markdown"] for page in ocr_response["pages"]])

    async def process(
        self,
        url: str,
        model: Optional[str] = OCR_MODEL,
        include_image_base64: Optional[bool] = True,
    ) -> Dict[str, Any]:
        """
        Process a document through Mistral's OCR.

        Args:
            url (str): URL of the file.
            model (str, optional): OCR model to use. Defaults to `mistal-ocr-latest`.
            include_image_base64 (bool, optional): Whether to include image data in response

        Returns:
            dict: Dictionary containing the OCR response
        """
        ocr_response = await self.client.ocr.process_async(
            model=model,
            document=DocumentURLChunk(document_url=url),
            include_image_base64=include_image_base64,
        )

        return json.loads(ocr_response.model_dump_json())

    async def _upload_document(self, file_name: str, file_bytes: bytes) -> str:
        """
        Upload a document to Mistral.

        Args:
            file_path: Path to the document file

        Returns:
            ID of the uploaded file
        """
        uploaded_file = await self.client.files.upload_async(
            file={"file_name": file_name, "content": file_bytes},
            purpose="ocr",
        )
        return uploaded_file.id

    async def process_file_bytes(
        self,
        file_name: str,
        file_bytes: bytes,
        model: Optional[str] = OCR_MODEL,
        include_image_base64: Optional[bool] = True,
        url_expiry_hours: Optional[int] = 1,
    ) -> Dict[str, Any]:
        """
        Process a document through Mistral's OCR.

        Args:
            file_path: Path to the document file
            model: OCR model to use
            include_image: Whether to include image data in response
            file_purpose: Purpose of the file upload
            url_expiry_hours: Hours until the signed URL expires

        Returns:
            Dictionary containing the OCR response
        """
        uploaded_file_id = await self._upload_document(file_name, file_bytes)

        # Get a signed URL
        signed_url = self.client.files.get_signed_url(
            file_id=uploaded_file_id, expiry=url_expiry_hours
        )

        return await self.process(signed_url.url, model, include_image_base64)

    async def process_file_from_path(
        self, file_path: Union[str, Path], **kwargs
    ) -> Dict[str, Any]:
        """
        Read a file from the given path and run OCR on it.

        Args:
            file_path (Union[str, Path]): Path to the file

        Returns:
            dict: OCR output for the given file
        """
        file_path = Path(file_path)
        file_name = file_path.stem
        file_bytes = file_path.read_bytes()

        return await self.process_file_bytes(file_name, file_bytes, **kwargs)

    async def get_markdown_from_url(self, url: str, **kwargs) -> str:
        ocr_response = await self.process(url, **kwargs)
        return self._parse_ocr_response_to_markdown_str(ocr_response)

    async def get_markdown_from_file_bytes(
        self, file_name: str, file_bytes: bytes, **kwargs
    ) -> str:
        ocr_response = await self.process_file_bytes(file_name, file_bytes, **kwargs)
        return self._parse_ocr_response_to_markdown_str(ocr_response)

    async def get_markdown_from_file_path(
        self, file_path: Union[str, Path], **kwargs
    ) -> str:
        ocr_response = await self.process_file_from_path(file_path, **kwargs)
        return self._parse_ocr_response_to_markdown_str(ocr_response)


if __name__ == "__main__":
    import asyncio

    ocr = OCR()
    result = asyncio.run(
        ocr.get_markdown_from_url(
            "https://cognitionandculture.net/wp-content/uploads/10.1.1.69.4147.pdf"
        )
    )
    print(result)
