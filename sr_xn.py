from inference_ccsr import main
from argparse import ArgumentParser, Namespace
from resize import resize_image
from crop1_4 import crop
from combine4_1 import combine
import os

# 输入图像的尺寸 [宽，高]
input_size = [512, 512] 
# 超分倍数（2 or 4 or 8  ）
sr_xn = 8 
# 超分输入图片所在路径
sr_input = '/home/stone/Desktop/SR/CCSR1/CCSR/preset/test-512'
# 超分输出图片路径（sr 最终结果）
sr_output = f'/home/stone/Desktop/SR/CCSR1/CCSR/experiments/sr{sr_xn}_output' 
# 中间结果保存位置（sr 中间结果，x4和x8才有中间结果）
if sr_xn == 4:
    sr_mid_xn = os.path.join(sr_output, 'mid_x4')   
elif sr_xn == 8:
    sr_mid_xn = os.path.join(sr_output,'mid_x8')
    sr_mid_xn1 = os.path.join(sr_output,'mid_x8_1')

def parse_args() -> Namespace:
    parser = ArgumentParser()

    parser.add_argument("--ckpt", type=str, help="full checkpoint path", default='/home/stone/Desktop/SR/CCSR1/CCSR/pre-trained-models/real-world_ccsr.ckpt')

    # 这个位置注意是 ccsr_stage2.yaml 
    parser.add_argument("--config", type=str, help="model config path", default='/home/stone/Desktop/SR/CCSR1/CCSR/configs/model/ccsr_stage2.yaml')

    parser.add_argument("--input", type=str, default='preprocess_img/input_x2')
    parser.add_argument("--steps", type=int, default=45)
    parser.add_argument("--sr_scale", type=float, default=4)
    parser.add_argument("--repeat_times", type=int, default=1)

    # patch-based sampling (tiling settings)
    parser.add_argument("--tiled", action="store_true")
    parser.add_argument("--tile_size", type=int, default=512)  # image size
    parser.add_argument("--tile_stride", type=int, default=256)  # image size

    parser.add_argument("--color_fix_type", type=str, default="adain", choices=["wavelet", "adain", "none"])
    parser.add_argument("--output", type=str, default="experiments/test")
    parser.add_argument("--t_max", type=float, default=0.6667)
    parser.add_argument("--t_min", type=float, default=0.3333)
    parser.add_argument("--show_lq", action="store_true")
    parser.add_argument("--skip_if_exist", action="store_true")

    parser.add_argument("--seed", type=int, default=233)
    parser.add_argument("--device", type=str, default="cuda", choices=["cpu", "cuda", "mps"])

    return parser.parse_args()

if sr_xn == 2:
    # 先 resize（//2）再超分（x4）
    args = parse_args()
    resize_input_path = sr_input
    resize_output_dir = os.path.join(resize_input_path, 'resized_input')
    resize_image(resize_input_path,resize_output_dir)
    args.input = resize_output_dir
    args.output = sr_output

    # 调用超分
    save_path = main(args)  
    x2_result_path = os.path.dirname(save_path)
    print('x2_result_path:', x2_result_path)

elif sr_xn == 4:
    # 先 crop 成 4 张，分别超分（x4），再 combine 到一起
    args = parse_args()
    crop_input_dir = sr_input
    crop_output_sir = crop(crop_input_dir)

    args.input = crop_output_sir
    args.output = sr_mid_xn
    # 调用超分
    save_path = main(args) 
    comb_input_dir = os.path.dirname(save_path)
    
    comb_output_dir = combine(comb_input_dir, input_size, sr_xn)

    print('x4_result_path:', comb_output_dir)


elif sr_xn == 8:
    # 先 x2
    args = parse_args()
    resize_input_path = sr_input
    resize_output_dir = os.path.join(resize_input_path, 'resized_input')
    resize_image(resize_input_path, resize_output_dir)
    args.input = resize_output_dir
    args.output = sr_mid_xn

    # 调用超分
    save_path = main(args)  
    x2_result_path = os.path.dirname(save_path)

    # 如果要进一个循环的话，这个 crop 得是整的（不能用重叠？）
    crop_input_dir = x2_result_path
    crop_output_sir = crop(crop_input_dir)

    # 再 x4 
    # for crop_input_dir1 = crop_output_sir
    #     crop_output_sir1 = crop(crop_input_dir1)

    #     args.input = crop_output_sir1
    #     args.output = sr_mid_xn
    #     # 调用超分
    #     save_path1 = main(args) 
    #     comb_input_dir = os.path.dirname(save_path1)

    args.input = crop_output_sir
    args.output = sr_mid_xn1
    # 调用超分
    save_path1 = main(args) 
    comb_input_dir = os.path.dirname(save_path1)

    comb_output_dir = combine(comb_input_dir, input_size, sr_xn)

    print('x8_result_path:', os.path.dirname(comb_output_dir))