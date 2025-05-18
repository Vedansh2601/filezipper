import fitz  # PyMuPDF
import docx
import io
import zipfile
from typing import Tuple

def read_text_from_file(content: bytes, filename: str) -> Tuple[str, bool]:
    ext = filename.lower().split('.')[-1]

    if ext == "txt":
        try:
            text = content.decode("utf-8")
        except UnicodeDecodeError:
            text = content.decode("latin1", errors="ignore")
        return text.strip(), False
        #return content.decode("utf-8", errors="ignore"), False

    elif ext == "pdf":
        doc = fitz.open(stream=content, filetype="pdf")
        full_text = ""
        contains_images = False
        for page in doc:
            text = page.get_text()
            images = page.get_images()
            full_text += text
            if images:
                contains_images = True
        return full_text.strip(), contains_images

    elif ext == "docx":
        doc_stream = io.BytesIO(content)
        doc = docx.Document(doc_stream)
        full_text = "\n".join([para.text for para in doc.paragraphs])
        return full_text.strip(), False

    elif ext == "doc":
        raise Exception("Legacy .doc files not supported. Please convert to .docx.")

    else:
        raise Exception("Unsupported file format.")

def lzw_compress(inputstring: str):
    content_length = len(set(inputstring))
    bit_length = min(max(9, (content_length).bit_length()), 16)
    MAX_TABLE_SIZE = 2 ** bit_length

    table = [chr(i) for i in range(256)]
    STRING = ""
    result = []

    for SYMBOL in inputstring:
        SS = STRING + SYMBOL
        if SS in table:
            STRING = SS
        else:
            result.append(table.index(STRING))
            if len(table) < MAX_TABLE_SIZE:
                table.append(SS)
            STRING = SYMBOL
    if STRING:
        result.append(table.index(STRING))
     
    y = "".join([chr(code) for code in result])
    return y, bit_length
if __name__ == "__main__":
    import sys
    import json

    filename = sys.argv[1]

    with open(filename, 'rb') as f:
        content = f.read()

    try:
        text, _ = read_text_from_file(content, filename)
        compressed, bit_length = lzw_compress(text)
        print(json.dumps({
            "compressed": compressed,
            "bit_length": bit_length
        }))
    except Exception as e:
        print(json.dumps({"error": str(e)}))

