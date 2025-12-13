# Convert each character of the message into its 8-bit binary representation
def message_to_bits(message):
    # Initialize an empty string to store the binary form of the message
    message_bits = ''
    # Loop through each character in the message
    for char in message:
        # Convert the character to its ASCII value, then to 8-bit binary, and append it
        message_bits += format(ord(char), '08b')
    # Return the full binary message
    return message_bits


# Convert a string of bits back into characters
def bits_to_message(bits_message):
    # Initialize an empty string to store the recovered characters
    message = ''
    # Loop through the bit string in steps of 8 bits
    for bit_index in range(0, len(bits_message), 8):
        # Extract 8 bits at a time
        eight_bits = bits_message[bit_index:bit_index+8]
        # Ensure the segment is exactly 8 bits before conversion
        if len(eight_bits) == 8:
            # Convert the 8-bit string back to a character and append it
            message += chr(int(eight_bits, 2))
    # Return the reconstructed message
    return message


# Reorder pixel byte positions from BGR to RGB for both 24-bit and 32-bit BMP formats
def bgr_to_rgb_reordered(num_pixel_bytes, bits_per_pixel):
    # Create a list to store reordered byte positions
    rgb_reordered = []

    # Handle 24-bit BMP pixels (3 bytes per pixel)
    if bits_per_pixel == 24:
        for pixel_start in range(0, num_pixel_bytes, 3):
            # Ensure 3 bytes remain before processing
            if num_pixel_bytes - pixel_start >= 3:
                # Append byte positions in RGB order
                rgb_reordered.append(pixel_start + 2)
                rgb_reordered.append(pixel_start + 1)
                rgb_reordered.append(pixel_start)

    # Handle 32-bit BMP pixels (4 bytes per pixel, ignoring alpha)
    elif bits_per_pixel == 32:
        for pixel_start in range(0, num_pixel_bytes, 4):
            # Ensure 4 bytes remain before processing
            if num_pixel_bytes - pixel_start >= 4:
                # Append only RGB bytes in correct order (skip alpha)
                rgb_reordered.append(pixel_start + 2)
                rgb_reordered.append(pixel_start + 1)
                rgb_reordered.append(pixel_start)

    # Unsupported bit depth is rejected
    else:
        raise ValueError(f"Unsupported bits-per-pixel: {bits_per_pixel}")

    # Return the complete list of reordered positions
    return rgb_reordered


# Insert message bits into pixel bytes using LSB substitution
def hide_bits_in_pixels(pixel_bytes, message_bits, bits_per_pixel):
    # Create a modifiable copy of the pixel data
    pixels_modified = bytearray(pixel_bytes)
    # Reorder pixel positions based on BMP bit depth
    rgb_reordered = bgr_to_rgb_reordered(len(pixels_modified), bits_per_pixel)

    # Check that the image has enough capacity for the message bits
    if len(message_bits) > len(rgb_reordered):
        raise ValueError("Message too long for this image (not enough pixels).")

    # Track which message bit is being written
    bit_position = 0

    # Loop through each pixel position where a bit will be embedded
    for byte_position in rgb_reordered:
        # Clear the LSB and insert the next message bit
        pixels_modified[byte_position] = (pixels_modified[byte_position] & 254) | int(message_bits[bit_position])
        # Move to the next bit in the message
        bit_position += 1
        # Stop once all bits have been embedded
        if bit_position == len(message_bits):
            break

    # Return the modified pixel bytes containing the hidden message
    return pixels_modified
