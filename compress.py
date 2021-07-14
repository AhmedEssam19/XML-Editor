from heapq import heappush, heappop
from collections import defaultdict

from typing import Dict, List

from bitstring import BitArray


class Node:
    def __init__(self, char, freq, left, right):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right

    def is_leaf(self) -> bool:
        return self.left is None and self.right is None

    def __lt__(self, other) -> bool:
        return self.freq < other.freq

    def __repr__(self):
        return f"Node({self.char}, {self.freq})"


def buildTrie(freq: Dict[str, int]) -> Node:
    heap = []
    for char in freq:
        heappush(heap, Node(char, freq[char], None, None))

    while len(heap) > 1:
        left = heappop(heap)
        right = heappop(heap)
        heappush(heap, Node('\0', left.freq + right.freq, left, right))

    return heappop(heap)


def buildCode(char_to_code: Dict[str, str], x: Node, code: str):
    if x.is_leaf():
        char_to_code[x.char] = code

    else:
        buildCode(char_to_code, x.left, code + '0')
        buildCode(char_to_code, x.right, code + '1')


def writeTrie(x: Node, bitArray: List[str]):
    if x.is_leaf():
        bitArray.append('1')
        bitArray.append(format(ord(x.char), '08b'))
        return

    bitArray.append('0')
    writeTrie(x.left, bitArray)
    writeTrie(x.right, bitArray)


def readTrie(trieBits: list) -> Node:
    isLeaf = int(trieBits.pop(0))
    if isLeaf:
        char = chr(int("".join([trieBits.pop(0) for _ in range(8)]), 2))
        return Node(char, -1, None, None)

    return Node('\0', -1, readTrie(trieBits), readTrie(trieBits))


def compress(file_name: str):
    # Read text file
    with open(file_name, 'rt') as xml_file:
        text = xml_file.read()

    # Tabulate frequency count
    freq = defaultdict(int)
    for char in text:
        freq[char] += 1

    # Build Huffman trie
    root = buildTrie(freq)

    # Build code table
    char_to_code = {}
    buildCode(char_to_code, root, "")

    # Save trie for decoding/expanding
    trieBits = []
    writeTrie(root, trieBits)
    trieBits = "".join(trieBits)

    # Encode text
    encoded_text = "".join([char_to_code[char] for char in text])

    # Save the compressed data
    with open(file_name.split('.')[0]+'.m3a', 'wb') as compress_file:
        compressed_data = format(len(trieBits), '064b') + trieBits + format(len(text), '064b') + encoded_text
        bitArray = BitArray(bin=compressed_data)
        bitArray.tofile(compress_file)


def expand(file_name: str) -> str:
    # Read file bits as string
    with open(file_name, 'rb') as compressed_file:
        data = compressed_file.read()
        bitArray = "".join(map(lambda byte: format(byte, '08b'), data))

    # Get the length of the trie model
    trieBitsLength = int(bitArray[:64], 2)

    # Get the trie bits
    trieBits = list(bitArray[64: 64 + trieBitsLength])

    # Construct the trie
    root = readTrie(trieBits)

    # Get characters number
    charsLength = int(bitArray[64 + trieBitsLength: 64 + trieBitsLength + 64], 2)

    # Get the encoded bits
    encoded_text = bitArray[64 + trieBitsLength + 64:]

    # Decode the text using the trie
    chars_list = []
    index = 0
    for i in range(charsLength):
        x = root
        while not x.is_leaf():
            bit = int(encoded_text[index])
            if bit:
                x = x.right
            else:
                x = x.left

            index += 1

        chars_list.append(x.char)

    return "".join(chars_list)


def minify(text: str) -> str:
    text = '>'.join([subtext.strip('\n\t ') for subtext in text.split('>')])
    text = '<'.join([subtext.strip('\n\t ') for subtext in text.split('<')])
    return text
