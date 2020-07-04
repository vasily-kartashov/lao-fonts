#!/usr/bin/env python3

from os import path, walk
from fontTools.ttLib import TTFont, TTLibError
from PIL import Image, ImageDraw, ImageFont

root_dir = path.dirname(path.realpath(__file__))
font_dir = path.join(root_dir, 'fonts')
spec_dir = path.join(root_dir, 'specimens')


def get_families():
    families = {}
    for (dir_path, dir_names, file_names) in walk(font_dir):
        for file_name in file_names:
            try:
                font_path = path.join(dir_path, file_name)
                font = TTFont(font_path)
                family = font['name'].names[1].string.decode("utf-8")
                style = font['name'].names[2].string.decode("utf-8")
                style_entry = {
                    'path': font_path,
                    'style': style,
                }
                families[family] = [style_entry]
            except TTLibError:
                print('Bad font %s' % file_name)
        for dir_name in dir_names:
            for (dir_path, _, file_names) in walk(dir_name):
                for file_name in file_names:
                    font_path = path.join(dir_path, file_name)
                    font = TTFont(font_path)
                    family = font['name'].names[1].string.decode("utf-8")
                    style = font['name'].names[2].string.decode("utf-8")
                    style_entry = {
                        'path': font_path,
                        'style': style
                    }
                    if families[family]:
                        families[family].append(style_entry)
                    else:
                        families[family] = [style_entry]
    return families


with open(path.join(root_dir, 'example.txt'), 'r') as file:
    lines = file.readlines()


def prepare_specimen(family, styles):
    print('Specimen for %s' % family)
    word = "ນ້ຳ ຟ້າ ສາສະໜາ ພາສາ ສະຫຼາມ ຊຳນານ ກະແລັມ ແວງ ຄຸກກີ້"

    files = []
    for style in styles:
        font = style['path']
        txt = Image.new('RGBA', (220, 350), (255, 255, 255, 255))
        d = ImageDraw.Draw(txt)
        d.rectangle([(0, 1600), (220, 350)], (255, 127, 42, 255))

        fnt = ImageFont.truetype('Roboto-Regular', 10)
        title = family + " (" + style['style'] + ")"
        d.text((10, 8), title, font=fnt, fill=(0, 0, 0, 255))

        fnt = ImageFont.truetype(font, 170)
        d.text((10,  35), lines[0], font=fnt, fill=(0, 125, 0, 255))
        d.text((10,  65), lines[1], font=fnt, fill=(0, 0, 255, 255))
        d.text((10,  95), lines[2], font=fnt, fill=(255, 0, 0, 255))
        d.text((10, 125), lines[3], font=fnt, fill=(0, 0, 0, 255))

        fnt = ImageFont.truetype(font, 12)
        offset = 0
        for line in lines[4:]:
            d.text((10, 165 + offset), line, font=fnt, fill=(0, 0, 0, 255))
            offset += 20
        output = path.join(spec_dir, family + '.png')
        try:
            txt.save(output)
            files.append([title, 'specimens/' + family + '.png'])
        except ValueError:
            print("Cannot store %s" % title)
    return files


if __name__ == '__main__':
    content = 'Lao Fonts\n'
    content += "===\n\n"
    content += "All examples for http://laofonts.tripod.com/index.htm. Copyright unknown.\n\n"
    for family, styles in get_families().items():
        for file in prepare_specimen(family, styles):
            content += '![' + file[0] + '](' + file[1] + ' "' + file[0] + '")\n\n'
    with open('README.md', 'w') as file:
        file.write(content)