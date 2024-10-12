from PIL import Image, ImageDraw, ImageFont


def get_nb_letters_to_print_on_line(text: str, current_position: tuple[int, int], img_width: int, font: ImageFont) -> tuple[int, int]:
    max_size_printable = img_width - current_position[0]

    length_of_text = font.getbbox(text)[2]
    naive_length_by_char = length_of_text / len(text)

    if length_of_text <= max_size_printable:
        return len(text), length_of_text

    probable_split_position = int(max_size_printable // naive_length_by_char)
    length_of_text_before_split = font.getbbox(text[:probable_split_position])[2]
    
    while length_of_text_before_split <= max_size_printable:
        probable_split_position += 1
        length_of_text_before_split = font.getbbox(text[:probable_split_position])[2]
        
    while length_of_text_before_split > max_size_printable:
        probable_split_position -= 1
        length_of_text_before_split = font.getbbox(text[:probable_split_position])[2]
        

    return probable_split_position, font.getbbox(text[:probable_split_position])[2]
