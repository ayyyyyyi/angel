# -*- coding: utf-8 -*-
"""
抠图后处理工具集：
1. 挖翅膀之间的云（孔洞填充的反向用法：把翅膀内部被误判成主体的"洞"填回透明）
2. 裁掉顶部横梁
用法: python postprocess.py <输入透明PNG> <输出透明PNG>
"""
import sys
import numpy as np
from PIL import Image
from scipy import ndimage

def find_holes_and_clear(angel_mask_path: str, out_path: str):
    """
    1. 找天使主体（最大连通分量）
    2. 用 binary_fill_holes 得到"应有轮廓"（实心的完整天使）
    3. 差集就是"翅膀之间被 AI 误判成主体的云"——把它填回透明
    """
    img = Image.open(angel_mask_path).convert("RGBA")
    arr = np.array(img)
    alpha = arr[:, :, 3]
    h, w = alpha.shape

    # 阈值二值化：>30 视为主体
    mask = alpha > 30

    # 找所有连通分量
    labels, n = ndimage.label(mask)
    if n == 0:
        print("没找到主体，跳过")
        return

    # 找最大连通分量（天使）
    sizes = ndimage.sum(mask, labels, range(1, n + 1))
    angel_label = int(np.argmax(sizes)) + 1
    angel_mask = (labels == angel_label)

    # 主体像素数
    angel_size = angel_mask.sum()

    # 用 binary_fill_holes 填主体内部的洞
    # 注意：这里 angel_mask 已经包含了"翅膀之间的云"，所以 binary_fill_holes 不会消除它们
    # 差异：angel_mask 是"AI 认为的主体"，filled 是"应有轮廓"
    # filled - angel_mask = 应有但 AI 没抠到的（极少，主要在外面）
    # angel_mask - filled = AI 抠多了的（翅膀之间的云 ← 这是我们要消除的）

    # 但 angel_mask 整体已经被翅膀包围，飞鸟形状，binary_fill_holes 不会有差异
    # 换个思路：找 angel_mask 的"凸包"，再和 angel_mask 比
    # 凸包一定包含翅膀之间的云（因为云在翅膀内部），所以凸包差集就是云的补集

    # 实际上更直接：angel_mask 内部的"洞"——alpha=0 但被 angel_mask 包围的区域（但我们没排除 clouds）
    # 所以需要换一种思路

    # 最简方案：直接用 ndimage.binary_fill_holes 反过来用
    # 先做 morphological closing 让翅膀合拢，把中间的云也包进去
    # 然后 subtract 出 angel_mask 没有覆盖到的"外部"区域
    # 那"内部"区域就是翅膀之间的云

    # 终极简单方案：找 angel_mask 的"凸包 hull"，减去 angel_mask
    # 凸包 = 翅膀合拢后整个外轮廓（飞鸟形状）
    # 差集 = 翅膀合拢后中间的"洞"区域
    # 这个"洞"区域恰好就是"翅膀中间的云"所在
    # 把这个区域的 alpha 强制设为 0

    # 用 OpenCV 做凸包
    try:
        import cv2
        # PIL 转 cv2
        binary = angel_mask.astype(np.uint8) * 255
        # 找轮廓
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            print("没找到轮廓，跳过")
            return
        # 取最大轮廓
        biggest = max(contours, key=cv2.contourArea)
        # 凸包
        hull = cv2.convexHull(biggest)
        # 画凸包成 mask
        hull_mask = np.zeros_like(angel_mask)
        cv2.fillConvexPoly(hull_mask, hull, 1)
        hull_mask = hull_mask.astype(bool)
    except ImportError:
        # 没 OpenCV，降级方案：纯 scipy
        print("OpenCV 不可用，用 scipy 兜底")
        # scipy 的 convex hull 不直接支持 2D image
        # 用 ndimage.binary_fill_holes 的反向思路
        # 把 angel_mask 的"补集"做连通标记，找最大连通分量是"外部"
        # 但 wings 围起来的小洞不算外部
        # 跳过这步，直接给出原图
        hull_mask = angel_mask

    # 凸包减去 angel_mask = 翅膀合拢后"新覆盖"的区域 = 应填回透明的翅膀之间的云
    holes_inside_hull = hull_mask & ~angel_mask
    # 但 holes_inside_hull 也包括翅膀外侧的区域（凸包比主体大）
    # 进一步过滤：要求这些区域在主体 bounding box 内
    ys, xs = np.where(angel_mask)
    if len(xs):
        bbox_x = (xs.min(), xs.max())
        bbox_y = (ys.min(), ys.max())
        # 排除 bounding box 外的（这些是"翅膀外侧补全的洞"）
        yy_grid, xx_grid = np.meshgrid(
            np.arange(h), np.arange(w), indexing='ij'
        )
        in_bbox = (
            (xx_grid >= bbox_x[0]) & (xx_grid <= bbox_x[1]) &
            (yy_grid >= bbox_y[0]) & (yy_grid <= bbox_y[1])
        )
        holes_inside_hull = holes_inside_hull & in_bbox

    # 把这些区域的 alpha 强制设为 0
    new_alpha = alpha.copy()
    new_alpha[holes_inside_hull] = 0

    # 顺手把 bounding box 外的、误判的"主体"也设为 0（保险）
    in_angel_bbox = np.zeros_like(mask)
    in_angel_bbox[bbox_y[0]:bbox_y[1]+1, bbox_x[0]:bbox_x[1]+1] = True
    # 不强制，看效果

    arr[:, :, 3] = new_alpha
    Image.fromarray(arr, "RGBA").save(out_path)

    print(f"挖掉 {int(holes_inside_hull.sum())} 个像素 ({holes_inside_hull.sum()/h/w*100:.2f}%) 来自翅膀之间的云区域")
    print(f"原主体像素: {angel_size} ({angel_size/h/w*100:.2f}%)")
    print(f"已保存: {out_path}")


def crop_top(src: str, out: str, ratio: float = 0.03):
    """裁掉顶部 X% 的像素（默认 3%，足以去掉拱门横梁）"""
    img = Image.open(src)
    w, h = img.size
    top = int(h * ratio)
    # 透明底图，裁后保留透明
    cropped = img.crop((0, top, w, h))
    cropped.save(out)
    print(f"裁掉顶部 {top}px ({ratio*100:.1f}%)：{src} -> {out}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法: python postprocess.py <输入透明PNG> <输出透明PNG> [--crop N]")
        sys.exit(1)
    inp, outp = sys.argv[1], sys.argv[2]

    # 可选 --crop 0.03 裁顶部 3%
    crop_ratio = 0.03
    args = sys.argv[3:]
    if "--crop" in args:
        idx = args.index("--crop")
        crop_ratio = float(args[idx + 1])
        print(f"将裁顶部 {crop_ratio*100:.1f}%")

    print(f"[1/2] 挖翅膀之间的云: {inp}")
    step_out = inp.replace(".png", "_step1_holes.png")
    find_holes_and_clear(inp, step_out)

    print(f"[2/2] 裁顶部 {crop_ratio*100:.1f}%")
    crop_top(step_out, outp, crop_ratio)
