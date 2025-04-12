import json
import os
from pathlib import Path

from dotenv import load_dotenv
from mistralai import DocumentURLChunk, Mistral

load_dotenv()


client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))
pdf_file = Path("/home/sujay/Code/cogitoad/ida_paper.pdf")

uploaded_file = client.files.upload(
    file={"file_name": pdf_file.stem, "content": pdf_file.read_bytes()}, purpose="ocr"
)
signed_url = client.files.get_signed_url(file_id=uploaded_file.id, expiry=1)

ocr_response = client.ocr.process(
    model="mistral-ocr-latest",
    document=DocumentURLChunk(document_url=signed_url.url),
    include_image_base64=True,
)

response_dict = json.loads(ocr_response.model_dump_json())
print(json.dumps(response_dict, indent=4)[:10000])
