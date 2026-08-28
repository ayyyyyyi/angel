import { useState, useEffect, useRef, useCallback } from 'react';
import { scenes } from './scenes';

const VIDEO = '/pv.mp4';

export default function App() {
  const [current, setCurrent] = useState(0); // 当前第几幕 0~3
  const [started, setStarted] = useState(false); // 是否已点「开始」
  const [detail, setDetail] = useState(null); // 打开的弹窗（哪一幕），null=关
  const [fading, setFading] = useState(false); // 切幕时画面是否正在淡出

  const videoRef = useRef(null);
  const currentRef = useRef(0); // 滚轮回调里拿不到最新 current，用 ref
  const startedRef = useRef(false);
  const lockRef = useRef(false); // 切幕锁，防止连滑

  const scene = scenes[current];

  // 切到第 i 幕：淡出 → 视频跳到该段起点 → 淡入 + 播放到该段终点停住
  const goTo = useCallback((i) => {
    if (i < 0 || i >= scenes.length || i === currentRef.current) return;
    if (lockRef.current) return;
    lockRef.current = true;

    const v = videoRef.current;
    currentRef.current = i;
    setCurrent(i);
    setDetail(null); // 切幕时顺手关掉弹窗

    setFading(true); // 先黑一下
    setTimeout(() => {
      v.currentTime = scenes[i].videoStart; // 跳到这段起点
      if (startedRef.current) {
        v.muted = false;
        v.play().catch(() => {});
      } else {
        v.pause(); // 没点开始：只显示这帧定格，不播
      }
      setFading(false); // 亮回来
      setTimeout(() => {
        lockRef.current = false;
      }, 300);
    }, 280);
  }, []);

  // 点「开始」：在同一次点击里同步「取消静音 + 播放」，浏览器才放行声音
  const handleStart = () => {
    const v = videoRef.current;
    startedRef.current = true;
    setStarted(true);
    v.muted = false;
    v.currentTime = scenes[currentRef.current].videoStart;
    v.play().catch(() => {});
  };

  // 滚轮切幕：往下滑 = 下一幕，往上滑 = 上一幕
  useEffect(() => {
    const onWheel = (e) => {
      e.preventDefault();
      if (e.deltaY > 0) goTo(currentRef.current + 1);
      else goTo(currentRef.current - 1);
    };
    window.addEventListener('wheel', onWheel, { passive: false });
    return () => window.removeEventListener('wheel', onWheel);
  }, [goTo]);

  // 播到该段 videoEnd 就停住定格
  useEffect(() => {
    const v = videoRef.current;
    if (!v) return;
    const onTime = () => {
      const s = scenes[currentRef.current];
      if (v.currentTime >= s.videoEnd) v.pause();
    };
    v.addEventListener('timeupdate', onTime);
    return () => v.removeEventListener('timeupdate', onTime);
  }, []);

  // Esc 关弹窗
  useEffect(() => {
    const onKey = (e) => {
      if (e.key === 'Escape') setDetail(null);
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, []);

  return (
    <div className="page">
      {/* 全屏背景视频（默认静音，点了「开始」才出声） */}
      <video ref={videoRef} className="bg-video" src={VIDEO} muted playsInline preload="auto" />

      {/* 切幕淡出遮罩（黑一下） */}
      <div className={'fade-overlay' + (fading ? ' on' : '')} />

      {/* 左上角：常驻身份（名字 + 定位），任何时候都让人知道这是谁的作品集 */}
      <div className="brand">
        <span className="brand-name">阿意</span>
        <span className="brand-role">游戏发行 · 内容运营</span>
      </div>

      {/* 左下：当前幕文案（key 变化触发淡入动画） */}
      <div className="scene-copy" key={scene.id}>
        <span className="scene-tag">{scene.tag}</span>
        <h1 className="scene-title">{scene.title}</h1>
        <p className="scene-desc">{scene.desc}</p>
        <button className="scene-detail-btn" onClick={() => setDetail(current)}>
          看这段细节 →
        </button>
      </div>

      {/* 右上：幕导航（点哪个跳哪个） */}
      <div className="scene-nav">
        {scenes.map((s, i) => (
          <button
            key={s.id}
            className={'nav-dot' + (i === current ? ' active' : '')}
            onClick={() => goTo(i)}
          >
            <span className="nav-num">{s.num}</span>
            <span className="nav-label">{s.title}</span>
          </button>
        ))}
      </div>

      {/* 开始遮罩（没点开始前盖着） */}
      {!started && (
        <div className="start-mask" onClick={handleStart}>
          <div className="start-btn">
            <span className="play-icon">▶</span>
            <span>点击开始 · 带声音</span>
          </div>
          <span className="start-hint">滚轮切换 4 段 · 点右上切段 · Esc 关弹窗</span>
        </div>
      )}

      {/* 弹窗（看这段细节） */}
      {detail !== null && (
        <div className="detail-mask" onClick={() => setDetail(null)}>
          <div className="detail-panel" onClick={(e) => e.stopPropagation()}>
            <button className="detail-close" onClick={() => setDetail(null)}>×</button>
            <span className="detail-num">{scenes[detail].num}</span>
            <h2 className="detail-title">{scenes[detail].title}</h2>
            <p className="detail-desc">{scenes[detail].desc}</p>
            <div className="detail-meta">
              <div className="meta-row"><em>定位</em><span>{scenes[detail].detail.role}</span></div>
              <div className="meta-row"><em>元素</em><span>{scenes[detail].detail.elements.join(' / ')}</span></div>
              <div className="meta-row"><em>调性</em><span>{scenes[detail].detail.tone}</span></div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
