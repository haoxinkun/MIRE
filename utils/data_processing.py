#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件        :data_processing.py
@说明        :数据处理相关代码
@时间        :2024/12/17 16:39:44
@作者        :xinkun hao
@版本        :1.0
'''
import json

def add_path_prefix(prefix="data/mire/images_test1/", path="../LLaMA-Factory/data/mire/test1.json"):

    # 读取 JSON 文件
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 遍历每个对象，为 image 列表中的元素添加前缀
    for item in data:
        if "image" in item:
            item["image"] = [prefix + img for img in item["image"]]

    # 将修改后的数据写回文件
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print("前缀添加完成，结果已保存到 updated_data.json 文件中。")


import os
from PIL import Image

def process_large_images(folder_path, pixel_limit=89478485, output_folder=None):
    """
    遍历文件夹下的所有图片，找到像素值大于指定阈值的图片并降低其像素大小到阈值以下。
    
    :param folder_path: 输入的文件夹路径
    :param pixel_limit: 像素阈值，默认89478485
    :param output_folder: 输出文件夹路径，如果为空则覆盖原图
    """
    if output_folder and not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 遍历文件夹
    for root, _, files in os.walk(folder_path):
        for file in files:
            # 判断文件是否为图片
            if file.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp')):
                file_path = os.path.join(root, file)
                # print(file)
                try:
                    # 打开图片，获取尺寸
                    with Image.open(file_path) as img:
                        width, height = img.size
                        pixel_count = width * height
                        
                        # 如果像素值大于限制
                        if pixel_count > pixel_limit:
                            print(f"处理图片: {file_path}, 当前像素: {pixel_count}")
                            # # print(file_path)
                            # # 计算缩放比例
                            # scale_factor = (pixel_limit / pixel_count) ** 0.5
                            # new_width = int(width * scale_factor)
                            # new_height = int(height * scale_factor)
                            
                            # # 缩放图片
                            # img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                            
                            # # 保存图片
                            # if output_folder:
                            #     output_path = os.path.join(output_folder, os.path.relpath(file_path, folder_path))
                            #     os.makedirs(os.path.dirname(output_path), exist_ok=True)
                            #     img_resized.save(output_path)
                            # else:
                            #     img_resized.save(file_path)
                            # print(f"图片已压缩至: {new_width}x{new_height} = {new_width*new_height} 像素")
                except Exception as e:
                    print(f"无法处理文件 {file_path}，错误信息：{e}")

if  __name__ == "__main__":
    # 示例调用
    folder_path = "/Work/haoxinkun7091/MIRE/LLaMA-Factory/data/mire/images_train"  # 替换为你的图片文件夹路径
    output_folder = "/Work/haoxinkun7091/MIRE/LLaMA-Factory/data/mire/images_test1"  # 替换为输出文件夹路径，若覆盖原文件可设为 None
    process_large_images(folder_path, pixel_limit=12845056, output_folder=output_folder)





    # add_path_prefix()