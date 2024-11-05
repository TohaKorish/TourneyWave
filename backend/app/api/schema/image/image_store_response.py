from pydantic import BaseModel


class ImageStoreResponse(BaseModel):
    url: str
