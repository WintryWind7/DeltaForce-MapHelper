import cv2
import numpy as np
import os

# 输入文件路径
small_map_path = "../resource/testimg/testimg01.png"
large_map_path = "../resource/map/daba.jpg"
output_dir = "../resource/output/scaled_results"  # 输出文件目录

# 创建输出目录
os.makedirs(output_dir, exist_ok=True)

# 加载大地图和小地图
large_map = cv2.imread(large_map_path)
small_map = cv2.imread(small_map_path)

# 转为灰度图（模板匹配需要灰度图）
large_map_gray = cv2.cvtColor(large_map, cv2.COLOR_BGR2GRAY)
small_map_gray = cv2.cvtColor(small_map, cv2.COLOR_BGR2GRAY)

# 定义缩放比例范围（从 50% 到 150%，步长为 10%）
scale_factors = np.linspace(0.1, 1, 50)

# 遍历每种比例，执行模板匹配
results = []
for scale in scale_factors:
    # 缩放小地图
    resized_small_map = cv2.resize(small_map_gray, None, fx=scale, fy=scale, interpolation=cv2.INTER_LINEAR)
    h, w = resized_small_map.shape  # 获取缩放后模板的尺寸

    # 跳过超出大地图尺寸的模板
    if h > large_map_gray.shape[0] or w > large_map_gray.shape[1]:
        print(f"缩放比例 {scale:.2f} 超出大地图范围，跳过")
        continue

    # 模板匹配
    result = cv2.matchTemplate(large_map_gray, resized_small_map, cv2.TM_CCOEFF_NORMED)

    # 获取匹配结果中最大值及其位置
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # 记录结果
    results.append((scale, max_val, max_loc))

    # 在大地图上绘制匹配区域
    matched_image = large_map.copy()
    top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    cv2.rectangle(matched_image, top_left, bottom_right, (0, 255, 0), 3)

    # 保存每种比例下的匹配结果
    output_path = os.path.join(output_dir, f"scaled_result_{scale:.2f}.png")
    cv2.imwrite(output_path, matched_image)
    print(f"缩放比例 {scale:.2f} 匹配分数：{max_val:.4f}，结果保存为：{output_path}")

# 输出所有比例的结果
print("\n所有缩放比例下的匹配结果：")
for scale, max_val, max_loc in results:
    print(f"比例 {scale:.2f}：匹配分数 {max_val:.4f}，匹配位置 {max_loc}")
