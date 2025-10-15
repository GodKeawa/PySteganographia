from libPNG import PNGImage


class FadeEncoder:
    def __init__(self, source_path: str, target_path: str):
        self.source_path = source_path
        self.target_path = target_path
        self.source_image = PNGImage(source_path)
        self.target_image = PNGImage(target_path)

    def encode(self) -> None:
        if (
            self.source_image.width != self.target_image.width
            or self.source_image.height != self.target_image.height
            or self.source_image.mode != self.target_image.mode # mode直接决定dimension，即每个像素的通道数
        ):
            raise ValueError("Source and target images must have the same dimensions.")

        for y in range(self.source_image.height):
            for x in range(self.source_image.width):
                source_pixel = self.source_image.get_pixel(x, y)
                target_pixel = self.target_image.get_pixel(x, y)
                result_pixel = []
                for i in range(len(source_pixel)):
                    mix_value = (source_pixel[i] & 0xF0) | (target_pixel[i] >> 4) 
                    result_pixel.append(mix_value)
                self.source_image.set_pixel(x, y, result_pixel)

    def save(self, output_path: str) -> None:
        self.source_image.save(output_path)

if __name__ == "__main__":
    encoder = FadeEncoder("resources/Source.png", "resources/Target.png")
    encoder.encode()
    encoder.save("result/Faded.png")
