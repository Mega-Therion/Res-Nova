export function AtlasField() {
  return (
    <div className="relative min-h-[360px] overflow-hidden border border-white/10 bg-[#102026]" role="img" aria-label="Abstract field diagram of the Res Nova research atlas">
      <svg className="absolute inset-0 h-full w-full" viewBox="0 0 640 520" preserveAspectRatio="xMidYMid slice" aria-hidden="true">
        <defs>
          <radialGradient id="field-core" cx="52%" cy="48%" r="42%">
            <stop offset="0%" stopColor="#2a8fa3" stopOpacity="0.28" />
            <stop offset="100%" stopColor="#102026" stopOpacity="0" />
          </radialGradient>
        </defs>
        <rect width="640" height="520" fill="url(#field-core)" />
        {[80, 160, 240, 320, 400, 480, 560].map((x) => (
          <line key={`v${x}`} x1={x} y1="0" x2={x} y2="520" stroke="rgba(126,201,212,0.08)" />
        ))}
        {[80, 160, 240, 320, 400, 480].map((y) => (
          <line key={`h${y}`} x1="0" y1={y} x2="640" y2={y} stroke="rgba(126,201,212,0.08)" />
        ))}
        <path d="M20 410 C 90 120, 210 460, 320 90 S 520 340, 630 140" fill="none" stroke="rgba(126,201,212,0.55)" strokeWidth="1.1" />
        <path d="M10 220 C 140 470, 230 40, 360 360 S 540 430, 640 250" fill="none" stroke="rgba(0,114,178,0.4)" strokeWidth="1" />
        <path d="M40 480 C 180 240, 330 310, 610 40" fill="none" stroke="rgba(213,94,0,0.32)" strokeWidth="1" />
        <path d="M30 70 C 160 230, 290 90, 430 250 S 560 180, 640 430" fill="none" stroke="rgba(255,255,255,0.22)" strokeWidth="0.9" strokeDasharray="3 6" />
        {[
          [90, 198],
          [160, 340],
          [268, 128],
          [352, 300],
          [468, 156],
          [532, 364],
          [582, 218],
          [416, 410],
          [224, 446],
          [300, 260],
        ].map(([x, y], i) => (
          <g key={i}>
            <circle cx={x} cy={y} r="7" fill="none" stroke={i % 3 === 0 ? "#d55e00" : "#7ec9d4"} strokeOpacity="0.8" />
            <circle cx={x} cy={y} r="2.2" fill={i % 3 === 0 ? "#d55e00" : "#7ec9d4"} />
          </g>
        ))}
      </svg>
      <div className="absolute inset-0 flex items-center justify-center">
        <div className="text-center text-paper">
          <span className="font-display text-[clamp(4.5rem,12vw,6.5rem)] leading-none tracking-[-0.08em]">R</span>
          <small className="ml-2 font-mono text-[11px] uppercase tracking-[0.22em] text-accent-2">nova</small>
        </div>
      </div>
      <div className="absolute bottom-5 left-5 right-5 flex items-center gap-3 font-mono text-[10px] uppercase tracking-[0.14em] text-[#91b4bb]">
        <span>research state / 2026.09</span>
        <span className="h-px flex-1 bg-accent-2/40" />
        <span>μstd live</span>
      </div>
    </div>
  );
}
