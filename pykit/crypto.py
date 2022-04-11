def pkcs7padding(text: bytes):
    bs = 16
    padding_size = len(text)
    padding = bs - padding_size % bs
    coding = chr(padding)
    padding_text = coding * padding
    return coding, text + padding_text.encode('ascii')
