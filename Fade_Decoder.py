from libPNG import PNGImage


class FadeDecoder:
    def __init__(self, image_path: str):
        self.image_path = image_path
        self.image = PNGImage(image_path)
        self.decoded_image = self.decode()

    def decode(self) -> PNGImage:
        decoded_image = self.image.copy()  # 复制一份，用来保存解码的图片，维持metadata
        for y in range(self.image.height):
            for x in range(self.image.width):
                pixel = self.image.get_pixel(x, y)
                target_pixel = []
                for i in range(len(pixel)):
                    target_value = (pixel[i] & 0x0F) << 4
                    target_pixel.append(target_value)
                decoded_image.set_pixel(x, y, target_pixel)
        return decoded_image

    def save(self, output_path: str) -> None:
        self.decoded_image.save(output_path)


if __name__ == "__main__":
    decoder = FadeDecoder("result/Faded.png")
    decoder.save("result/Decoded.png")
