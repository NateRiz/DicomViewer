import os

from PIL import Image
from PIL.ImageQt import ImageQt, QImage
from PyQt6.QtGui import QPixmap


class ImageLoader:
    def __init__(self):
        pass

    def load_from_series(self, series_path, only_load_preview=False) -> dict[str, QPixmap]:
        pixmaps = {}
        for filename in os.listdir(series_path):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):  # Check for image files
                image_path = os.path.join(series_path, filename)
                try:
                    pil_image = Image.open(image_path)
                    pil_image = pil_image.convert("RGBA")
                    data = pil_image.tobytes("raw", "BGRA")
                    q_image = QImage(data, pil_image.size[0], pil_image.size[1], QImage.Format.Format_ARGB32)
                    pixmap = QPixmap.fromImage(q_image)
                    pixmaps[filename] = pixmap
                    if only_load_preview:
                        break
                except Exception as e:
                    print(f"Failed to load image {filename}: {e}")

        return pixmaps

    def load_series_preview_image(self, series_path) -> QPixmap:
        pixmaps = self.load_from_series(series_path, only_load_preview=True)
        if pixmaps:
            return next(iter(pixmaps.values()))
        return QPixmap()
