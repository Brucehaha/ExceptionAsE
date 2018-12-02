import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter


_letter_cases = "abcdefghjkmnpqrstuvwxy"  # 小写字母，去除可能干扰的i，l，o，z
_upper_cases = _letter_cases.upper()  # 大写字母
_numbers = ''.join(map(str, range(3, 10)))  # 数字
init_chars = ''.join((_letter_cases, _upper_cases, _numbers))

# PIL
def recaptcha(size=(120, 30),
                         chars=init_chars,
                         img_type="GIF",
                         mode="RGB",
                         bg_color=(255, 255, 255),
                         fg_color=(0, 0, 255),
                         font_size=18,
                         font_type="Monaco.ttf",
                         length=4,
                         draw_lines=True,
                         n_line=(1, 2),
                         draw_points=True,
                         point_chance=2):
    """
    @todo: generate code with photo
    @param size: photo size，dimension（width, height）defualt(120, 30)
    @param chars: allowed characters
    @param img_type: image type, defualt, GIF, available GIF，JPEG，TIFF，PNG
    @param mode: default RGB
    @param bg_color: background color, default white
    @param fg_color: front color, color of code in fort，default blue #0000FF
    @param font_size: code size
    @param font_type: code font family, defualt ae_AlArabiya.ttf
    @param length: code length
    @param draw_lines: if lines required
    @param n_lines: no. of lines, tuple default(1, 2)，draw_lines must beTrue
    @param draw_points: if dot required default true
    @param point_chance: the frequency of dots shows, [0, 100]
    @return: [0]: PIL Image instance
    @return: [1]: code on the photo
    """

    width, height = size  # w h
    # create image
    img = Image.new(mode, size, bg_color)
    draw = ImageDraw.Draw(img)  # create a pen

    def get_chars():
        """generate a certain length code from chars"""
        return random.sample(chars, length)

    def create_lines():
        """ draw lines for interference"""
        line_num = random.randint(*n_line)  # no. of interferential line

        for i in range(line_num):
            # start
            begin = (random.randint(0, size[0]), random.randint(0, size[1]))
            # end
            end = (random.randint(0, size[0]), random.randint(0, size[1]))
            draw.line([begin, end], fill=(0, 0, 0))

    def create_points():
        """draw interferential dots"""
        chance = min(100, max(0, int(point_chance)))  # between [0, 100]

        for w in range(width):
            for h in range(height):
                tmp = random.randint(0, 100)
                if tmp > 100 - chance:
                    draw.point((w, h), fill=(0, 0, 0))

    def create_strs():
        """draw code"""
        c_chars = get_chars()
        strs = ' %s ' % ' '.join(c_chars)  # code is seperate with space

        font = ImageFont.truetype(font_type, font_size)
        font_width, font_height = font.getsize(strs)

        draw.text(((width - font_width) / 3, (height - font_height) / 3),
                  strs, font=font, fill=fg_color)

        return ''.join(c_chars)

    if draw_lines:
        create_lines()
    if draw_points:
        create_points()
    strs = create_strs()

    # twist the picture
    params = [1 - float(random.randint(1, 2)) / 100,
              0,
              0,
              0,
              1 - float(random.randint(1, 10)) / 100,
              float(random.randint(1, 2)) / 500,
              0.001,
              float(random.randint(1, 2)) / 500
              ]
    img = img.transform(size, Image.PERSPECTIVE, params)  # 创建扭曲

    img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)  # 滤镜，边界加强（阈值更大）

    return img, strs

