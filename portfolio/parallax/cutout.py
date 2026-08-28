# -*- coding: utf-8 -*-
"""
用 rembg 抠图脚本（AI 抠主体 → 透明底 PNG）
用法: python cutout.py <输入图> <输出图> [模型名]
模型名可选: u2net(默认,快) / isnet-general-use(更准,写实主体推荐)
"""
import sys
from PIL import Image
from rembg import remove, new_session

def main():
    if len(sys.argv) < 3:
        print("用法: python cutout.py 输入图 输出图 [模型名]")
        return

    inp = sys.argv[1]
    outp = sys.argv[2]
    model = sys.argv[3] if len(sys.argv) > 3 else "isnet-general-use"

    print(f"[1/3] 读取图片: {inp}")
    img = Image.open(inp).convert("RGB")
    print(f"      尺寸 {img.size}")

    print(f"[2/3] 加载模型 {model} ...（首次会下载模型，稍等）")
    session = new_session(model)

    print("[3/3] AI 抠图中 ...")
    # alpha_matting=True 会再做一次边缘细化（grabcut 风格），
    # 对羽毛、薄纱这种半透明边缘更准。
    out = remove(
        img,
        session=session,
        alpha_matting=True,
        alpha_matting_foreground_threshold=240,
        alpha_matting_background_threshold=10,
        alpha_matting_erode_size=10,
    )

    out.save(outp)
    print(f"完成! 已保存: {outp}  尺寸 {out.size} 模式 {out.mode}")

if __name__ == "__main__":
    main()
