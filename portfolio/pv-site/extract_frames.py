# 把 pv.mp4 抽成一串静态图，供"滚轮逐帧翻"用
# 用法：换新视频后，改下面的 VID 路径 + 输出帧率，重跑本脚本即可
import cv2
import os

VID = r"C:/Users/ayiqianwang/WorkBuddy/vibe coding/portfolio/pv-site/public/pv.mp4"
OUT = r"C:/Users/ayiqianwang/WorkBuddy/vibe coding/portfolio/pv-site/public/frames"
TARGET_FPS = 10        # 每秒抽 10 帧（15s 视频 ≈ 150 张）
OUT_WIDTH = 1920       # 抽帧后缩到 1920 宽（够当全屏背景，又比 2K 轻）
JPEG_QUALITY = 82

os.makedirs(OUT, exist_ok=True)

vid = cv2.VideoCapture(VID)
fps = vid.get(cv2.CAP_PROP_FPS)
total = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
print(f"fps={fps:.2f}  total_frames={total}  duration={total/fps:.2f}s")

step = max(1, round(fps / TARGET_FPS))

idx = 0
count = 0
while True:
    ok, frame = vid.read()
    if not ok:
        break
    if idx % step == 0:
        h, w = frame.shape[:2]
        new_h = int(h * OUT_WIDTH / w)
        frame = cv2.resize(frame, (OUT_WIDTH, new_h), interpolation=cv2.INTER_AREA)
        path = os.path.join(OUT, f"frame-{count:03d}.jpg")
        cv2.imwrite(path, frame, [cv2.IMWRITE_JPEG_QUALITY, JPEG_QUALITY])
        count += 1
    idx += 1

vid.release()
print(f"done, wrote {count} frames -> {OUT}")
