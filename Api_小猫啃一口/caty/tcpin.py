from flask import Flask, request, send_file, jsonify
from PIL import Image, ImageDraw
import io
import requests
from requests.exceptions import RequestException

app = Flask(__name__)

def create_avatar_image(avatar_url, bg_image):
    try:
        # 获取头像图像
        avatar_response = requests.get(avatar_url)
        avatar_response.raise_for_status()  # 检查请求是否成功
        avatar_data = avatar_response.content
        avatar_image = Image.open(io.BytesIO(avatar_data))
    except RequestException as e:
        print(f"头像请求失败: {e}")
        return None
    except IOError as e:
        print(f"头像图像加载失败: {e}")
        return None

    # 将头像图片转换为 RGBA 模式
    avatar_image = avatar_image.convert('RGBA')

    # 调整头像大小
    avatar_width = int(bg_image.width * 0.286)
    avatar_height = int(bg_image.height * 0.286)
    avatar_image = avatar_image.resize((avatar_width, avatar_height))

    # 旋转头像
    avatar_image = avatar_image.rotate(30, expand=True)

    # 确定头像在背景图像上的位置
    avatar_position = (
        int(bg_image.width * 0.21) - 32,  # 向左移动 2 像素
        int(bg_image.height * 0.93) - avatar_image.height + 115  # 向下移动 30 像素
    )

    return avatar_image, avatar_position

def apply_background_and_avatar(bg_image, avatar_image, avatar_position):
    # 创建透明画布
    canvas = Image.new('RGBA', (bg_image.width, bg_image.height), (0, 0, 0, 0))

    # 先将头像图层粘贴到画布上
    canvas.paste(avatar_image, avatar_position, avatar_image)

    # 然后将背景图层粘贴到画布上
    canvas.paste(bg_image, (0, 0), bg_image)

    return canvas

def save_image(image):
    # 将合并后的图像保存到内存中的字节流
    byte_io = io.BytesIO()
    # 转换回 RGB 模式并保存为 JPEG
    image.convert('RGB').save(byte_io, 'JPEG')
    byte_io.seek(0)
    return byte_io

@app.route('/generate_image', methods=['GET'])
def generate_image():
    qq = request.args.get('qq')
    if not qq:
        return jsonify({"error": "Missing 'qq' parameter"}), 400

    # 加载背景图像
    bg_path = 'images/bg.png'
    try:
        bg_image = Image.open(bg_path).convert('RGBA')
    except IOError as e:
        print(f"背景图像加载失败: {e}")
        return jsonify({"error": "Failed to load background image"}), 500

    # 创建头像图像
    avatar_url = f'http://q.qlogo.cn/headimg_dl?dst_uin={qq}&spec=640&img_type=jpg'
    avatar_image, avatar_position = create_avatar_image(avatar_url, bg_image)

    if avatar_image:
        # 应用背景图像和头像图像
        combined_image = apply_background_and_avatar(bg_image, avatar_image, avatar_position)
        # 保存合成图像到内存中的字节流
        byte_io = save_image(combined_image)
        return send_file(byte_io, mimetype='image/jpeg', as_attachment=True, download_name='combined_image.jpg')
    else:
        return jsonify({"error": "Failed to create avatar image"}), 500

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port=8099)
