from libPNG import PNGImage
from typing import Any

class LSBDecoder:
    def __init__(self, image_path: str, parse_type: str = 'bytes'):
        self.image_path = image_path
        self.image = PNGImage(image_path)
        self.bytes = self.decode()
        self.result = self.parse(parse_type)

    def decode(self) -> bytes:
        bits : list[bool] = []
        for y in range(self.image.height):
            for x in range(self.image.width):
                pixel = self.image.get_pixel(x, y)
                for channel in pixel:
                    bits.append(channel & 1)  # Extract LSB

        # Convert bits to bytes
        bytes_list : list[int] = []
        for i in range(0, len(bits), 8):
            byte = 0
            for j in range(8):
                if i + j < len(bits):
                    byte = (byte << 1) | bits[i + j]
            bytes_list.append(byte)

        return bytearray(bytes_list)

    def parse(self, parse_type : str) -> Any:
        if parse_type == 'utf-8':
            return self.bytes.decode('utf-8', errors='ignore')
        elif parse_type == 'bytes':
            return self.bytes
        else:
            try:
                return self.bytes.decode(parse_type, errors='ignore')
            except Exception:
                raise ValueError(f"Unsupported parse type: {parse_type}")

if __name__ == "__main__":
    decoder = LSBDecoder("resources/Figure2-encode.png", parse_type='utf-8')
    print(decoder.result)