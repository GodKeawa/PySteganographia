from libPNG import PNGImage


class FadeEncoder:
    def __init__(self, source_path: str):
        self.source_path = source_path
        self.source_image = PNGImage(source_path)

    def encode(self, target_path: str) -> None:
        target_image = PNGImage(target_path)
        if (
            self.source_image.width != target_image.width
            or self.source_image.height != target_image.height
            or self.source_image.mode != target_image.mode # mode直接决定dimension，即每个像素的通道数
        ):
            raise ValueError("Source and target images must have the same dimensions.")

        for y in range(self.source_image.height):
            for x in range(self.source_image.width):
                source_pixel = self.source_image.get_pixel(x, y)
                target_pixel = target_image.get_pixel(x, y)
                result_pixel = []
                for i in range(len(source_pixel)):
                    mix_value = (source_pixel[i] & 0xF0) | (target_pixel[i] >> 4) 
                    result_pixel.append(mix_value)
                self.source_image.set_pixel(x, y, result_pixel)

    def save(self, output_path: str) -> None:
        self.source_image.save(output_path)

if __name__ == "__main__":
    encoder = FadeEncoder("resources/Source.png")
    encoder.encode("resources/Target.png")
    encoder.save("result/Faded.png")
