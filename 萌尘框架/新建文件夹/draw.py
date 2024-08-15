from PIL import Image, ImageDraw, ImageFont, ImageFilter
import pygame
import io
import datetime
import os
import numpy as np

# Define constants
SCOREMAX = 10000
rankArray = [0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]  # Example values

def get_hour_word():
    now = datetime.datetime.now()
    return now.strftime("%H:%M")

def get_avatar(uid):
    # This function should fetch the avatar image by uid
    # Placeholder function
    return Image.open("avatar_placeholder.png")

def init_pic(picfile, uid):
    # This function should return avatar bytes and error
    return get_avatar(uid), None

def draw_score_16(a):
    picfile = a['picfile']
    uid = a['uid']
    nickname = a['nickname']
    score = a['score']
    inc = a['inc']
    level = a['level']
    rank = a['rank']

    avatar_img, err = init_pic(picfile, uid)
    if err:
        return None, err

    back = Image.open(picfile)
    back = back.resize((1280, 720), Image.LANCZOS)

    imgDX, imgDY = back.size
    canvas = Image.new('RGBA', (imgDX, imgDY), (255, 255, 255, 0))
    draw = ImageDraw.Draw(canvas)

    # Draw Aero Style
    aero_style = Image.new('RGBA', (imgDX-200, imgDY-200), (255, 255, 255, 0))
    aero_draw = ImageDraw.Draw(aero_style)
    aero_style = aero_style.filter(ImageFilter.GaussianBlur(2.5))
    aero_draw.rounded_rectangle([0, 0, imgDX-200, imgDY-200], radius=16, outline=(255, 255, 255, 100), fill=(255, 255, 255, 140))

    canvas.paste(back, (0, 0))
    canvas.paste(aero_style, (100, 100), aero_style)

    hour_word = get_hour_word()
    avatar_img = avatar_img.resize((200, 200), Image.LANCZOS)
    avatar_img = avatar_img.convert("RGBA")
    avatar_img = Image.new("RGBA", avatar_img.size, (255, 255, 255, 0))
    draw_avatar = ImageDraw.Draw(avatar_img)
    draw_avatar.ellipse([0, 0, 200, 200], fill=(255, 255, 255), outline=(0, 0, 0))

    canvas.paste(avatar_img, (120, 120), avatar_img)

    # Load fonts
    font_bold = ImageFont.truetype("BoldFontFile.ttf", 50)
    font_regular = ImageFont.truetype("FontFile.ttf", 30)

    draw.text((350, 180), nickname, font=font_bold, fill=(0, 0, 0))
    draw.text((350, 280), hour_word, font=font_regular, fill=(0, 0, 0))
    draw.text((350, 350), f"{wallet.get_wallet_name()} + {inc}", font=font_regular, fill=(0, 0, 0))
    draw.text((350, 400), f"当前{wallet.get_wallet_name()}：{score}", font=font_regular, fill=(0, 0, 0))
    draw.text((350, 450), f"LEVEL: {getrank(level)}", font=font_regular, fill=(0, 0, 0))

    get_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    draw.text((imgDX-100, imgDY-100), get_time, font=font_regular, fill=(0, 0, 0))

    nextrank_score = rankArray[rank + 1] if rank < 10 else SCOREMAX
    next_level_style = f"{level}/{nextrank_score}"
    draw.text((100, imgDY-100), next_level_style, font=font_regular, fill=(0, 0, 0))

    # Add gradient
    # This part might need a more complex approach to achieve similar results as the Go code

    draw.text((imgDX/2, imgDY-20), f"Created By Zerobot-Plugin {banner.VERSION}", font=font_regular, fill=(255, 255, 255))
    draw.text((imgDX/2 - 3, imgDY-19), f"Created By Zerobot-Plugin {banner.VERSION}", font=font_regular, fill=(0, 0, 0))

    return canvas, None

def draw_score_15(a):
    picfile = a['picfile']
    uid = a['uid']
    nickname = a['nickname']
    score = a['score']
    inc = a['inc']
    level = a['level']
    rank = a['rank']

    _, err = init_pic(picfile, uid)
    if err:
        return None, err

    back = Image.open(picfile)
    back = back.resize((1280, 720), Image.LANCZOS)
    canvas = Image.new('RGBA', (int(back.width), int(back.height * 1.7)), (255, 255, 255, 255))
    draw = ImageDraw.Draw(canvas)

    draw.paste(back, (0, 0))
    month_word = datetime.datetime.now().strftime("%m/%d")
    hour_word = get_hour_word()

    # Load fonts
    font_bold = ImageFont.truetype("BoldFontFile.ttf", back.width * 0.1)
    font_regular = ImageFont.truetype("FontFile.ttf", back.width * 0.04)

    draw.text((back.width * 0.1, back.height * 1.2), hour_word, font=font_bold, fill=(0, 0, 0))
    draw.text((back.width * 0.6, back.height * 1.2), month_word, font=font_bold, fill=(0, 0, 0))
    draw.text((back.width * 0.1, back.height * 1.3), f"{nickname} {wallet.get_wallet_name()}+{inc}", font=font_regular, fill=(0, 0, 0))
    draw.text((back.width * 0.1, back.height * 1.4), f"当前{wallet.get_wallet_name()}:{score}", font=font_regular, fill=(0, 0, 0))
    draw.text((back.width * 0.1, back.height * 1.5), f"LEVEL:{rank}", font=font_regular, fill=(0, 0, 0))

    # Draw rectangle and fill
    draw.rectangle([back.width * 0.1, back.height * 1.55, back.width * 0.6, back.height * 1.65], outline=(150, 150, 150), fill=(150, 150, 150))
    nextrank_score = rankArray[rank + 1] if rank < 10 else SCOREMAX
    draw.rectangle([back.width * 0.1, back.height * 1.55, back.width * 0.6 * (level / nextrank_score), back.height * 1.65], outline=(102, 102, 102), fill=(102, 102, 102))
    draw.text((back.width * 0.75, back.height * 1.62), f"{level}/{nextrank_score}", font=font_regular, fill=(0, 0, 0))

    return canvas, None

def draw_score_17(a):
    picfile = a['picfile']
    uid = a['uid']
    nickname = a['nickname']
    score = a['score']
    inc = a['inc']
    level = a['level']
    rank = a['rank']

    avatar_img, err = init_pic(picfile, uid)
    if err:
        return None, err

    back = Image.open(picfile)
    back = back.resize((1280, 720), Image.LANCZOS)
    imgDX, imgDY = back.size

    canvas = Image.new('RGBA', (imgDX, imgDY), (255, 255, 255, 255))
    draw = ImageDraw.Draw(canvas)

    # Draw background
    canvas.paste(back, (0, 0))

    # Draw Aero Style boxes
    def create_aero_box(x, y, width, height):
        aero_style = Image.new('RGBA', (int(width), int(height)), (255, 255, 255, 0))
        aero_draw = ImageDraw.Draw(aero_style)
        aero_draw.rounded_rectangle([0, 0, width, height], radius=8, outline=(255, 255, 255, 100), fill=(255, 255, 255, 140))
        return aero_style

    aero_box = create_aero_box(120, 60, imgDX - 240, imgDY - 120)
    canvas.paste(aero_box, (120, 60), aero_box)

    # Load fonts
    font_bold = ImageFont.truetype("BoldFontFile.ttf", 50)
    font_regular = ImageFont.truetype("FontFile.ttf", 30)

    draw.text((350, 60), nickname, font=font_bold, fill=(0, 0, 0))
    draw.text((350, 120), get_hour_word(), font=font_regular, fill=(0, 0, 0))
    draw.text((350, 180), f"{wallet.get_wallet_name()} + {inc}", font=font_regular, fill=(0, 0, 0))
    draw.text((350, 240), f"当前{wallet.get_wallet_name()}：{score}", font=font_regular, fill=(0, 0, 0))
    draw.text((350, 300), f"LEVEL: {getrank(level)}", font=font_regular, fill=(0, 0, 0))

    get_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    draw.text((imgDX - 100, imgDY - 100), get_time, font=font_regular, fill=(0, 0, 0))

    nextrank_score = rankArray[rank + 1] if rank < 10 else SCOREMAX
    next_level_style = f"{level}/{nextrank_score}"
    draw.text((120, imgDY - 100), next_level_style, font=font_regular, fill=(0, 0, 0))

    # Add gradient
    # This part might need a more complex approach to achieve similar results as the Go code

    draw.text((imgDX / 2, imgDY - 20), f"Created By Zerobot-Plugin {banner.VERSION}", font=font_regular, fill=(255, 255, 255))
    draw.text((imgDX / 2 - 3, imgDY - 19), f"Created By Zerobot-Plugin {banner.VERSION}", font=font_regular, fill=(0, 0, 0))

    return canvas, None

# Example usage
a = {
    'picfile': 'background_image.png',
    'uid': 123456,
    'nickname': 'PlayerName',
    'score': 1234,
    'inc': 56,
    'level': 3,
    'rank': 4
}

# Draw score 16
img, err = draw_score_16(a)
if img:
    img.show()

# Draw score 15
img, err = draw_score_15(a)
if img:
    img.show()

# Draw score 17
img, err = draw_score_17(a)
if img:
    img.show()
