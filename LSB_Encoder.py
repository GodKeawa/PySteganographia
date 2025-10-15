from pickletools import uint8

from libPNG import PNGImage

class LSBEncoder:
    def __init__(self, image_path: str):
        self.image_path = image_path
        self.image = PNGImage(image_path)

    def encode(self, data: bytes) -> None:
        capacity = (self.image.width * self.image.height * len(self.image.get_pixel(0, 0))) // 8
        print(
            "Available capacity (in bytes): ", capacity
        )
        if len(data) * 8 > capacity * 8:
            raise ValueError("Data is too large to encode in the image.")
        bits : list[bool] = []
        for byte in data:
            for i in range(8):
                bits.append(bool((byte >> (7 - i)) & 1))  # Extract each bit

        bit_index = 0
        for y in range(self.image.height):
            for x in range(self.image.width):
                if bit_index >= len(bits):
                    break
                pixel = list(self.image.get_pixel(x, y))
                for channel in range(len(pixel)):
                    if bit_index < len(bits):
                        pixel[channel] = (pixel[channel] & 0xfe) | bits[bit_index]  # Set LSB
                        bit_index += 1
                self.image.set_pixel(x, y, tuple(pixel))
            if bit_index >= len(bits):
                break

    def save(self, output_path: str) -> None:
        self.image.save(output_path)

if __name__ == "__main__":
    encoder = LSBEncoder("resources/Figure1-origin.png")
    secret_message = "Hello, World!"
    encoder.encode(secret_message.encode('utf-8'))
    encoder.save("result/Figure1-encoded-1.png")
