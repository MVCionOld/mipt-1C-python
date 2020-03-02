import string


CODEC_BANK = f"{string.ascii_uppercase}{string.ascii_lowercase}{string.digits}+/"


class CodecConverter1251:

    @staticmethod
    def encode(text):
        bits = "".join(list(map(
            lambda byte: format(byte, '08b'),
            text.encode('windows-1251')
        )))
        additional_bytes_num = (3 - (len(text) % 3)) % 3
        bits += "0" * 8 * additional_bytes_num
        last_idx = len(bits) - 6 * additional_bytes_num
        intermediate_encoded = "".join([
            CodecConverter1251._convert_codec_to(bits[i:i+6])
            for i in range(0, last_idx, 6)
        ]) + "=" * additional_bytes_num
        encoded = bytes(
            intermediate_encoded,
            encoding='windows-1251'
        )
        return encoded

    @staticmethod
    def decode(encoded):
        intermediate_encoded, bytes_repr = encoded.decode('windows-1251'), []
        for i in range(0, len(intermediate_encoded), 4):
            block = ''.join([
                format(CodecConverter1251._convert_codec_from(letter), '06b')
                for letter in intermediate_encoded[i:i + 4]
            ])
            bytes_repr.extend([
                int(block[j:j + 8], base=2)
                for j in range(0, len(block), 8)
            ])
        bytes_repr = list(filter(lambda x: x> 0, bytes_repr))
        return bytes(bytes_repr).decode('windows-1251')

    @staticmethod
    def _convert_codec_to(batch: str) -> str:
        return CODEC_BANK[int(batch, base=2)]

    @staticmethod
    def _convert_codec_from(bit_batch: str):
        return 0 if bit_batch == '=' else CODEC_BANK.index(bit_batch)


if __name__ == '__main__':

    import base64

    def test(test_text):
        print("-"*120)
        print(f"Custom encoded: {CodecConverter1251.encode(test_text)}")
        print(f"base64 encoded: {base64.b64encode(test_text.encode('windows-1251'))}")
        print(f"decode(encode(src))==src:"+
              f" {CodecConverter1251.decode(CodecConverter1251.encode(test_text)) == test_text}")

    TEST_TEXTS = [
        'qwerty 1234',
        'АБВГДЕ',
        'вышел заяц на крыльцо почесать своё ...',
        'Вновь он пережил банкротство, и теперь надо было подвести итог. Но итог был неутешительный. У него не было ничего – ни работы, ни денег, ни здоровья, ни сил, ни мыслей, ни желаний, ни душевного пыла, ни честолюбивых устремлений и, самое главное, не стало опоры, на которой держалась бы его жизнь. Ему было двадцать шесть лет, в пятый раз он потерпел неудачу и уже не чувствовал в себе мужества начать все с начала. Читать далее…',
        'Том вышел на улицу с ведром известки и длинной кистью. Он окинул взглядом забор, и радость в одно мгновенье улетела у него из души, и там — воцарилась тоска. Тридцать ярдов деревянного забора в девять футов вышины! Жизнь показалась ему бессмыслицей, существование — тяжелою ношею. Со вздохом обмакнул он кисть в известку, провел ею по верхней доске, потом проделал то же самое снова и остановился: как ничтожна белая полоска по сравнению с огромным пространством некрашеного забора! В отчаянии он опустился на землю под деревом. Из ворот выбежал вприпрыжку Джим. В руке у него было Читать далее…',
        'Неужели, по-твоему, красота, самое драгоценное, что есть в мире, валяется, как камень на берегу, который может поднять любой прохожий? Красота — это то удивительное и недоступное, что художник в тяжких душевных муках творит из хаоса мироздания. И когда она уже создана, не всякому дано ее узнать. Чтобы постичь красоту, надо вжиться в дерзание художника. Красота — мелодия, которую он поет нам, и для того чтобы она отозвалась в нашем сердце, нужны знание, восприимчивость и фантазия.'
    ]

    for text in TEST_TEXTS:
        test(text)
