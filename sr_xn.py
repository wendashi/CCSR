from inference_ccsr import main
from argparse import ArgumentParser, Namespace
from resize import resize_image
# from crop1_4 import crop
from combine4_1 import combine
import os
import yaml

def srxn(input_size, sr_xn, sr_input):
    # 基础配置
    sr_output = f'{sr_input}/srx{sr_xn}_output'
    args = create_args(sr_input, sr_output, sr_xn)

    if sr_xn == 2:
        sr_output = process_x2(args, sr_input, sr_output)
    elif sr_xn == 4:
        sr_output = process_x4(args, sr_input, sr_output, input_size)
    # elif sr_xn == 8:
    #     sr_output = process_x8(args, sr_input, sr_output, input_size)

    return sr_output

def create_args(sr_input, sr_output, sr_xn, config_path='/home/stone/Desktop/SR/CCSR1/CCSR/sx_xn.yml'):
    # 从YAML文件读取配置
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    
    # 更新从函数参数获取的值
    config['input'] = sr_input
    # config['sr_scale'] = sr_xn # 2 可以，4 可以
    config['output'] = sr_output

    # 将配置字典转换为Namespace对象
    args = Namespace(**config)
    return args

def process_x2(args, sr_input, sr_output):
    resize_output_dir = resize_and_set_args(args, sr_input, 'resized_input')
    # resize 到原来的 1/2
    args.input = resize_output_dir
    args.output = sr_output
    # x4 超分
    save_path = main(args)
    print('x2_result_path:', os.path.dirname(save_path))
    return save_path

def process_x4(args, sr_input, sr_output, input_size):
    args.input = sr_input
    args.output = sr_output
    # x4 超分
    save_path = main(args)
    print('x4_result_path:', os.path.dirname(save_path))
    return save_path

# def process_x4(args, sr_input, sr_output, input_size):
#     crop_output_dir = crop(sr_input)
#     args.input = crop_output_dir
#     args.output = os.path.join(sr_output, 'mid_x4')
#     save_path = main(args)
#     comb_output_dir = combine(os.path.dirname(save_path), input_size, 4)
#     print('x4_result_path:', comb_output_dir)
#     return comb_output_dir

# def process_x8(args, sr_input, sr_output, input_size):
#     resize_output_dir = resize_and_set_args(args, sr_input, 'resized_input')
#     mid_x8_path = main(args)
#     crop_output_dir = crop(os.path.dirname(mid_x8_path))
#     args.input = crop_output_dir
#     args.output = os.path.join(sr_output, 'mid_x8')
#     save_path = main(args)
#     comb_output_dir = combine(os.path.dirname(save_path), input_size, 8)
#     print('x8_result_path:', os.path.dirname(comb_output_dir))
#     return os.path.dirname(comb_output_dir)

def resize_and_set_args(args, input_path, output_subdir):
    output_dir = os.path.join(input_path, output_subdir)
    resize_image(input_path, output_dir)
    args.input = output_dir
    return output_dir

if __name__ == "__main__":
    sr_xn = 4 
    input_size = [200, 200]
    sr_input = '/home/stone/Desktop/SR/CCSR1/CCSR/preset/test-200'
    sr_output = srxn(input_size, sr_xn, sr_input)
