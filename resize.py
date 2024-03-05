from PIL import Image
import os

def resize_image(input_image_path, output_dir):
    # 确保输出目录存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 对目录中的每个文件进行操作
    for filename in os.listdir(input_image_path):
        if filename.lower().endswith(('png', 'jpg', 'jpeg')):
            file_path = os.path.join(input_image_path, filename)
            # 打开图像
            with Image.open(file_path) as img:
                # 获取图像的原始尺寸
                original_width, original_height = img.size
                
                # 计算新的尺寸
                new_width = original_width // 2
                new_height = original_height // 2
                
                # 调整图像大小
                resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                # 为调整大小后的图像构建输出路径
                output_file_path = os.path.join(output_dir, filename)
                
                # 保存调整大小后的图像
                resized_img.save(output_file_path)
                print(f"Image {filename} resized and saved to {output_file_path}")

if __name__ == "__main__":
    resize_input_path = '/home/stone/Desktop/preprocess_img/test_input'
    resize_output_dir = os.path.join(os.path.dirname(resize_input_path), 'resized_input')
    resize_image(resize_input_path, resize_output_dir)
