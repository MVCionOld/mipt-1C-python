import string


class CodecConverter1251:
    CODEC_BANK = f"{string.ascii_uppercase}{string.ascii_lowercase}{string.digits}+/"

    @staticmethod
    def encode(data):
        bits = "".join(
            format(byte, '08b')
            for byte in data.encode('windows-1251')
        )
        additional_bytes_num = (6 - (len(bits) // 8) % 6) % 6
        bits += "0" * 8 * additional_bytes_num
        last_idx = len(bits) - 6 * additional_bytes_num
        encoded = "".join([
            CodecConverter1251._convert_codec_to(bits[i:i + 6])
            for i in range(0, last_idx, 6)
        ]) + "=" * additional_bytes_num
        raw_encoded = bytes(encoded, encoding='windows-1251')
        return raw_encoded

    @staticmethod
    def decode(raw_data):
        raw_data = raw_data.decode('windows-1251')
        ans = list()
        # import pdb; pdb.set_trace()
        for i in range(0, len(raw_data)-3, 4):
            block = ''
            for letter in raw_data[i:i + 4]:
                block += format(0 if letter == '=' else CodecConverter1251.CODEC_BANK.index(letter), '06b')
            # import pdb; pdb.set_trace()
            for j in range(0, len(block), 8):
                if int(block[j:j + 8], base=2) > 0:
                    ans.append(int(block[j:j + 8], base=2))
        return bytes(ans).decode('windows-1251')

    @staticmethod
    def _convert_codec_to(batch: str) -> str:
        return CodecConverter1251.CODEC_BANK[int(batch, base=2)]

    @staticmethod
    def _convert_codec_from(bit_batch: str):
        return 0 if bit_batch == '=' else CodecConverter1251.CODEC_BANK.index(bit_batch)


if __name__ == '__main__':

    import base64

    text = "АБВГДeёo0"
    print(
        CodecConverter1251.encode(text),
        base64.b64encode(text.encode('windows-1251')),
        CodecConverter1251.encode(text) == base64.b64encode(text.encode('windows-1251'))
    )
    print(CodecConverter1251.decode(CodecConverter1251.encode(text)))
