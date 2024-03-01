from inference_ccsr import main
from argparse import ArgumentParser, Namespace
from resize import resize_image
# from crop1_4 import crop
# from combine4_1 import combine
import os

xn = 8 # 2 or 4 or 8  超分倍数
sr_input = '/home/stone/Desktop/SR/CCSR1/CCSR/preset/test_datasets'
sr_output = '/home/stone/Desktop/SR/CCSR1/CCSR/experiments/srx8_output' # sr 最终结果

# 中间结果保存位置
# sr_output_x4 = '/home/stone/Desktop/SR/CCSR1/CCSR/experiments/srx4_output/mid' # x4的中间图像保存位置
sr_output_x8 = '/home/stone/Desktop/SR/CCSR1/CCSR/experiments/srx8_output/mid' # x8的中间图像保存位置

def parse_args() -> Namespace:
    parser = ArgumentParser()

    parser.add_argument("--ckpt", type=str, help="full checkpoint path", default='/home/stone/Desktop/SR/CCSR1/CCSR/pre-trained-models/real-world_ccsr.ckpt')
    parser.add_argument("--config", type=str, help="model config path", default='configs/model/ccsr_stage2.yaml')

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

if xn == 2:
    args = parse_args()
    resize_input_path = sr_input
    resize_output_dir = os.path.join(resize_input_path, 'resized_input')
    resize_image(resize_input_path,resize_output_dir)
    args.input = resize_output_dir
    args.output = sr_output

    # 调用超分
    main(args)  

elif xn == 4:
    args = parse_args()

    args.input = sr_input
    args.output = sr_output
    # 调用超分
    main(args) 

elif xn == 8:
    args = parse_args()
    resize_input_path = sr_input
    resize_output_dir = os.path.join(resize_input_path, 'resized_input')
    resize_image(resize_input_path,resize_output_dir)
    args.input = resize_output_dir
    args.output = sr_output_x8

    # 调用超分
    save_path = main(args)  
    # print(save_path) # /home/stone/Desktop/SR/CCSR1/CCSR/experiments/srx8_output/mid/512.png

    args = parse_args()

    args.input = os.path.dirname(save_path)
    args.output = sr_output
    # 调用超分
    main(args) 









