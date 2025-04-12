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

    async def _upload_document(self, file_path: Union[str, Path]) -> str:
        """
        Upload a document to Mistral.

        Args:
            file_path: Path to the document file

        Returns:
            ID of the uploaded file
        """
        file_path = Path(file_path)
        uploaded_file = await self.client.files.upload_async(
            file={"file_name": file_path.stem, "content": file_path.read_bytes()},
            purpose="ocr",
        )
        return uploaded_file.id

    async def process_file(
        self,
        file_path: Union[str, Path],
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
        uploaded_file_id = await self._upload_document(file_path)

        # Get a signed URL
        signed_url = self.client.files.get_signed_url(
            file_id=uploaded_file_id, expiry=url_expiry_hours
        )

        return await self.process(signed_url.url, model, include_image_base64)


if __name__ == "__main__":
    import asyncio

    ocr = OCR()
    result = asyncio.run(ocr.process(url="https://arxiv.org/pdf/1810.08575"))
    print(json.dumps(result, indent=4)[:2000])
