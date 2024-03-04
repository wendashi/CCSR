import os
from PIL import Image
import time

def combine_images(input_dir, output_dir, filename, input_size, sr_xn):
    """Combine four parts of images into one."""
    basename, ext = os.path.splitext(filename)
    original_basename = basename[:-2]

    # 打开图像
    img1 = Image.open(os.path.join(input_dir, f'{original_basename}-1{ext}'))
    img2 = Image.open(os.path.join(input_dir, f'{original_basename}-2{ext}'))
    img3 = Image.open(os.path.join(input_dir, f'{original_basename}-3{ext}'))
    img4 = Image.open(os.path.join(input_dir, f'{original_basename}-4{ext}'))

    # 计算输出图像的尺寸
    output_width, output_height = [size * sr_xn for size in input_size]

    # 创建一个新的空白图像，大小为原图x倍数（input_size*sr_xn）
    new_img = Image.new('RGB', (output_width, output_height))

    width, height = img1.size
    # 将四个图像粘贴到新的图像上（按照四个角的点来贴！）
    new_img.paste(img1, (0, 0))
    new_img.paste(img2, (output_width - width, 0))
    new_img.paste(img3, (0, output_height - height))
    new_img.paste(img4, (output_width - width, output_height - height))
    # new_img.paste(img1, (0, 0))
    # new_img.paste(img2, (width, 0))
    # new_img.paste(img3, (0, height))
    # new_img.paste(img4, (width, height))

    # 保存新的图像
    new_img.save(os.path.join(output_dir, f'{original_basename}{ext}'))

def combine(input_dir, input_size, sr_xn):
    output_dir = os.path.join(os.path.dirname(input_dir), 'combined_input')
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(input_dir):

        if filename.lower().endswith(('png', 'jpg', 'jpeg')):
            combine_images(input_dir, output_dir, filename, input_size, sr_xn)
                
    return output_dir

if __name__ == "__main__":
    comb_input_dir = '/home/stone/Desktop/preprocess_img/test_input_x2'
    input_size = [512, 512]
    sr_xn = 4 
    comb_output_dir = combine(comb_input_dir, input_size, sr_xn)
