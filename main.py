from LSB_Decoder import LSBDecoder
from LSB_Encoder import LSBEncoder

def test(from_path: str, to_path: str, message: str, save_type: str = 'utf-8') -> None:
    encoder = LSBEncoder(from_path)
    encoder.encode(message.encode(save_type))
    encoder.save(to_path)

    decoder = LSBDecoder(to_path, parse_type=save_type)
    print(decoder.result)

if __name__ == "__main__":
    test("resources/Figure1-origin.png", "result/Figure1-encoded-1.png", "Hello, World!")