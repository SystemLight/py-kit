from typing import Literal

class Convert:

    def __init__(self, data: str):
        self.prefix = data[0:2]
        self.real_data = data[2:]

        if self.prefix == '0b':
            self.number = int(self.real_data, 2)
            self.hex = format(self.number, 'X')
            self.bytes = bytes.fromhex(self.hex)
        elif self.prefix == '0x':
            self.number = int(self.real_data, 16)
            self.hex = self.real_data
            self.bytes = bytes.fromhex(self.real_data)
        elif self.prefix == '0d':
            self.number = int(self.real_data)
            self.hex = format(self.number, 'X')
            self.bytes = bytes.fromhex(self.hex)
        elif self.prefix == '0t':
            self.number = int.from_bytes(self.real_data.encode('utf-8'), 'big', signed=False)
            self.hex = format(self.number, 'X')
            self.bytes = self.real_data.encode('utf-8')
        else:
            raise ValueError('data type not supported')

    def __getitem__(self, item: Literal['number', 'hex', 'bytes']):
        if item == 'number':
            return self.number
        elif item == 'hex':
            return self.hex
        else:
            return self.bytes


def convert_dict(data, rules):
    for i in rules:
        if data.get(i[0]):
            data[i[0]] = Convert(data[i[0]])[i[1]]
    return data
