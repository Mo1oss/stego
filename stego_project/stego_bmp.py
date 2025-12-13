# Function to read header and pixel data from a BMP image
def read_bmp_header_and_pixels(input_bmp_image):

    # Open the input BMP file in binary read mode
    with open(input_bmp_image, 'rb') as bmp_file:

        # Read the first 54 bytes (standard BMP header)
        header_54 = bmp_file.read(54)

        # Check if the file starts with 'BM' signature
        if header_54[0:2] != b'BM':
            # If signature is wrong, it's not a valid BMP file
            raise ValueError("Not a valid BMP file")

        # Extract pixel data offset from bytes 10–13 (little-endian)
        pixel_start = int.from_bytes(header_54[10:14], 'little')

        # Extract bits-per-pixel from bytes 28–29
        bits_per_pixel = int.from_bytes(header_54[28:30], 'little')

        # Move file pointer back to the start of the file
        bmp_file.seek(0)

        # Read all bytes up to the start of pixel data (header region)
        header_bytes = bmp_file.read(pixel_start)

        # Read the remaining bytes (pixel data) into a mutable bytearray
        pixel_bytes = bytearray(bmp_file.read())

    # Return header bytes, pixel bytes, pixel offset, and bits-per-pixel
    return header_bytes, pixel_bytes, pixel_start, bits_per_pixel


# Function to write a BMP header and pixel data to a new file
def write_bmp_header_and_pixels(output_bmp_image, header_bytes, pixels_modified):

    # Open the output BMP file in binary write mode
    with open(output_bmp_image, 'wb') as bmp_file:

        # Write original header bytes unchanged
        bmp_file.write(header_bytes)

        # Write modified pixel bytes (message embedded)
        bmp_file.write(pixels_modified)


# Convert a text message into a string of bits (0s and 1s)
def message_to_bits(message):

    # Start with an empty bit-string
    message_bits = ''

    # Loop through every character in the message
    for char in message:
        # Convert character to ASCII int, then to 8-bit binary string
        message_bits += format(ord(char), '08b')

    # Return full binary representation of message
    return message_bits


# Convert a string of bits back to text characters
def bits_to_message(bits_message):

    # Empty string to store the decoded characters
    message = ''

    # Loop through bits in steps of 8 (one byte per character)
    for bit_index in range(0, len(bits_message), 8):

        # Extract one 8-bit chunk
        eight_bits = bits_message[bit_index:bit_index+8]

        # Only convert if full 8 bits exist
        if len(eight_bits) == 8:
            # Convert binary to int → to character → add to message
            message += chr(int(eight_bits, 2))

    # Return decoded text
    return message


# Function to get pixel byte positions in RGB order instead of BGR
def bgr_to_rgb_reordered(num_pixel_bytes, bits_per_pixel):

    # List to store reordered byte indices
    rgb_reordered = []

    # Case for 24-bit BMP (3 bytes per pixel)
    if bits_per_pixel == 24:

        # Loop through pixel data in steps of 3
        for pixel_start in range(0, num_pixel_bytes, 3):

            # Ensure enough bytes for a full pixel
            if num_pixel_bytes - pixel_start >= 3:
                # Append R, G, B positions in RGB order
                rgb_reordered.append(pixel_start + 2)
                rgb_reordered.append(pixel_start + 1)
                rgb_reordered.append(pixel_start)

    # Case for 32-bit BMP (4 bytes per pixel)
    elif bits_per_pixel == 32:

        # Loop through pixel data in steps of 4
        for pixel_start in range(0, num_pixel_bytes, 4):

            # Ensure enough bytes for a full pixel
            if num_pixel_bytes - pixel_start >= 4:
                # Append R, G, B (ignore alpha)
                rgb_reordered.append(pixel_start + 2)
                rgb_reordered.append(pixel_start + 1)
                rgb_reordered.append(pixel_start)

    # Unsupported format
    else:
        # Raise error if bits-per-pixel is not 24 or 32
        raise ValueError(f"Unsupported bits-per-pixel: {bits_per_pixel}")

    # Return ordered byte positions
    return rgb_reordered


# Function to embed message bits into pixel bytes using LSB
def hide_bits_in_pixels(pixel_bytes, message_bits, bits_per_pixel):

    # Copy pixel bytes into a mutable bytearray
    pixels_modified = bytearray(pixel_bytes)

    # Get pixel byte positions in RGB order
    rgb_reordered = bgr_to_rgb_reordered(len(pixels_modified), bits_per_pixel)

    # Ensure the image has enough bytes to hide all message bits
    if len(message_bits) > len(rgb_reordered):
        raise ValueError("Message too long for this image (not enough pixels).")

    # Start at the first bit of the message
    bit_position = 0

    # Loop through pixel bytes in RGB order
    for byte_position in rgb_reordered:

        # Clear LSB of pixel byte, then set it to message bit
        pixels_modified[byte_position] = (pixels_modified[byte_position] & 254) | int(message_bits[bit_position])

        # Move to next message bit
        bit_position += 1

        # Stop when all bits are embedded
        if bit_position == len(message_bits):
            break

    # Return modified pixel array
    return pixels_modified


# Main function to hide message in a BMP image
def hide_message_in_bmp(input_bmp_image, message, output_bmp_image):

    # Use try/except to handle errors without crashing
    try:

        # Read header, pixels, offset, and bits-per-pixel
        header_bytes, pixel_bytes, pixel_start, bits_per_pixel = read_bmp_header_and_pixels(input_bmp_image)

        # Add delimiter to detect end of message during extraction
        message_with_delimiter = message + "###END###"

        # Convert message (with delimiter) to bits
        message_bits = message_to_bits(message_with_delimiter)

        # Embed bits into pixel bytes
        pixels_modified = hide_bits_in_pixels(pixel_bytes, message_bits, bits_per_pixel)

        # Write new BMP file with embedded message
        write_bmp_header_and_pixels(output_bmp_image, header_bytes, pixels_modified)

        # Print success information
        print(f"Message hidden successfully in {output_bmp_image}")
        print(f"Message length: {len(message)} characters ({len(message_bits)} bits)")
        print(f"BMP bits-per-pixel: {bits_per_pixel}")

    # Catch errors during hiding
    except Exception as error:
        print(f"Error hiding message: {error}")


# Function to extract hidden message from BMP image
def extract_message_from_bmp(output_bmp_image):

    # Use try/except to handle extraction errors
    try:

        # Read BMP header and pixel data
        header_bytes, pixel_bytes, pixel_start, bits_per_pixel = read_bmp_header_and_pixels(output_bmp_image)

        # Get pixel byte positions in RGB order
        rgb_reordered = bgr_to_rgb_reordered(len(pixel_bytes), bits_per_pixel)

        # Temporary collector for 8-bit sequences
        bits_collected = ""

        # String to accumulate recovered characters
        hidden_message = ""

        # Loop through pixel byte positions
        for byte_position in rgb_reordered:

            # Extract LSB of pixel byte and append to bits
            bits_collected += str(pixel_bytes[byte_position] & 1)

            # When we have 8 bits, decode them
            if len(bits_collected) == 8:

                # Convert 8-bit binary string to character
                hidden_message += chr(int(bits_collected, 2))

                # Reset bit collector
                bits_collected = ""

                # Check for end delimiter
                if hidden_message.endswith("###END###"):

                    # Remove delimiter (9 chars)
                    message = hidden_message[:-9]

                    # Print extraction info
                    print(f"Message extracted successfully: {len(message)} characters")
                    print(f"BMP bits-per-pixel: {bits_per_pixel}")

                    # Return decoded message
                    return message

        # If no delimiter found, no message embedded or corrupted
        print("No hidden message found or message corrupted")
        return None

    # Handle unexpected errors
    except Exception as error:
        print(f"Error extracting message: {error}")
        return None



# Main menu for the user interface
def main():

    # Display program title
    print("\n=== BMP Image Steganography ===")
    print("1. Hide message in image")
    print("2. Extract message from image")
    print("3. Exit")

    # Read user choice
    choice = input("\nEnter choice (1-3): ").strip()

    # Handle hide message option
    if choice == '1':

        # Ask for input BMP file path
        input_bmp_image = input("Enter input BMP image path: ").strip()

        # Ask for output BMP file path
        output_bmp_image = input("Enter output BMP image path: ").strip()

        # Ask how the message will be provided
        print("\nEnter message to hide:")
        print("1. Type message")
        print("2. Read from file")

        msg_choice = input("Choice (1-2): ").strip()

        # If user types the message manually
        if msg_choice == '1':
            message = input("Enter your secret message: ")

        # If user wants to read message from text file
        elif msg_choice == '2':
            file_input = input("Enter file path: ").strip()

            try:
                # Read message from file
                with open(file_input, 'r', encoding='utf-8') as file:
                    message = file.read()

            except Exception as error:
                # Print file read error
                print(f"Error reading file: {error}")
                return

        # If user enters invalid option
        else:
            print("Invalid choice")
            return

        # Hide the message in the BMP image
        hide_message_in_bmp(input_bmp_image, message, output_bmp_image)

    # Handle extract message option
    elif choice == '2':

        # Ask for BMP image containing hidden message
        output_bmp_image = input("Enter BMP image path (with hidden message): ").strip()

        # Extract hidden message
        message = extract_message_from_bmp(output_bmp_image)

        # If extraction successful
        if message:
            print("\n--- Hidden Message ---")
            print(message)
            print("----------------------")

            # Ask whether to save extracted message to file
            save = input("\nSave to file? (y/n): ").strip().lower()

            if save == 'y':
                output_file = input("Enter output file path: ").strip()

                try:
                    # Save message to file
                    with open(output_file, 'w', encoding='utf-8') as f:
                        f.write(message)

                    print(f"Message saved to {output_file}")

                except Exception as error:
                    # Print error if saving failed
                    print(f"Error saving file: {error}")

    # Exit option
    elif choice == '3':
        print("Exiting...")
        return

    # Invalid menu choice
    else:
        print("Invalid choice")



# Only run main loop if script is executed directly
if __name__ == "__main__":

    # Infinite loop to allow multiple operations
    while True:

        try:
            # Run main menu
            main()

            # Ask whether to continue using the program
            cont = input("\nContinue? (y/n): ").strip().lower()

            # If user chooses no → exit
            if cont != 'y':
                print("Goodbye!")
                break

        # Handle Ctrl+C interrupt
        except KeyboardInterrupt:
            print("\n\nExiting...")
            break
