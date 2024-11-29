def pad(data, block_size):
    padding_length = block_size - len(data) % block_size
    return data + bytes([padding_length] * padding_length)

def unpad(data, block_size):
    padding_length = data[-1]
    if padding_length > block_size:
        raise ValueError("Invalid padding")
    return data[:-padding_length]
