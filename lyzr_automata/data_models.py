from typing import Optional
from pydantic import BaseModel


class FileResponse(BaseModel):
    url: Optional[str] = None
    local_file_path: Optional[str] = None
    error: Optional[str] = None
