from libPNG import PNGImage
from LSB_Decoder import LSBDecoder
from LSB_Encoder import LSBEncoder
from Fade_Decoder import FadeDecoder
from Fade_Encoder import FadeEncoder
from os import path, makedirs


def test_text(
    from_path: str, to_path: str, message: str, save_type: str = "utf-8"
) -> None:
    encoder = LSBEncoder(from_path)
    encoder.encode(message.encode(save_type))
    encoder.save(to_path)

    decoder = LSBDecoder(to_path, parse_type=save_type)
    print(str(decoder.result)[: len(message) :])


def test_bytes(from_path: str, to_path: str, data: bytes) -> bytes:
    encoder = LSBEncoder(from_path)
    encoder.encode(data)
    encoder.save(to_path)

    decoder = LSBDecoder(to_path, parse_type="bytes")
    return decoder.result[: len(data) :]


def test_fade(
    source_path: str, target_path: str, output_path: str, decode_path: str
) -> None:
    encoder = FadeEncoder(source_path)
    encoder.encode(target_path)
    encoder.save(output_path)
    decoder = FadeDecoder(output_path)
    decoder.save(decode_path)


if __name__ == "__main__":
    if not path.exists("result"):
        makedirs("result")
    # test_text(
    #     "resources/Figure1-origin.png", "result/Figure1-encoded-1.png", "Hello, World!"
    # )
    # test_text(
    #     "resources/Figure1-origin.png",
    #     "result/Figure1-encoded-1.png",
    #     "Hello, World!",
    #     "ascii",
    # )
    with open("resources/HEAD.jpg", "rb") as f:
        data = f.read()
    print("data size:", len(data), "bytes, Please wait...")
    decode_data = test_bytes(
        "resources/Figure3-origin.png", "result/Figure3-encoded-1.png", data
    )
    with open("result/HEAD-out.jpg", "wb") as f:
        f.write(decode_data)

    test_fade(
        "resources/Source.png",
        "resources/Target.png",
        "result/Faded.png",
        "result/Decoded.png",
    )
