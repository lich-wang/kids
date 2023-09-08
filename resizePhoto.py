from PIL import Image
import os
import csv
import pandas as pd

def get_output_image_name(input_image_name, mappingfile="filename.xlsx"):
    """
    获取输出图片路径
    :param input_image_path: 输入图片路径
    :param mappingfile: xlsx文件，D列是输入图片路径，C列是输出图片路径
    :return: 输出图片路径
    """
    # 读取 Excel 文件
    df = pd.read_excel(mappingfile, engine='openpyxl')
    # 寻找匹配的输入图片名称
    matching_row = df[df['D'] == input_image_name]
    if not matching_row.empty:
        # 如果找到匹配项，返回对应的输出图片名称（C列）
        return matching_row.iloc[0]['C'] + '.jpg'
    # 如果没有找到匹配项，默认返回输入图片名称
    return input_image_name

def resize_image(input_image_path, output_image_path, max_file_size_kb=60, target_dpi=96):
    """
    根据目标文件大小动态调整图像分辨率
    :param input_image_path: 输入图片路径
    :param output_image_path: 输出图片路径
    :param max_file_size_kb: 最大目标文件大小（以KB为单位）
    :param target_dpi: 输出图片dpi
    :return:
    """
    
    # 打开输入图片
    img = Image.open(input_image_path)

    # 获取当前分辨率
    current_width, current_height = img.size

    # 计算目标文件大小（字节）
    target_file_size_bytes = max_file_size_kb * 1024

    # 动态调整分辨率，直到文件大小不超过目标大小
    while True:
        # 重新设置图像分辨率
        img = img.resize((current_width, current_height))
        
        # 保存为JPEG格式
        img.save(output_image_path, 'JPEG', dpi=(target_dpi, target_dpi))
        
        # 获取文件大小（字节）
        file_size = os.path.getsize(output_image_path)
        
        if file_size <= target_file_size_bytes or current_width <= 1 or current_height <= 1:
            # 如果文件大小不超过目标大小，或者分辨率已经很小，停止调整
            break
        
        # 动态降低分辨率，每次减小10%
        current_width = int(current_width * 0.9)
        current_height = int(current_height * 0.9)

    print(f"图片已保存为 {output_image_path}，文件大小为 {file_size / 1024:.2f}KB")


# 输入文件夹和输出文件夹的路径
input_folder = os.path.join(os.getcwd(), 'source')
output_folder = os.path.join(os.getcwd(), 'output')

# 确保输出文件夹存在
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 遍历输入文件夹中的所有文件
for filename in os.listdir(input_folder):
    print(f"正在处理图片 {filename}")
    input_image_path = os.path.join(input_folder, filename)
    output_image_name = get_output_image_name(filename)
    output_image_path = os.path.join(output_folder, output_image_name )
    print (f"正在处理图片 {input_image_path}，已保存为 {output_image_path}")
    resize_image(input_image_path, output_image_path)

print("所有图片已转换完成。")
