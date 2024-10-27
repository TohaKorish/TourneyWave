from fastapi import APIRouter, UploadFile, File

from app.api.depenencies import ImageServiceIoC
from app.api.schema.image.image_store_response import ImageStoreResponse

router = APIRouter(prefix="/api/images", tags=["images"])


@router.post('/')
async def store_image(service: ImageServiceIoC, image: UploadFile = File(...)):
    image_url = service.store(image)

    return ImageStoreResponse(url=image_url)
