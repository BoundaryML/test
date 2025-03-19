from fastapi import FastAPI, UploadFile, File, HTTPException
from pdf2image import convert_from_bytes
from PIL import Image
import io
import os
import base64
from app.baml_client import b, reset_baml_env_vars
from baml_py import Image as BamlImage
from typing import List
import logging
from dotenv import load_dotenv

load_dotenv()
os.environ["BAML_LOG"] = "WARN"
reset_baml_env_vars(dict(os.environ))

app = FastAPI()


def convert_pdf_to_images(pdf_bytes: bytes) -> List[Image.Image]:
    try:
        return convert_from_bytes(pdf_bytes, dpi=300, fmt="png")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error converting PDF: {str(e)}")


def convert_to_images(content_type: str, file_bytes: bytes) -> List[Image.Image]:
    if content_type == "application/pdf":
        return convert_pdf_to_images(file_bytes)
    elif content_type.startswith("image/"):
        img = Image.open(io.BytesIO(file_bytes))
        return [img]
    else:
        raise HTTPException(
            status_code=415, detail=f"Unsupported file type: {content_type}"
        )


def img_to_baml_image(img: Image.Image) -> BamlImage:
    buffer = io.BytesIO()
    img.save(buffer, format=img.format or "PNG")
    base64_str = base64.b64encode(buffer.getvalue()).decode()
    return BamlImage.from_base64(
        f"image/{img.format.lower() if img.format else 'png'}", base64_str
    )


@app.get("/")
async def root():
    return {
        "name": "PDF and Image Extraction API",
        "description": "This API converts PDFs and images to a format suitable for data extraction using BAML.",
        "endpoints": {
            "/": "This information",
            "/extract": "Upload a PDF or image file to extract data using BAML"
        }
    }


@app.post("/extract")
async def extract(file: UploadFile = File(...)):
    try:
        # Read file content
        content = await file.read()

        content_type = file.content_type or "application/pdf"

        # Convert to PIL Images
        images = convert_to_images(content_type, content)

        if not images:
            raise HTTPException(status_code=400, detail="No images could be extracted")

        # Process each image and extract data
        extraction_results = []
        image_data = []
        
        for i, img in enumerate(images):
            # Convert image to BAML Image for extraction
            baml_image = img_to_baml_image(img)
            
            # Call BAML function for this image
            result = b.ExtractFromImage(baml_image)
            extraction_results.append({
                "page": i+1,
                "data": result
            })
            
            # Convert image to base64 for response
            buffer = io.BytesIO()
            img.save(buffer, format="PNG")
            base64_str = base64.b64encode(buffer.getvalue()).decode()
            image_data.append({
                "page": i+1,
                "image": base64_str
            })

        return {"results": extraction_results, "images": image_data}
        
    except Exception as e:
        logging.error(f"Extraction error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
