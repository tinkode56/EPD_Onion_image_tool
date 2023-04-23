from colorsys import rgb_to_hsv
from PIL import Image

# Colors:
# 		0x00 - black (2 pixels)
# 		0x33 - white (2 pixels)
# 		0x44 - red (2 pixels)


def determine_pixel_output(pixel):
    if pixel[0] > 80 and pixel[1] < 180 and pixel[2] < 180:
        return (255, 0, 0)
    else:
        return (255, 255, 255)


def calculate_pixel(pixel_black1, pixel_red1, pixel_black2, pixel_red2):
    double_pixel = 0x00

    # if pixel red, let it be, do not overwrite
    # otherwise it is not shown on epd (BLACK > RED)

    if pixel_black1 > 128:
        double_pixel = double_pixel | 0x30
    else:
        if pixel_red1 == (255, 0, 0):
            double_pixel = double_pixel | 0x40
        else:
            double_pixel = double_pixel | 0x00

    if pixel_black2 > 128:
        double_pixel = double_pixel | 0x03
    else:
        if pixel_red2 == (255, 0, 0):
            double_pixel = double_pixel | 0x04
        else:
            double_pixel = double_pixel | 0x00

    # if pixel_red1 == (255, 0, 0):
    #     double_pixel = (double_pixel & 0x0F) | 0x40
    # else:
    #     double_pixel = double_pixel | 0x00
    #
    # if pixel_red2 == (255, 0, 0):
    #     double_pixel = (double_pixel & 0xF0) | 0x04
    # else:
    #     double_pixel = double_pixel | 0x00

    return double_pixel


image = Image.open("out_color.jpg")
dithered_image = Image.open("out_gray.jpg")

pixels = image.load()
dithered_pixels = dithered_image.load()

print(image.size)
print(pixels[0, 0])
print(dithered_pixels[0, 0])

print(image.size[0])

with open('image.h', 'w') as f:
    binary = open('image.bin', 'wb')
    f.write("static const uint8_t epd_75_image [] = {\n")
    for y in range(image.size[1]):
        for x in range(0, image.size[0], 2):
            r1 = determine_pixel_output(pixels[x, y])
            r2 = determine_pixel_output(pixels[x+1, y])
            byte_value = calculate_pixel(dithered_pixels[x, y], r1,  dithered_pixels[x+1, y], r2)
            f.write(hex(byte_value) + ", ")
            binary.write(byte_value.to_bytes(1, 'big'))
        f.write("\n")
    f.write("};\n")
    binary.close()
