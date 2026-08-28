// 4 幕对应视频里的 4 段（秒）
// 整段视频 15 秒，分成 0–3 / 3–6 / 6–9 / 9–15 共 4 段
// 滚轮往下滑 → 切到下一段，video 从 videoStart 播到 videoEnd 就停住
// 想改文案/标签/详情，只改这里，不用动 App.jsx

export const scenes = [
  {
    id: 1,
    num: '01',
    videoStart: 0,
    videoEnd: 3,
    tag: 'SWEET TRAP',
    title: '开场 · 脚前面',
    desc: '先给镜头一个站定的姿态，嘻哈气场直接拉满。',
    detail: {
      role: '出场定型',
      elements: ['嘻哈气场', '红黑银', '定格 pose'],
      tone: '张力 / 定格 / 嘻哈',
    },
  },
  {
    id: 2,
    num: '02',
    videoStart: 3,
    videoEnd: 6,
    tag: '拔刀 · 分镜',
    title: '中场 · 刀光闪过',
    desc: '三屏分镜切进来，刀光一闪，节奏被切开。',
    detail: {
      role: '节奏切分',
      elements: ['分镜', '刀光', '黑白红'],
      tone: '凌厉 / 转场 / 节拍',
    },
  },
  {
    id: 3,
    num: '03',
    videoStart: 6,
    videoEnd: 9,
    tag: '闭眼 · 吹泡泡',
    title: '转折 · 鼓起腮帮',
    desc: '镜头给到脸，闭眼，鼓腮，蓄势准备。',
    detail: {
      role: '情绪蓄势',
      elements: ['特写', '粉色', '拟声感'],
      tone: '静 / 聚焦 / 蓄势',
    },
  },
  {
    id: 4,
    num: '04',
    videoStart: 9,
    videoEnd: 15,
    tag: '收尾 · 定格',
    title: '终章 · 泡泡落定',
    desc: '整段视频最后一段，让最饱满的画面多停一会儿。',
    detail: {
      role: '收尾留白',
      elements: ['压轴', '特写', '泡泡'],
      tone: '延展 / 收束 / 印象',
    },
  },
];
