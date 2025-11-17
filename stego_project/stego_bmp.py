def read_bmp_header(filepath):
    """Return the full pre-pixel prefix (0..offset-1), the pixel bytes, and offset."""
    with open(filepath, 'rb') as f:
        first54 = f.read(54)
        if first54[0:2] != b'BM':
            raise ValueError("Not a valid BMP file")
        offset = int.from_bytes(first54[10:14], 'little')
        f.seek(0)
        prefix = f.read(offset)
        pixels = bytearray(f.read())
    return prefix, pixels, offset

def write_bmp(filepath, prefix, pixel_data, offset):
    """Write the exact original prefix (up to offset), then the modified pixels."""
    with open(filepath, 'wb') as f:
        f.write(prefix)
        f.write(pixel_data)


def text_to_binary(text):
    """Convert text to binary string"""
    binary = ''
    for char in text:
        binary += format(ord(char), '08b')
    return binary

def binary_to_text(binary):
    """Convert binary string to text"""
    text = ''
    for i in range(0, len(binary), 8):
        byte = binary[i:i+8]
        if len(byte) == 8:
            text += chr(int(byte, 2))
    return text

def hide_message(image_path, message, output_path):
    """Hide message in BMP image using LSB steganography"""
    raise NotImplementedError

def extract_message(image_path):
    """Extract hidden message from BMP image"""
    raise NotImplementedError

def main():
    print("\n=== BMP Image Steganography ===")
    print("1. Hide message in image")
    print("2. Extract message in image")
    print("3. Exit")

    choice = input("\nEnter choice (1-3): ").strip()
    print("WIP choice:", choice) 

    if choice == "3":
        print("Exiting program...")
        raise SystemExit


if __name__ == "__main__":
  while True:
    try:
        main()
        cont = input("\nContinue? (y/n): ").strip().lower()
        if cont != 'y':
            print("Goodbye!")
            break
    except KeyboardInterrupt:
        print("\n\nExiting...")
        break


