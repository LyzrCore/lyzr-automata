from ast import List
from pathlib import Path
import requests
from urllib.parse import unquote, urlparse

from lyzr_automata.data_models import FileResponse


class ResourceBox:
    def __init__(self, base_folder="resources"):
        self.base_folder = Path(base_folder)
        self.base_folder.mkdir(parents=True, exist_ok=True)

    def save_from_url(self, url, subfolder=None) -> FileResponse:
        subfolder = str(subfolder)
        # Extract file name from URL
        parsed_url = urlparse(url)
        file_name = unquote(Path(parsed_url.path).name)

        # If the URL does not contain a filename, you might want to handle this case differently
        if not file_name:
            return FileResponse(error="url not found")

        # Create the subfolder path if specified
        if subfolder:
            full_path = self.base_folder / subfolder
            full_path.mkdir(parents=True, exist_ok=True)
        else:
            full_path = self.base_folder

        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for bad responses

            file_path = full_path / file_name
            with open(file_path, "wb") as f:
                f.write(response.content)
            return FileResponse(url=url, local_file_path=str(file_path))
        except Exception as e:
            return FileResponse(error=str(e))

    def get_files_from_subfolder(self, subfolder) -> list[FileResponse]:
        subfolder = str(subfolder)
        subfolder_path = self.base_folder / subfolder
        if subfolder_path.exists() and subfolder_path.is_dir():
            return [
                FileResponse(local_file_path=str(subfolder_path / file.name))
                for file in subfolder_path.iterdir()
                if file.is_file()
            ]
        else:
            return []