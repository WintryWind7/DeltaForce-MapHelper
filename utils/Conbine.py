import os
from PIL import Image

# 本地图片目录（包含 3_3_2.jpg 格式的图片）
input_dir = "../resource/origin"  # 替换为你的图片目录
output_dir = "../resource/map"
os.makedirs(output_dir, exist_ok=True)

# 裁剪边缘，使用上下左右裁剪变量
crop_top = 4  # 裁剪顶部2个图片高度
crop_bottom = 4  # 裁剪底部2个图片高度
crop_left = 1  # 裁剪左侧2个图片宽度
crop_right = 1  # 裁剪右侧2个图片宽度

# 读取目录下所有图片
files = [f for f in os.listdir(input_dir) if f.endswith('.jpg')]

# 创建一个字典来存储图片路径，根据行列号组织
image_map = {}
max_row = max_col = 0

for file in files:
    try:
        # 提取文件名中的行、列信息
        base_name = os.path.splitext(file)[0]
        _, col, row = map(int, base_name.split('_'))  # 假设文件名格式固定为 "行_列_序号.jpg"
        max_row = max(max_row, row)  # 获取最大行号
        max_col = max(max_col, col)  # 获取最大列号
        image_map[(row, col)] = os.path.join(input_dir, file)  # 将图片路径存入字典
    except ValueError:
        print(f"跳过无效文件名: {file}")

# 打开示例图片以获取每个图片的尺寸
sample_image = Image.open(next(iter(image_map.values())))  # 打开一个示例图片
image_width, image_height = sample_image.size

# 计算拼接后图片的总尺寸（根据最大行和列计算）
total_width = image_width * max_col
total_height = image_height * max_row

# 创建一个空白图片用于拼接
result_image = Image.new("RGB", (total_width, total_height))

# 按照行列号将图片放到正确位置
for row in range(1, max_row + 1):  # 遍历所有行
    for col in range(1, max_col + 1):  # 遍历所有列
        if (row, col) in image_map:
            img_path = image_map[(row, col)]
            img = Image.open(img_path)
            # 根据行列号计算放置的位置
            x_offset = (col - 1) * image_width  # 列决定 x 方向
            y_offset = (row - 1) * image_height  # 行决定 y 方向
            result_image.paste(img, (x_offset, y_offset))
        else:
            # 如果图片不存在，可以选择跳过或用空白填充
            placeholder = Image.new("RGB", (image_width, image_height), color=(255, 255, 255))
            x_offset = (col - 1) * image_width
            y_offset = (row - 1) * image_height
            result_image.paste(placeholder, (x_offset, y_offset))


# 计算裁剪距离
crop_top_height = crop_top * image_height
crop_bottom_height = crop_bottom * image_height
crop_left_width = crop_left * image_width
crop_right_width = crop_right * image_width

# 计算裁剪后的区域
left = crop_left_width
top = crop_top_height
right = total_width - crop_right_width
bottom = total_height - crop_bottom_height

# 执行裁剪
result_image = result_image.crop((left, top, right, bottom))

# 保存裁剪后的图片
output_path = os.path.join(output_dir, "stitched_image_cropped.jpg")
result_image.save(output_path)
print(f"拼接并裁剪完成，图片保存到: {output_path}")
