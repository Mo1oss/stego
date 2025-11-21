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
    try:
        prefix, pixels, offset = read_bmp_header(image_path)
        message_with_delimiter = message + "###END###"
        binary_message = text_to_binary(message_with_delimiter)
        message_length = len(binary_message)
        if message_length > len(pixels):
            raise ValueError(f"Message too long. Max {len(pixels)} bits, got {message_length}")
        for i in range(message_length):
            pixels[i] = (pixels[i] & 0xFE) | int(binary_message[i])
        write_bmp(output_path, prefix, pixels, offset)
        print(f"Message hidden successfully in {output_path}")
        print(f"Message length: {len(message)} characters ({message_length} bits)")
    except Exception as e:
        print(f"Error hiding message: {e}")


def extract_message(image_path):
    """Extract hidden message from BMP image"""
    try:
        prefix, pixels, offset = read_bmp_header(image_path)
        binary_message = ''
        for pixel in pixels:
            binary_message += str(pixel & 1)
        text = binary_to_text(binary_message)
        delimiter_pos = text.find("###END###")
        if delimiter_pos == -1:
            print("No hidden message found or message corrupted")
            return None
        message = text[:delimiter_pos]
        print(f"Message extracted successfully: {len(message)} characters")
        return message
    except Exception as e:
        print(f"Error extracting message: {e}")
        return None

def main():
    """Main menu for steganography application"""
    print("\n=== BMP Image Steganography ===")
    print("1. Hide message in image")
    print("2. Extract message in image")
    print("3. Exit")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == '1':
        image_path = input("Enter input BMP image path: ").strip()
        output_path = input("Enter output BMP image path: ").strip()
        print("\nEnter message to hide:")
        print("1. Type message")
        print("2. Read from file")
        msg_choice = input("Choice (1-2): ").strip()
        
        if msg_choice == '1':
            message = input("Enter your secret message: ")
        elif msg_choice == '2':
            file_path = input("Enter file path: ").strip()
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    message = f.read()
            except Exception as e:
                print(f"Error reading file: {e}")
                return
        else:
            print("Invalid choice")
            return
        
        hide_message(image_path, message, output_path)
        
    elif choice == '2':
        image_path = input("Enter BMP image path: ").strip()
        message = extract_message(image_path)
        
        if message:
            print("\n--- Hidden Message ---")
            print(message)
            print("----------------------")
            
            save = input("\nSave to file? (y/n): ").strip().lower()
            if save == 'y':
                output_file = input("Enter output file path: ").strip()
                try:
                    with open(output_file, 'w', encoding='utf-8') as f:
                        f.write(message)
                    print(f"Message saved to {output_file}")
                except Exception as e:
                    print(f"Error saving file: {e}")
                    
    elif choice == '3':
        print("Exiting...")
        return
    else:
        print("Invalid choice")


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


