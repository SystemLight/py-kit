from typing import Literal, List, Tuple


def safe_hex(_hex_text):
    """

    获取安全格式HEX

    :param _hex_text:
    :return:

    """
    _hex_text = _hex_text.replace(' ', '')
    if len(_hex_text) % 2 > 0:
        return '0' + _hex_text
    else:
        return _hex_text


class Convert:

    def __init__(self, data: str):
        self.prefix = data[0:2]
        self.real_data = data[2:]

        if self.prefix == '0b':
            self.number = int(self.real_data, 2)
            self.hex = safe_hex(format(self.number, 'x'))
            self.bytes = bytes.fromhex(self.hex)
        elif self.prefix == '0x':
            self.number = int(self.real_data, 16)
            self.hex = safe_hex(self.real_data)
            self.bytes = bytes.fromhex(self.hex)
        elif self.prefix == '0d':
            self.number = int(self.real_data)
            self.hex = safe_hex(format(self.number, 'x'))
            self.bytes = bytes.fromhex(self.hex)
        elif self.prefix == '0t':
            self.bytes = self.real_data.encode('utf-8')
            self.number = int.from_bytes(self.bytes, 'big', signed=False)
            self.hex = safe_hex(format(self.number, 'x'))
        else:
            raise ValueError('data type not supported')

    def __getitem__(self, item: Literal['number', 'hex', 'bytes']):
        if item == 'number':
            return self.number
        elif item == 'hex':
            return self.hex
        elif item == 'bytes':
            return self.bytes
        else:
            raise ValueError


def convert_dict(data: dict, rules: List[Tuple[str, Literal['number', 'hex', 'bytes']]]):
    """

    根据规则转换字典中元素类型

    :param data:
    :param rules:
    :return:

    """
    for i in rules:
        if data.get(i[0]):
            data[i[0]] = Convert(data[i[0]])[i[1]]
    return data
