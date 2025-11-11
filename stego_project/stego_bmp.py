
def read_bmp_header(filepath):
    """Return the full pre-pixel prefix (0..offset-1), the pixel bytes, and offset."""
    raise NotImplementedError

def write_bmp(filepath, prefix, pixel_data, offset):
    """Write the exact original prefix (up to offset), then the modified pixels."""
    raise NotImplementedError

def text_to_binary(text):
    """Convert text to binary string"""
    raise NotImplementedError

def binary_to_text(binary):
    """Convert binary string to text"""
    raise NotImplementedError

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


