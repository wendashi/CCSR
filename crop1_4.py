import os
from PIL import Image

def crop_and_save_image(img, crop_area, output_path):
    """裁剪图像并保存到指定路径"""
    cropped_img = img.crop(crop_area)
    cropped_img.save(output_path)

def crop(crop_input_dir):
    crop_output_dir = os.path.join(crop_input_dir, f'cropped_input')

    # 确保输出目录存在
    os.makedirs(crop_output_dir, exist_ok=True)

    for filename in os.listdir(crop_input_dir):
        if filename.lower().endswith(('png', 'jpg', 'jpeg')):
            basename, ext = os.path.splitext(filename)
            img_path = os.path.join(crop_input_dir, filename)
            img = Image.open(img_path)
            width, height = img.size

            # 定义裁剪区域
            crop_areas = [
                (0, 0, width // 2, height // 2),  # 左上角
                (width // 2, 0, width, height // 2),  # 右上角
                (0, height // 2, width // 2, height),  # 左下角
                (width // 2, height // 2, width, height)  # 右下角
            ]

            # 裁剪并保存图像
            for i, crop_area in enumerate(crop_areas, start=1):
                output_filename = f'{basename}-{i}{ext}'
                output_path = os.path.join(crop_output_dir, output_filename)
                crop_and_save_image(img, crop_area, output_path)

    return crop_output_dir

if __name__ == "__main__":
    crop_input_dir = '/home/stone/Desktop/preprocess_img/test_input'
    crop_output_sir = crop(crop_input_dir)
