# lzwdecompress_utils.py

def lzw_decompress(content: bytes, bit_length: int) -> str:
    """
    Decompresses LZW-compressed binary content encoded in UTF-16BE.
    
    Parameters:
        content (bytes): Compressed content of the .lzw file.
        bit_length (int): The bit length used during compression (between 9 and 16).
        
    Returns:
        str: The decompressed string content.
    """
    if bit_length < 9 or bit_length > 16:
        raise ValueError("Bit length must be between 9 and 16")

    MAX_TABLE_SIZE = 2 ** bit_length
    arr = content.decode("UTF-16BE")

    table = [chr(i) for i in range(256)]
    result = []

    STRING = table[ord(arr[0])]
    result.append(STRING)

    for j in range(1, len(arr)):
        code = ord(arr[j])
        if code >= len(table):
            entry = STRING + STRING[0]
        else:
            entry = table[code]
        result.append(entry)
        if len(table) < MAX_TABLE_SIZE:
            table.append(STRING + entry[0])
        STRING = entry

    return ''.join(result)
