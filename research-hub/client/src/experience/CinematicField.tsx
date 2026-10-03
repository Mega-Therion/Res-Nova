import { useEffect, useRef, useState } from "react";
import * as THREE from "three";
import { Orbit, Volume2, VolumeX, Zap } from "lucide-react";

type RenderTier = "TIER_A" | "TIER_B" | "TIER_C";
type FieldMode = "nbody" | "kerr" | "sparc" | "cosmic";

type Capabilities = {
  tier: RenderTier;
  webgpu: boolean;
  webgl2: boolean;
  reducedMotion: boolean;
};

async function detectCapabilities(): Promise<Capabilities> {
  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  let webgl2 = false;
  try {
    const probe = document.createElement("canvas");
    webgl2 = Boolean(probe.getContext("webgl2"));
    probe.width = 1;
    probe.height = 1;
  } catch {
    webgl2 = false;
  }

  let webgpu = false;
  try {
    const gpu = (navigator as Navigator & { gpu?: { requestAdapter: (options?: unknown) => Promise<unknown> } }).gpu;
    if (gpu) webgpu = Boolean(await gpu.requestAdapter({ powerPreference: "high-performance" }));
  } catch {
    webgpu = false;
  }

  return {
    tier: reducedMotion ? (webgl2 ? "TIER_B" : "TIER_C") : webgpu ? "TIER_A" : webgl2 ? "TIER_B" : "TIER_C",
    webgpu,
    webgl2,
    reducedMotion,
  };
}

const modeMeta: Record<FieldMode, { label: string; accent: string; description: string }> = {
  nbody: { label: "N-body", accent: "#79d7e8", description: "orbital structure / field flow" },
  kerr: { label: "Kerr", accent: "#c49af7", description: "relativistic frame / spin" },
  sparc: { label: "SPARC", accent: "#f1b86a", description: "rotation curves / evidence" },
  cosmic: { label: "Cosmic", accent: "#75d6a0", description: "large-scale bridge / horizon" },
};

export default function CinematicField() {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const [tier, setTier] = useState<RenderTier>("TIER_C");
  const [mode, setMode] = useState<FieldMode>("nbody");
  const [audioOn, setAudioOn] = useState(false);
  const [fps, setFps] = useState(0);
  const audioRef = useRef<AudioContext | null>(null);
  const oscillatorRef = useRef<OscillatorNode | null>(null);
  const gainRef = useRef<GainNode | null>(null);

  useEffect(() => {
    let cancelled = false;
    let frame = 0;
    let cleanup = () => {};

    async function start() {
      const caps = await detectCapabilities();
      if (cancelled) return;
      setTier(caps.tier);
      if (caps.tier === "TIER_C" || !canvasRef.current) return;

      const canvas = canvasRef.current;
      const scene = new THREE.Scene();
      scene.fog = new THREE.FogExp2(0x10262d, 0.006);
      const camera = new THREE.PerspectiveCamera(48, 1, 0.1, 500);
      camera.position.set(0, 10, 62);
      camera.lookAt(0, 0, 0);

      let renderer: any;
      let isWebGPU = false;
      try {
        if (caps.tier === "TIER_A") {
          const module = await import("three/webgpu");
          renderer = new (module as any).WebGPURenderer({ canvas, antialias: true, alpha: true, powerPreference: "high-performance" });
          await renderer.init();
          isWebGPU = true;
        }
      } catch {
        renderer = null;
      }
      if (!renderer) {
        renderer = new THREE.WebGLRenderer({ canvas, antialias: caps.tier === "TIER_B", alpha: true, powerPreference: "high-performance" });
      }
      renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, caps.tier === "TIER_A" ? 1.6 : 1.25));
      renderer.outputColorSpace = THREE.SRGBColorSpace;
      renderer.toneMapping = THREE.ACESFilmicToneMapping;
      renderer.toneMappingExposure = 1.12;

      const root = new THREE.Group();
      scene.add(root);
      const core = new THREE.Mesh(
        new THREE.SphereGeometry(3.6, 32, 32),
        new THREE.MeshBasicMaterial({ color: 0x79d7e8, transparent: true, opacity: 0.72 })
      );
      root.add(core);

      const glow = new THREE.Mesh(
        new THREE.SphereGeometry(7.2, 24, 24),
        new THREE.MeshBasicMaterial({ color: 0x2f9eaf, transparent: true, opacity: 0.08, blending: THREE.AdditiveBlending, depthWrite: false })
      );
      root.add(glow);

      const count = caps.tier === "TIER_A" ? 18000 : 6500;
      const positions = new Float32Array(count * 3);
      const colors = new Float32Array(count * 3);
      const seeds = new Float32Array(count);
      for (let i = 0; i < count; i++) {
        const radius = 7 + Math.pow(Math.random(), 0.55) * 48;
        const angle = Math.random() * Math.PI * 2;
        const thickness = (Math.random() - 0.5) * (1.4 + radius * 0.03);
        const j = i * 3;
        positions[j] = Math.cos(angle) * radius;
        positions[j + 1] = thickness;
        positions[j + 2] = Math.sin(angle) * radius;
        colors[j] = 0.28 + Math.random() * 0.2;
        colors[j + 1] = 0.72 + Math.random() * 0.2;
        colors[j + 2] = 0.88 + Math.random() * 0.12;
        seeds[i] = Math.random();
      }
      const geometry = new THREE.BufferGeometry();
      geometry.setAttribute("position", new THREE.BufferAttribute(positions, 3));
      geometry.setAttribute("color", new THREE.BufferAttribute(colors, 3));
      const points = new THREE.Points(geometry, new THREE.PointsMaterial({ size: caps.tier === "TIER_A" ? 0.34 : 0.48, vertexColors: true, transparent: true, opacity: 0.82, blending: THREE.AdditiveBlending, depthWrite: false, sizeAttenuation: true }));
      root.add(points);

      const ring = new THREE.Mesh(
        new THREE.TorusGeometry(18, 0.035, 8, 160),
        new THREE.MeshBasicMaterial({ color: 0x79d7e8, transparent: true, opacity: 0.27 })
      );
      ring.rotation.x = Math.PI / 2.18;
      root.add(ring);

      const pointer = { x: 0, y: 0 };
      const handlePointer = (event: PointerEvent) => {
        pointer.x = (event.clientX / window.innerWidth - 0.5) * 2;
        pointer.y = (event.clientY / window.innerHeight - 0.5) * 2;
      };
      window.addEventListener("pointermove", handlePointer, { passive: true });

      const resize = () => {
        const rect = canvas.getBoundingClientRect();
        const width = Math.max(1, rect.width);
        const height = Math.max(1, rect.height);
        camera.aspect = width / height;
        camera.updateProjectionMatrix();
        renderer.setSize(width, height, false);
      };
      resize();
      window.addEventListener("resize", resize);

      let last = performance.now();
      let frames = 0;
      let lastFps = last;
      const tick = (now: number) => {
        if (cancelled) return;
        const delta = Math.min((now - last) / 1000, 0.05);
        last = now;
        frames++;
        if (now - lastFps > 700) {
          setFps(Math.round((frames * 1000) / (now - lastFps)));
          frames = 0;
          lastFps = now;
        }
        const animate = !caps.reducedMotion;
        const speed = mode === "kerr" ? 0.58 : mode === "sparc" ? 0.32 : mode === "cosmic" ? 0.12 : 0.22;
        if (animate) {
          points.rotation.y += delta * speed;
          ring.rotation.z += delta * speed * 0.23;
          root.rotation.x += (pointer.y * 0.12 - root.rotation.x) * Math.min(1, delta * 2.4);
          root.rotation.z += (-pointer.x * 0.08 - root.rotation.z) * Math.min(1, delta * 2.4);
          core.scale.setScalar(1 + Math.sin(now * 0.0012) * 0.035);
        }
        camera.position.x += (pointer.x * 2.8 - camera.position.x) * Math.min(1, delta * 1.8);
        camera.position.y += (10 - pointer.y * 1.6 - camera.position.y) * Math.min(1, delta * 1.8);
        camera.lookAt(0, 0, 0);
        renderer.render(scene, camera);
        frame = requestAnimationFrame(tick);
      };
      frame = requestAnimationFrame(tick);

      cleanup = () => {
        cancelAnimationFrame(frame);
        window.removeEventListener("resize", resize);
        window.removeEventListener("pointermove", handlePointer);
        geometry.dispose();
        (points.material as THREE.Material).dispose();
        core.geometry.dispose();
        core.material.dispose();
        glow.geometry.dispose();
        glow.material.dispose();
        ring.geometry.dispose();
        ring.material.dispose();
        renderer.dispose();
      };

      // Keep the renderer label available to the HUD without pretending WebGL2 is WebGPU.
      if (!isWebGPU && caps.tier === "TIER_A") setTier("TIER_B");
    }

    start();
    return () => {
      cancelled = true;
      cleanup();
    };
  }, [mode]);

  const toggleAudio = () => {
    if (!audioRef.current) {
      const AudioContextCtor = window.AudioContext || (window as typeof window & { webkitAudioContext?: typeof AudioContext }).webkitAudioContext;
      if (!AudioContextCtor) return;
      const ctx = new AudioContextCtor();
      const oscillator = ctx.createOscillator();
      const gain = ctx.createGain();
      oscillator.type = "sine";
      oscillator.frequency.value = 92;
      gain.gain.value = 0.018;
      oscillator.connect(gain).connect(ctx.destination);
      oscillator.start();
      audioRef.current = ctx;
      oscillatorRef.current = oscillator;
      gainRef.current = gain;
    }
    const next = !audioOn;
    setAudioOn(next);
    if (gainRef.current) gainRef.current.gain.setTargetAtTime(next ? 0.018 : 0, audioRef.current!.currentTime, 0.12);
    if (audioRef.current?.state === "suspended" && next) void audioRef.current.resume();
  };

  const meta = modeMeta[mode];
  return (
    <div className="cinematic-field" aria-label="Interactive Res Nova research field">
      <canvas ref={canvasRef} className="cinematic-field-canvas" aria-label="Animated orbital research field" />
      {tier === "TIER_C" && <div className="cinematic-field-static" aria-hidden="true" />}
      <div className="cinematic-field-vignette" aria-hidden="true" />
      <div className="cinematic-field-hud">
        <div className="field-hud-brand"><Orbit size={15} /><span>RES NOVA</span><small>field / live</small></div>
        <div className="field-hud-status"><span className="field-status-dot" style={{ background: meta.accent }} />{meta.description}<span className="field-hud-separator">·</span>{tier === "TIER_A" ? "WebGPU" : tier === "TIER_B" ? "WebGL2" : "static"}<span className="field-hud-separator">·</span>{fps || "—"} fps</div>
      </div>
      <div className="cinematic-field-controls" role="group" aria-label="Research field modes">
        <div className="field-mode-label"><Zap size={13} /> explore layer</div>
        <div className="field-mode-buttons">
          {(Object.keys(modeMeta) as FieldMode[]).map((item) => <button key={item} type="button" className={mode === item ? "is-active" : ""} style={mode === item ? { borderColor: modeMeta[item].accent, color: modeMeta[item].accent } : undefined} onClick={() => setMode(item)}>{modeMeta[item].label}</button>)}
        </div>
        <button type="button" className="field-audio-button" onClick={toggleAudio} aria-pressed={audioOn}>{audioOn ? <Volume2 size={13} /> : <VolumeX size={13} />}{audioOn ? "soundscape on" : "soundscape off"}</button>
      </div>
      <div className="cinematic-field-caption"><span className="field-caption-rule" /><span>visual index / {mode.toUpperCase()} / not a physical simulation</span></div>
    </div>
  );
}

export { detectCapabilities };
