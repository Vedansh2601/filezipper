import heapq
import os
import json
import time

class HuffmanCoding:
    def __init__(self, path):
        self.path = path
        self.heap = []
        self.codes = {}
        self.reverse_mapping = {}

    class HeapNode:
        def __init__(self, char, freq):
            self.char = char
            self.freq = freq
            self.left = None
            self.right = None

        def __lt__(self, other):
            return self.freq < other.freq

    def make_frequency_dict(self, text):
        frequency = {}
        for character in text:
            frequency[character] = frequency.get(character, 0) + 1
        return frequency

    def make_heap(self, frequency):
        for key in frequency:
            heapq.heappush(self.heap, self.HeapNode(key, frequency[key]))

    def merge_nodes(self):
        while len(self.heap) > 1:
            node1 = heapq.heappop(self.heap)
            node2 = heapq.heappop(self.heap)
            merged = self.HeapNode(None, node1.freq + node2.freq)
            merged.left = node1
            merged.right = node2
            heapq.heappush(self.heap, merged)

    def make_codes_helper(self, root, current_code):
        if root is None:
            return
        if root.char is not None:
            self.codes[root.char] = current_code
            return
        self.make_codes_helper(root.left, current_code + "0")
        self.make_codes_helper(root.right, current_code + "1")

    def make_codes(self):
        root = heapq.heappop(self.heap)
        self.make_codes_helper(root, "")

    def get_encoded_text(self, text):
        return ''.join(self.codes[char] for char in text)

    def pad_encoded_text(self, encoded_text):
        extra_padding = 8 - len(encoded_text) % 8
        return "{0:08b}".format(extra_padding) + encoded_text + "0" * extra_padding

    def get_byte_array(self, padded_encoded_text):
        return bytearray(int(padded_encoded_text[i:i+8], 2) for i in range(0, len(padded_encoded_text), 8))

    def compress(self, save_dir="compressed"):
        start_time = time.time()
        filename = os.path.splitext(os.path.basename(self.path))[0]
        ext = os.path.splitext(self.path)[1]
        os.makedirs(save_dir, exist_ok=True)
        output_path = os.path.join(save_dir, f"{filename}_compressed.bin")

        with open(self.path, 'r', encoding='utf-8', errors='ignore') as file:
            text = file.read()

        frequency = self.make_frequency_dict(text)
        self.make_heap(frequency)
        self.merge_nodes()
        self.make_codes()

        encoded_text = self.get_encoded_text(text)
        padded_encoded_text = self.pad_encoded_text(encoded_text)
        byte_array = self.get_byte_array(padded_encoded_text)

        header = {
            "frequency": frequency,
            "original_extension": ext
        }

        with open(output_path, 'wb') as output:
            output.write((json.dumps(header) + '\n').encode('utf-8'))
            output.write(byte_array)

        end_time = time.time()
        duration = end_time - start_time
        input_size = os.path.getsize(self.path)
        output_size = os.path.getsize(output_path)
        compression_ratio = output_size / input_size
        percentage = (1 - compression_ratio) * 100

        return {
            "file_path": output_path,
            "compression_ratio": round(compression_ratio, 4),
            "percentage_saved": round(percentage, 2),
            "time_taken": round(duration, 4)
        }

    def remove_padding(self, padded_encoded_text):
        extra_padding = int(padded_encoded_text[:8], 2)
        return padded_encoded_text[8:-extra_padding]

    def build_decode_tree(self):
        tree = {}
        for char, code in self.codes.items():
            node = tree
            for bit in code:
                node = node.setdefault(bit, {})
            node['char'] = char
        return tree

    def decode_text_tree(self, encoded_text, tree):
        node = tree
        decoded_text = []
        for bit in encoded_text:
            node = node[bit]
            if 'char' in node:
                decoded_text.append(node['char'])
                node = tree
        return ''.join(decoded_text)

    def decompress(self, save_dir="decompressed"):
        os.makedirs(save_dir, exist_ok=True)
        filename = os.path.splitext(os.path.basename(self.path))[0]

        with open(self.path, 'rb') as file:
            header_bytes = b""
            while True:
                byte = file.read(1)
                if byte == b'\n':
                    break
                header_bytes += byte
            header = json.loads(header_bytes.decode('utf-8'))
            frequency = header["frequency"]
            ext = header["original_extension"]

            self.make_heap(frequency)
            self.merge_nodes()
            self.make_codes()

            bit_chunks = []
            byte = file.read(1)
            while byte:
                bits = bin(int.from_bytes(byte, 'big'))[2:].rjust(8, '0')
                bit_chunks.append(bits)
                byte = file.read(1)
            bit_string = ''.join(bit_chunks)

            encoded_text = self.remove_padding(bit_string)
            decode_tree = self.build_decode_tree()
            decompressed_text = self.decode_text_tree(encoded_text, decode_tree)

        output_path = os.path.join(save_dir, f"{filename}_decompressed{ext}")
        with open(output_path, 'w', encoding='utf-8') as output:
            output.write(decompressed_text)

        return output_path
