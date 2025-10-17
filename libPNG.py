import numpy as np
from PIL import Image
from PIL.PngImagePlugin import PngInfo


class PNGImage:
    def __init__(self, image_path=None):
        self.width = 0
        self.height = 0
        self.mode = None
        self.format = None

        self.pixels = np.array([], dtype=np.uint8)
        self.metadata = {}

        if image_path:
            self.load_from_file(image_path)

    def load_from_file(self, image_path: str):
        img = Image.open(image_path)

        # 基本信息
        self.width, self.height = img.size
        self.mode = img.mode
        self.format = img.format

        # 像素数据
        self.pixels = np.array(img, dtype=np.uint8)

        # 不处理调色板模式
        if img.mode == "P":
            raise RuntimeError("Palette mode 'P' is not supported in this version.")

        # 提取PNG文本块元数据
        self._extract_metadata(img)

        print(f"loaded: {image_path}")
        print(f"  size: {self.width}x{self.height}")
        print(f"  mode: {self.mode}")
        print(f"  metadata: {self.metadata}")

    def _extract_metadata(self, img):
        for key in img.info.keys():
            self.metadata[key] = img.info[key]

    def get_pixel(self, x: int, y: int) -> np.ndarray:
        if not self._validate_coords(x, y):
            raise ValueError(f"OutOfRange: ({x}, {y})")
        return self.pixels[y, x].copy()

    def set_pixel(self, x: int, y: int, color):
        if not self._validate_coords(x, y):
            raise ValueError(f"OutOfRange: ({x}, {y})")

        # 类型检查和转换
        if isinstance(color, (list, tuple)):
            color = np.array(color, dtype=np.uint8)
        elif isinstance(color, (int, float)):
            color = np.uint8(color)
        else:
            raise ValueError(f"InvalidColorFormat: ({x}, {y})")

        self.pixels[y, x] = color

    def add_metadata(self, key: str, value: str):
        self.metadata[key] = value

    def get_metadata(self, key: str) -> str | None:
        return self.metadata.get(key)

    def save(self, output_path: str):
        # 从numpy数组创建PIL图像，模式可以自动推导
        img = Image.fromarray(self.pixels)

        # 准备PNG元数据
        pnginfo = PngInfo()
        save_kwargs = {
            "format": "PNG",
            "pnginfo": pnginfo,
        }
        for key, value in self.metadata.items():
            if isinstance(value, str):
                pnginfo.add_text(key, value)
            else:
                save_kwargs[key] = value
        # 保存文件

        img.save(output_path, **save_kwargs)
        print(f"saved: {output_path}")
        print(f"  size: {self.width}x{self.height}")
        print(f"  mode: {self.mode}")
        print(f"  metadata: {self.metadata}")

    def _validate_coords(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def copy(self):
        new_image = PNGImage()
        new_image.width = self.width
        new_image.height = self.height
        new_image.mode = self.mode
        new_image.format = self.format
        new_image.pixels = self.pixels.copy() if self.pixels is not None else None
        new_image.metadata = self.metadata.copy()
        return new_image


# Example usage
if __name__ == "__main__":
    png = PNGImage("resources/Figure1-origin.png")

    png.save("result/test-output.png")
