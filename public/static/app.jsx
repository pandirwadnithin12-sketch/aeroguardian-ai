/* ============================================================
   AeroGuardian AI - React Master Application
   "An AI Agent for Pilot Workload & Decision Support"
   Theme: "Smart Systems for a Safer Future in Aviation"
   ============================================================ */

const { useState, useEffect, useRef, useMemo, useCallback } = React;

// ============================================================
// 1. LUCIDE ICONS (Direct High-Performance SVG Components)
// ============================================================

const LucideIcons = {
  Shield: (props) => (
    <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
    </svg>
  ),
  Home: (props) => (
    <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/>
    </svg>
  ),
  Sparkles: (props) => (
    <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="m12 3-1.9 5.8a2 2 0 0 1-1.3 1.3L3 12l5.8 1.9a2 2 0 0 1 1.3 1.3L12 21l1.9-5.8a2 2 0 0 1 1.3-1.3L21 12l-5.8-1.9a2 2 0 0 1-1.3-1.3Z"/>
    </svg>
  ),
  ArrowRight: (props) => (
    <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>
    </svg>
  ),
  Plane: (props) => (
    <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M17.8 19.2 16 11l3.5-3.5C21 6 21.5 4 21 3c-1-.5-3 0-4.5 1.5L13 8 4.8 6.2c-.5-.1-.9.1-1.1.5l-.3.5c-.2.5-.1 1 .3 1.3L9 12l-2 3H4l-1 1 3 2 2 3 1-1v-3l3-2 3.5 5.3c.3.4.8.5 1.3.3l.5-.2c.4-.3.6-.7.5-1.2z"/>
    </svg>
  ),
  Radio: (props) => (
    <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="12" cy="12" r="2"/><path d="M16.24 7.76a6 6 0 0 1 0 8.49m-8.48-.01a6 6 0 0 1 0-8.49m11.31-2.82a10 10 0 0 1 0 14.14m-14.14 0a10 10 0 0 1 0-14.14"/>
    </svg>
  ),
  AlertTriangle: (props) => (
    <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/>
    </svg>
  ),
  AlertOctagon: (props) => (
    <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <polygon points="7.86 2 16.14 2 22 7.86 22 16.14 16.14 22 7.86 22 2 16.14 2 7.86 7.86 2"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/>
    </svg>
  ),
  CheckCircle2: (props) => (
    <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/>
    </svg>
  ),
  Wind: (props) => (
    <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M17.7 7.7a2.5 2.5 0 1 1 1.8 4.3H2"/><path d="M9.6 4.6A2 2 0 1 1 11 8H2"/><path d="M12.6 19.4A2 2 0 1 0 14 16H2"/>
    </svg>
  ),
  Eye: (props) => (
    <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"/><circle cx="12" cy="12" r="3"/>
    </svg>
  ),
  Compass: (props) => (
    <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="12" cy="12" r="10"/><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/>
    </svg>
  ),
  Activity: (props) => (
    <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>
    </svg>
  ),
  BarChart3: (props) => (
    <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <line x1="12" y1="20" x2="12" y2="10"/><line x1="18" y1="20" x2="18" y2="4"/><line x1="6" y1="20" x2="6" y2="16"/>
    </svg>
  ),
  MessageSquare: (props) => (
    <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
    </svg>
  ),
  Info: (props) => (
    <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/>
    </svg>
  ),
  RefreshCw: (props) => (
    <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8"/><path d="M21 3v5h-5"/><path d="M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16"/><path d="M8 16H3v5"/>
    </svg>
  ),
  Layers: (props) => (
    <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/>
    </svg>
  ),
  Search: (props) => (
    <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>
    </svg>
  ),
  Filter: (props) => (
    <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"/>
    </svg>
  ),
  Check: (props) => (
    <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <polyline points="20 6 9 17 4 12"/>
    </svg>
  ),
  X: (props) => (
    <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
    </svg>
  ),
  Key: (props) => (
    <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="7.5" cy="15.5" r="5.5"/><path d="m21 2-9.6 9.6"/><path d="m15.5 7.5 3 3L22 7l-3-3"/>
    </svg>
  ),
  Route: (props) => (
    <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="6" cy="19" r="3"/><path d="M9 19h8.5a3.5 3.5 0 0 0 0-7h-11a3.5 3.5 0 0 1 0-7H15"/><circle cx="18" cy="5" r="3"/>
    </svg>
  ),
  MapPin: (props) => (
    <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/>
    </svg>
  ),
  Clock: (props) => (
    <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>
    </svg>
  ),
  ChevronRight: (props) => (
    <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <polyline points="9 18 15 12 9 6"/>
    </svg>
  ),
  Navigation: (props) => (
    <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <polygon points="3 11 22 2 13 21 11 13 3 11"/>
    </svg>
  ),
  Thermometer: (props) => (
    <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M14 14.76V3.5a2.5 2.5 0 0 0-5 0v11.26a4.5 4.5 0 1 0 5 0z"/>
    </svg>
  ),
  CloudRain: (props) => (
    <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M4 14.899A7 7 0 1 1 15.71 8h1.79a4.5 4.5 0 0 1 2.5 8.242"/><path d="M16 14v6"/><path d="M8 14v6"/><path d="M12 16v6"/>
    </svg>
  ),
  Gauge: (props) => (
    <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="m12 14 4-4"/><path d="M3.34 19a10 10 0 1 1 17.32 0"/>
    </svg>
  ),
  Volume2: (props) => (
    <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/><path d="M15.54 8.46a5 5 0 0 1 0 7.07"/><path d="M19.07 4.93a10 10 0 0 1 0 14.14"/>
    </svg>
  ),
  VolumeX: (props) => (
    <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/><line x1="23" y1="9" x2="17" y2="15"/><line x1="17" y1="9" x2="23" y2="15"/>
    </svg>
  ),
  Download: (props) => (
    <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/>
    </svg>
  ),
  Terminal: (props) => (
    <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <polyline points="4 17 10 11 4 5"/><line x1="12" y1="19" x2="20" y2="19"/>
    </svg>
  ),
  Cpu: (props) => (
    <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <rect x="4" y="4" width="16" height="16" rx="2"/><rect x="9" y="9" width="6" height="6"/><line x1="9" y1="1" x2="9" y2="4"/><line x1="15" y1="1" x2="15" y2="4"/><line x1="9" y1="20" x2="9" y2="23"/><line x1="15" y1="20" x2="15" y2="23"/><line x1="20" y1="9" x2="23" y2="9"/><line x1="20" y1="14" x2="23" y2="14"/><line x1="1" y1="9" x2="4" y2="9"/><line x1="1" y1="14" x2="4" y2="14"/>
    </svg>
  ),
  Clock: (props) => (
    <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>
    </svg>
  ),
  Square: (props) => (
    <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <rect width="18" height="18" x="3" y="3" rx="2"/>
    </svg>
  ),
  CheckSquare: (props) => (
    <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <polyline points="9 11 12 14 22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/>
    </svg>
  ),
  MapPin: (props) => (
    <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/>
    </svg>
  ),
  Maximize2: (props) => (
    <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <polyline points="15 3 21 3 21 9"/><polyline points="9 21 3 21 3 15"/><line x1="21" y1="3" x2="14" y2="10"/><line x1="3" y1="21" x2="10" y2="14"/>
    </svg>
  ),
  Minimize2: (props) => (
    <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <polyline points="4 14 10 14 10 20"/><polyline points="20 10 14 10 14 4"/><line x1="14" y1="10" x2="21" y2="3"/><line x1="3" y1="21" x2="10" y2="14"/>
    </svg>
  ),
  Play: (props) => (
    <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <polygon points="5 3 19 12 5 21 5 3"/>
    </svg>
  ),
  Pause: (props) => (
    <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <rect x="6" y="4" width="4" height="16"/><rect x="14" y="4" width="4" height="16"/>
    </svg>
  ),
  FastForward: (props) => (
    <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <polygon points="13 19 22 12 13 5 13 19"/><polygon points="2 19 11 12 2 5 2 19"/>
    </svg>
  ),
  Route: (props) => (
    <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="6" cy="19" r="3"/><path d="M9 19h8.5a3.5 3.5 0 0 0 0-7h-11a3.5 3.5 0 0 1 0-7H15"/><circle cx="18" cy="5" r="3"/>
    </svg>
  ),
};

const Icon = ({ name, size = 18, color = "currentColor", className = "", style = {} }) => {
  const Component = LucideIcons[name];
  if (!Component) return null;
  return <Component width={size} height={size} stroke={color} className={className} style={style} />;
};


// ============================================================
// 2. WEB AUDIO API AVIONICS CAUTION CHIME
// ============================================================

const playCautionChime = () => {
  try {
    const AudioContext = window.AudioContext || window.webkitAudioContext;
    if (!AudioContext) return;
    const ctx = new AudioContext();
    const now = ctx.currentTime;

    const osc1 = ctx.createOscillator();
    const osc2 = ctx.createOscillator();
    const gain = ctx.createGain();

    osc1.type = "sine";
    osc1.frequency.setValueAtTime(880, now); // A5
    osc1.frequency.setValueAtTime(1046.5, now + 0.1); // C6

    osc2.type = "triangle";
    osc2.frequency.setValueAtTime(440, now);

    gain.gain.setValueAtTime(0.08, now);
    gain.gain.exponentialRampToValueAtTime(0.001, now + 0.35);

    osc1.connect(gain);
    osc2.connect(gain);
    gain.connect(ctx.destination);

    osc1.start(now);
    osc2.start(now);
    osc1.stop(now + 0.35);
    osc2.stop(now + 0.35);
  } catch (e) {
    // Audio contexts restricted by user gesture or unsupported
  }
};


// ============================================================
// 3. UTILITY FORMATTERS (Aviation Conversions)
// ============================================================

const fmtAlt = (meters) => {
  if (meters === null || meters === undefined) return "N/A";
  const ft = Math.round(meters * 3.28084);
  return `${ft.toLocaleString()} ft (${Math.round(meters).toLocaleString()} m)`;
};

const fmtSpd = (ms) => {
  if (ms === null || ms === undefined) return "N/A";
  const kts = Math.round(ms * 1.94384);
  return `${kts} kts (${ms.toFixed(1)} m/s)`;
};

const fmtVR = (ms) => {
  if (ms === null || ms === undefined) return "N/A";
  const fpm = Math.round(ms * 196.85);
  if (Math.abs(fpm) < 100) return "Level (0 fpm)";
  const arrow = fpm > 0 ? "▲" : "▼";
  return `${arrow} ${fpm > 0 ? "+" : ""}${fpm} fpm`;
};

const fmtHdg = (deg) => {
  if (deg === null || deg === undefined) return "N/A";
  const dirs = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"];
  const idx = Math.floor((deg + 11.25) / 22.5) % 16;
  return `${Math.round(deg)}° (${dirs[idx]})`;
};


// ============================================================
// 4. INTERACTIVE LEAFLET RADAR MAP COMPONENT
// ============================================================

const getCardinalDirection = (deg) => {
  if (deg === null || deg === undefined) return "N";
  const val = Math.round(deg / 22.5);
  const dirs = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"];
  return dirs[val % 16];
};

const calcDirectionVector = (lat, lon, heading, km = 24) => {
  const headingRad = ((heading || 0) * Math.PI) / 180.0;
  const latRad = (lat * Math.PI) / 180.0;
  const projLat = lat + (km / 6371.0) * (180.0 / Math.PI) * Math.cos(headingRad);
  const projLon = lon + ((km / 6371.0) * (180.0 / Math.PI) * Math.sin(headingRad)) / Math.cos(latRad);
  return [[lat, lon], [projLat, projLon]];
};

const RadarMap = ({
  aircraft = [],
  alerts = [],
  onSelectPlane,
  region = "India",
  selectedPlane = null,
}) => {
  const mapContainerRef = useRef(null);
  const mapInstanceRef = useRef(null);
  const markersLayerRef = useRef(null);
  const vectorsLayerRef = useRef(null);
  const routesLayerRef = useRef(null);
  const airportsLayerRef = useRef(null);
  const baseLayersRef = useRef({});
  const layersControlRef = useRef(null);
  const planesSimRef = useRef({});
  const lastTimeRef = useRef(performance.now());
  const animFrameRef = useRef(null);

  // Motion, Direction & Flight Path Corridors States
  const [motionSpeed, setMotionSpeed] = useState(3); // 1 = Realtime, 3 = Active Glide, 8 = Fast Cruise, 0 = Pause
  const [showDirections, setShowDirections] = useState(true);
  const [routeMode, setRouteMode] = useState("selected"); // "selected" | "all" | "off"

  // Map API Key State
  const [mapApiKey, setMapApiKey] = useState("");
  const [keyProvider, setKeyProvider] = useState("mapbox");
  const [hasApiKey, setHasApiKey] = useState(false);
  const [showKeyModal, setShowKeyModal] = useState(false);
  const [keyInput, setKeyInput] = useState("");
  const [savingKey, setSavingKey] = useState(false);
  const [saveStatus, setSaveStatus] = useState(null);

  // Region Centers
  const regionCoords = {
    India: { center: [21.5, 79.0], zoom: 5 },
    Global: { center: [20.0, 0.0], zoom: 2 },
    Europe: { center: [50.0, 10.0], zoom: 4 },
    "North America": { center: [39.0, -98.0], zoom: 4 },
    "Southeast Asia": { center: [8.0, 115.0], zoom: 4 },
    "Middle East": { center: [25.0, 48.0], zoom: 4 },
  };

  // 1. Setup Base Tile Layers (Free Open Basemaps + Mapbox/MapTiler when API key is provided)
  const setupTileLayers = useCallback((map, apiKey, provider) => {
    if (!map) return;

    // Remove existing tile layers and layer switcher
    Object.values(baseLayersRef.current).forEach((l) => {
      if (map.hasLayer(l)) map.removeLayer(l);
    });
    if (layersControlRef.current) {
      map.removeControl(layersControlRef.current);
      layersControlRef.current = null;
    }

    baseLayersRef.current = {};

    // 100% Free Open Basemaps (No API key required, zero watermark)
    const esriDark = L.layerGroup([
      L.tileLayer("https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Dark_Gray_Base/MapServer/tile/{z}/{y}/{x}", {
        maxZoom: 16,
        attribution: "Tiles &copy; Esri",
      }),
      L.tileLayer("https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Dark_Gray_Reference/MapServer/tile/{z}/{y}/{x}", {
        maxZoom: 16,
        attribution: "&copy; Esri, DeLorme, NAVTEQ",
      }),
    ]);

    const osmStandard = L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      maxZoom: 19,
      attribution: "&copy; OpenStreetMap contributors",
    });

    const cartoUrl = (apiKey && apiKey.trim())
      ? `https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png?key=${apiKey.trim()}`
      : "https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png";

    const cartoDark = L.tileLayer(cartoUrl, {
      subdomains: "abcd",
      maxZoom: 19,
      attribution: "&copy; OpenStreetMap contributors &copy; CARTO",
    });

    const baseMaps = {
      "🌙 Dark Aerospace (Esri Dark - Free)": esriDark,
      "🗺️ OpenStreetMap (Free)": osmStandard,
      "🌙 Carto Dark": cartoDark,
    };

    let activeLayer = esriDark;

    // When Map API Key is provided, activate premium vector tiles
    if (apiKey && apiKey.trim()) {
      const cleanKey = apiKey.trim();
      if (provider === "carto") {
        baseMaps["⭐ CARTO Dark (Active Key)"] = cartoDark;
        activeLayer = cartoDark;
      } else if (provider === "maptiler" || cleanKey.startsWith("key_")) {
        const maptilerDark = L.tileLayer(`https://api.maptiler.com/maps/dataviz-dark/{z}/{x}/{y}.png?key=${cleanKey}`, {
          maxZoom: 20,
          attribution: "&copy; MapTiler &copy; OpenStreetMap contributors",
        });
        baseMaps["⭐ MapTiler Dark (Active Key)"] = maptilerDark;
        activeLayer = maptilerDark;
      } else {
        // Mapbox (Default or pk. token)
        const mapboxDark = L.tileLayer(`https://api.mapbox.com/styles/v1/mapbox/dark-v11/tiles/{z}/{x}/{y}?access_token=${cleanKey}`, {
          tileSize: 512,
          zoomOffset: -1,
          maxZoom: 22,
          attribution: "&copy; Mapbox &copy; OpenStreetMap contributors",
        });
        const mapboxSatellite = L.tileLayer(`https://api.mapbox.com/styles/v1/mapbox/satellite-streets-v12/tiles/{z}/{x}/{y}?access_token=${cleanKey}`, {
          tileSize: 512,
          zoomOffset: -1,
          maxZoom: 22,
          attribution: "&copy; Mapbox &copy; OpenStreetMap contributors",
        });
        baseMaps["⭐ Mapbox Dark Vector (Active Key)"] = mapboxDark;
        baseMaps["🛰️ Mapbox Satellite (Active Key)"] = mapboxSatellite;
        activeLayer = mapboxDark;
      }
    }

    activeLayer.addTo(map);
    baseLayersRef.current = baseMaps;
    layersControlRef.current = L.control.layers(baseMaps, null, { position: "topright" }).addTo(map);
  }, []);

  // 2. Fetch Map API Key from Backend on Mount
  useEffect(() => {
    fetch("/api/config/map")
      .then((res) => res.json())
      .then((cfg) => {
        if (cfg.active_key) {
          setMapApiKey(cfg.active_key);
          setKeyInput(cfg.active_key);
          setKeyProvider(cfg.provider || "mapbox");
          setHasApiKey(true);
          if (mapInstanceRef.current) {
            setupTileLayers(mapInstanceRef.current, cfg.active_key, cfg.provider || "mapbox");
          }
        }
      })
      .catch(() => {});
  }, [setupTileLayers]);

  // 3. Initialize Map Instance and Layer Groups
  useEffect(() => {
    if (!mapContainerRef.current) return;

    let resizeObserver = null;

    if (!mapInstanceRef.current) {
      const cfg = regionCoords[region] || regionCoords.India;
      const map = L.map(mapContainerRef.current, {
        center: cfg.center,
        zoom: cfg.zoom,
        zoomControl: false,
        attributionControl: false,
      });

      L.control.zoom({ position: "bottomright" }).addTo(map);

      // Setup initial tile layers
      setupTileLayers(map, mapApiKey, keyProvider);

      vectorsLayerRef.current = L.layerGroup().addTo(map);
      routesLayerRef.current = L.layerGroup().addTo(map);
      airportsLayerRef.current = L.layerGroup().addTo(map);
      markersLayerRef.current = L.layerGroup().addTo(map);
      mapInstanceRef.current = map;

      // Fix map sizing: Multi-pulse invalidateSize to guarantee complete full-width rendering
      [50, 150, 300, 600, 1200].forEach((delay) => {
        setTimeout(() => {
          if (mapInstanceRef.current) {
            mapInstanceRef.current.invalidateSize();
          }
        }, delay);
      });
    }

    if (window.ResizeObserver && mapContainerRef.current) {
      resizeObserver = new ResizeObserver(() => {
        if (mapInstanceRef.current) {
          mapInstanceRef.current.invalidateSize();
        }
      });
      resizeObserver.observe(mapContainerRef.current);
    }

    const handleWindowResize = () => {
      if (mapInstanceRef.current) {
        mapInstanceRef.current.invalidateSize();
      }
    };
    window.addEventListener("resize", handleWindowResize);

    return () => {
      window.removeEventListener("resize", handleWindowResize);
      if (resizeObserver) resizeObserver.disconnect();
      if (animFrameRef.current) cancelAnimationFrame(animFrameRef.current);
      if (mapInstanceRef.current) {
        mapInstanceRef.current.remove();
        mapInstanceRef.current = null;
      }
      planesSimRef.current = {};
      markersLayerRef.current = null;
      vectorsLayerRef.current = null;
      routesLayerRef.current = null;
      airportsLayerRef.current = null;
    };
  }, [region]);

  // 4. Save and Apply Map API Key Handler
  const handleSaveApiKey = async (clearKey = false) => {
    setSavingKey(true);
    setSaveStatus(null);
    const keyToSave = clearKey ? "" : keyInput.trim();
    try {
      const res = await fetch("/api/config/map", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ api_key: keyToSave, provider: keyProvider }),
      });
      const data = await res.json();
      if (data.status === "success") {
        setMapApiKey(keyToSave);
        if (clearKey) setKeyInput("");
        setHasApiKey(Boolean(keyToSave));
        setSaveStatus({
          type: "success",
          msg: keyToSave ? "Map API Key saved in .env & activated on map!" : "API Key cleared. Using free open basemaps.",
        });
        if (mapInstanceRef.current) {
          setupTileLayers(mapInstanceRef.current, keyToSave, keyProvider);
        }
        setTimeout(() => {
          setShowKeyModal(false);
          setSaveStatus(null);
        }, 1200);
      } else {
        setSaveStatus({ type: "error", msg: data.message || "Failed to save API key" });
      }
    } catch (err) {
      setSaveStatus({ type: "error", msg: "Network error saving API key" });
    } finally {
      setSavingKey(false);
    }
  };

  // 5. Pan Gently to Selected Plane
  useEffect(() => {
    if (selectedPlane && selectedPlane.latitude && selectedPlane.longitude && mapInstanceRef.current) {
      mapInstanceRef.current.panTo([selectedPlane.latitude, selectedPlane.longitude], { animate: true });
    }
  }, [selectedPlane?.icao24]);

  // 6. Toggle Direction Vector Layer Visibility
  useEffect(() => {
    if (!mapInstanceRef.current || !vectorsLayerRef.current) return;
    if (showDirections) {
      if (!mapInstanceRef.current.hasLayer(vectorsLayerRef.current)) {
        vectorsLayerRef.current.addTo(mapInstanceRef.current);
      }
    } else {
      if (mapInstanceRef.current.hasLayer(vectorsLayerRef.current)) {
        vectorsLayerRef.current.remove();
      }
    }
  }, [showDirections]);

  // 7. Synchronize Live ADS-B Data into Kinematic Simulation Model
  useEffect(() => {
    if (!mapInstanceRef.current || !markersLayerRef.current || !vectorsLayerRef.current) return;
    const markersGroup = markersLayerRef.current;
    const vectorsGroup = vectorsLayerRef.current;
    const currentIcaos = new Set();
    const alertMap = {};
    alerts.forEach((a) => {
      alertMap[a.icao24] = a.priority;
    });

    aircraft.forEach((plane) => {
      if (plane.latitude === null || plane.latitude === undefined || plane.longitude === null || plane.longitude === undefined) return;
      const icao = plane.icao24;
      currentIcaos.add(icao);

      const heading = plane.heading || 0;
      const pri = alertMap[icao];
      let color = "#00e5ff"; // Nominal airborne cyan
      if (pri === "CRITICAL") color = "#ff3366";
      else if (pri === "HIGH") color = "#f59e0b";
      else if (pri === "MEDIUM") color = "#fbbf24";
      else if (plane.on_ground) color = "#64748b";

      const isSelected = selectedPlane && selectedPlane.icao24 === icao;
      const fl = plane.flight_level || (plane.baro_altitude ? `FL${Math.round(plane.baro_altitude * 3.28084 / 100)}` : "FL--");
      const speedKts = plane.speed_kts || Math.round((plane.velocity || 0) * 1.94384);
      const callsign = (plane.callsign || icao).trim();
      const speedMs = plane.velocity || (plane.speed_kts ? plane.speed_kts * 0.514444 : 220);
      const cardinalDir = getCardinalDirection(heading);

      // Clean SVG Aircraft Marker (Rotates in the exact flight direction, no text glued on plane)
      const buildIconHtml = (hdg, clr, sel) => `
        <div style="width:32px; height:32px; display:flex; align-items:center; justify-content:center; cursor:pointer; position:relative;">
          ${sel ? '<div style="position:absolute; width:34px; height:34px; border-radius:50%; border:2px solid #00e5ff; box-shadow:0 0 10px #00e5ff;"></div>' : ''}
          <svg style="transform: rotate(${hdg}deg); transform-origin: center center; filter: drop-shadow(0 0 5px ${clr});" width="24" height="24" viewBox="0 0 24 24" fill="${clr}">
            <path d="M21 16v-2l-8-5V3.5c0-.83-.67-1.5-1.5-1.5S10 2.67 10 3.5V9l-8 5v2l8-2.5V19l-2 1.5V22l3.5-1 3.5 1v-1.5L13 19v-5.5l8 2.5z"/>
          </svg>
        </div>
      `;

      const tooltipContent = `
        <div style="font-family:var(--font-mono, monospace); font-size:11px; line-height:1.4;">
          <b style="color:#00e5ff; font-size:12px;">${callsign}</b> (${icao})<br/>
          Alt: <b>${fl}</b> • Speed: <b>${speedKts} kts</b><br/>
          Direction: <b>${Math.round(heading)}° (${cardinalDir})</b> • Country: <b>${plane.origin_country || plane.country || "Intl"}</b>
        </div>
      `;

      if (planesSimRef.current[icao]) {
        // Update existing simulated plane
        const sim = planesSimRef.current[icao];
        sim.targetLat = plane.latitude;
        sim.targetLon = plane.longitude;
        sim.heading = heading;
        sim.speedMs = speedMs;
        sim.speedKts = speedKts;
        sim.onGround = plane.on_ground;
        sim.color = color;
        sim.isSelected = isSelected;

        // Re-anchor if telemetry moved significantly (e.g. initial re-fix)
        if (Math.hypot(sim.lat - plane.latitude, sim.lon - plane.longitude) > 0.5) {
          sim.lat = plane.latitude;
          sim.lon = plane.longitude;
        }

        if (sim.marker) {
          sim.marker.setIcon(
            L.divIcon({
              html: buildIconHtml(heading, color, isSelected),
              className: "aircraft-clean-marker",
              iconSize: [32, 32],
              iconAnchor: [16, 16],
            })
          );
          sim.marker.setTooltipContent(tooltipContent);
        }

        if (sim.vectorLine) {
          sim.vectorLine.setStyle({
            color: isSelected ? "#00e5ff" : color,
            weight: isSelected ? 2.5 : 1.5,
            opacity: isSelected ? 0.95 : 0.65,
          });
        }
      } else {
        // Create new plane object
        const sim = {
          icao: icao,
          lat: plane.latitude,
          lon: plane.longitude,
          targetLat: plane.latitude,
          targetLon: plane.longitude,
          heading: heading,
          speedMs: speedMs,
          speedKts: speedKts,
          onGround: plane.on_ground,
          color: color,
          isSelected: isSelected,
          marker: null,
          vectorLine: null,
        };

        // Aircraft Marker
        sim.marker = L.marker([sim.lat, sim.lon], {
          icon: L.divIcon({
            html: buildIconHtml(heading, color, isSelected),
            className: "aircraft-clean-marker",
            iconSize: [32, 32],
            iconAnchor: [16, 16],
          }),
        }).addTo(markersGroup);

        sim.marker.bindTooltip(tooltipContent, { direction: "top", offset: [0, -14], opacity: 0.95 });
        sim.marker.on("click", () => {
          if (onSelectPlane) onSelectPlane(plane);
        });

        // Direction Vector Line (Sleek forward leader line showing flight direction)
        if (!plane.on_ground) {
          sim.vectorLine = L.polyline(calcDirectionVector(sim.lat, sim.lon, heading, 24), {
            color: isSelected ? "#00e5ff" : color,
            weight: isSelected ? 2.5 : 1.5,
            opacity: isSelected ? 0.95 : 0.65,
            dashArray: "4, 6",
          }).addTo(vectorsGroup);
        }

        planesSimRef.current[icao] = sim;
      }
    });

    // Remove departed planes
    Object.keys(planesSimRef.current).forEach((icao) => {
      if (!currentIcaos.has(icao)) {
        const s = planesSimRef.current[icao];
        if (s.marker) markersGroup.removeLayer(s.marker);
        if (s.vectorLine) vectorsGroup.removeLayer(s.vectorLine);
        delete planesSimRef.current[icao];
      }
    });
  }, [aircraft, alerts, selectedPlane]);

  // 7b. Draw Real Flight Paths & Origin/Destination Airport Pins
  useEffect(() => {
    if (!mapInstanceRef.current || !routesLayerRef.current || !airportsLayerRef.current) return;
    const routesGroup = routesLayerRef.current;
    const airportsGroup = airportsLayerRef.current;
    routesGroup.clearLayers();
    airportsGroup.clearLayers();

    // Reset line references on simulated planes
    Object.values(planesSimRef.current).forEach((sim) => {
      sim.flownLine = null;
      sim.flownPoints = null;
      sim.remainingLine = null;
      sim.remainingPoints = null;
    });

    if (routeMode === "off") return;

    // Filter planes with routes
    let targets = [];
    if (routeMode === "all") {
      targets = aircraft.filter((p) => p.route && p.route.has_route);
    } else if (routeMode === "selected" && selectedPlane && selectedPlane.route && selectedPlane.route.has_route) {
      const match = aircraft.find((p) => p.icao24 === selectedPlane.icao24) || selectedPlane;
      targets = [match];
    }

    const renderedAirports = new Set();

    targets.forEach((plane) => {
      const r = plane.route;
      if (!r || !r.origin || !r.destination) return;
      const origin = r.origin;
      const dest = r.destination;
      const isSelected = selectedPlane && selectedPlane.icao24 === plane.icao24;
      const sim = planesSimRef.current[plane.icao24];
      const curLat = sim ? sim.lat : plane.latitude;
      const curLon = sim ? sim.lon : plane.longitude;

      // 1. Draw Origin Airport Pin (Start 🛫)
      const originKey = origin.iata || origin.icao;
      if (originKey && !renderedAirports.has(`orig-${originKey}`)) {
        renderedAirports.add(`orig-${originKey}`);
        const origMarker = L.marker([origin.lat, origin.lon], {
          icon: L.divIcon({
            html: `
              <div style="display:flex; flex-direction:column; align-items:center; cursor:pointer;">
                <div style="background:rgba(10,16,30,0.95); border:1.5px solid #00d4aa; color:#00d4aa; padding:2px 7px; border-radius:10px; font-size:10px; font-weight:800; font-family:monospace; box-shadow:0 0 10px rgba(0,212,170,0.5); white-space:nowrap;">
                  🛫 ${origin.iata || origin.code}
                </div>
                <div style="width:10px; height:10px; border-radius:50%; background:#00d4aa; border:2px solid #ffffff; box-shadow:0 0 8px #00d4aa; margin-top:2px;"></div>
              </div>
            `,
            className: "airport-custom-marker",
            iconSize: [60, 34],
            iconAnchor: [30, 30],
          }),
        }).addTo(airportsGroup);

        origMarker.bindTooltip(`
          <div style="font-family:var(--font-mono, monospace); font-size:11px; line-height:1.4;">
            <b style="color:#00d4aa; font-size:12px;">🛫 FLIGHT ORIGIN (STARTING AIRPORT)</b><br/>
            <b>${origin.name} (${origin.iata || origin.code})</b><br/>
            Location: <b>${origin.city}, ${origin.country}</b><br/>
            Status: <b>Departed Runway Sector</b>
          </div>
        `, { direction: "top", offset: [0, -10], opacity: 0.95 });

        origMarker.on("click", () => {
          if (mapInstanceRef.current) mapInstanceRef.current.panTo([origin.lat, origin.lon], { animate: true });
        });
      }

      // 2. Draw Destination Airport Pin (End 🛬)
      const destKey = dest.iata || dest.icao;
      if (destKey && !renderedAirports.has(`dest-${destKey}`)) {
        renderedAirports.add(`dest-${destKey}`);
        const destMarker = L.marker([dest.lat, dest.lon], {
          icon: L.divIcon({
            html: `
              <div style="display:flex; flex-direction:column; align-items:center; cursor:pointer;">
                <div style="background:rgba(10,16,30,0.95); border:1.5px solid #ff3366; color:#ff3366; padding:2px 7px; border-radius:10px; font-size:10px; font-weight:800; font-family:monospace; box-shadow:0 0 10px rgba(255,51,102,0.5); white-space:nowrap;">
                  🛬 ${dest.iata || dest.code}
                </div>
                <div style="width:10px; height:10px; border-radius:50%; background:#ff3366; border:2px solid #ffffff; box-shadow:0 0 8px #ff3366; margin-top:2px;"></div>
              </div>
            `,
            className: "airport-custom-marker",
            iconSize: [60, 34],
            iconAnchor: [30, 30],
          }),
        }).addTo(airportsGroup);

        destMarker.bindTooltip(`
          <div style="font-family:var(--font-mono, monospace); font-size:11px; line-height:1.4;">
            <b style="color:#ff3366; font-size:12px;">🛬 FLIGHT DESTINATION (ENDING AIRPORT)</b><br/>
            <b>${dest.name} (${dest.iata || dest.code})</b><br/>
            Location: <b>${dest.city}, ${dest.country}</b><br/>
            Status: <b>Target Arrival Aerodrome</b>
          </div>
        `, { direction: "top", offset: [0, -10], opacity: 0.95 });

        destMarker.on("click", () => {
          if (mapInstanceRef.current) mapInstanceRef.current.panTo([dest.lat, dest.lon], { animate: true });
        });
      }

      // 3. Traveled / Flown Segment (Solid Cyan Airway Line from Start to Current Plane)
      let flownPts = r.flown_waypoints && r.flown_waypoints.length >= 2
        ? r.flown_waypoints
        : [[origin.lat, origin.lon], [curLat, curLon]];
      flownPts = [...flownPts.slice(0, -1), [curLat, curLon]];

      const flownLine = L.polyline(flownPts, {
        color: isSelected ? "#00e5ff" : "rgba(0, 229, 255, 0.65)",
        weight: isSelected ? 3.5 : 2,
        opacity: isSelected ? 0.95 : 0.65,
      }).addTo(routesGroup);

      flownLine.bindTooltip(`
        <div style="font-family:var(--font-mono, monospace); font-size:11px;">
          <b style="color:#00e5ff;">${plane.callsign || plane.icao24}</b> Traveled Path<br/>
          From <b>${origin.iata}</b>: ${Math.round(r.traveled_km || 0)} km (${Math.round(r.progress_pct || 0)}% flown)
        </div>
      `, { sticky: true });

      // 4. Remaining Segment (Dashed Magenta/Coral Airway Corridor from Current Plane to End)
      let remPts = r.remaining_waypoints && r.remaining_waypoints.length >= 2
        ? r.remaining_waypoints
        : [[curLat, curLon], [dest.lat, dest.lon]];
      remPts = [[curLat, curLon], ...remPts.slice(1)];

      const remainingLine = L.polyline(remPts, {
        color: isSelected ? "#ff3366" : "rgba(255, 51, 102, 0.6)",
        weight: isSelected ? 2.5 : 1.5,
        opacity: isSelected ? 0.9 : 0.6,
        dashArray: "6, 8",
      }).addTo(routesGroup);

      remainingLine.bindTooltip(`
        <div style="font-family:var(--font-mono, monospace); font-size:11px;">
          <b style="color:#ff3366;">${plane.callsign || plane.icao24}</b> Remaining Path<br/>
          To <b>${dest.iata}</b>: ${Math.round(r.remaining_km || 0)} km remaining
        </div>
      `, { sticky: true });

      if (sim) {
        sim.flownLine = flownLine;
        sim.flownPoints = flownPts;
        sim.remainingLine = remainingLine;
        sim.remainingPoints = remPts;
      }
    });
  }, [aircraft, selectedPlane, routeMode]);

  // 8. Smooth 60-FPS Continuous Flight Motion Loop ("Move the Aeroplanes")
  useEffect(() => {
    let animId;

    const animateFlightMotion = () => {
      const now = performance.now();
      const dt = Math.min((now - lastTimeRef.current) / 1000, 0.1);
      lastTimeRef.current = now;

      if (motionSpeed > 0) {
        Object.values(planesSimRef.current).forEach((sim) => {
          if (!sim.onGround && sim.speedMs > 20) {
            // Forward kinematic flight motion along heading direction
            const distKm = (sim.speedMs * dt * motionSpeed) / 1000.0;
            const headingRad = ((sim.heading || 0) * Math.PI) / 180.0;
            const latRad = (sim.lat * Math.PI) / 180.0;

            const dLat = (distKm / 6371.0) * (180.0 / Math.PI) * Math.cos(headingRad);
            const dLon = ((distKm / 6371.0) * (180.0 / Math.PI) * Math.sin(headingRad)) / Math.cos(latRad);

            // Gentle convergence towards latest server ADS-B fix
            const nudgeLat = (sim.targetLat - sim.lat) * 0.15 * dt * motionSpeed;
            const nudgeLon = (sim.targetLon - sim.lon) * 0.15 * dt * motionSpeed;

            sim.lat += dLat + nudgeLat;
            sim.lon += dLon + nudgeLon;

            // Move aircraft marker
            if (sim.marker) {
              sim.marker.setLatLng([sim.lat, sim.lon]);
            }

            // Move direction leader line
            if (sim.vectorLine && showDirections) {
              sim.vectorLine.setLatLngs(calcDirectionVector(sim.lat, sim.lon, sim.heading, 24));
            }

            // Move flight route corridors dynamically with the moving plane!
            if (sim.flownLine && sim.flownPoints) {
              const updatedFlown = [...sim.flownPoints.slice(0, -1), [sim.lat, sim.lon]];
              sim.flownLine.setLatLngs(updatedFlown);
            }
            if (sim.remainingLine && sim.remainingPoints) {
              const updatedRemaining = [[sim.lat, sim.lon], ...sim.remainingPoints.slice(1)];
              sim.remainingLine.setLatLngs(updatedRemaining);
            }
          }
        });
      }

      animId = requestAnimationFrame(animateFlightMotion);
    };

    animId = requestAnimationFrame(animateFlightMotion);
    return () => cancelAnimationFrame(animId);
  }, [motionSpeed, showDirections]);

  return (
    <div className="radar-map-wrapper">
      {/* Top Map Control Strip */}
      <div className="map-toolbar-strip">
        <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
          <span style={{ fontSize: "11px", fontWeight: 700, color: "var(--cyan)", letterSpacing: "0.5px", display: "flex", alignItems: "center", gap: "6px" }}>
            <Icon name="Compass" size={13} color="var(--cyan)" /> MOTION:
          </span>
          <div style={{ display: "flex", alignItems: "center", gap: "3px", background: "rgba(12,20,36,0.8)", padding: "2px 4px", borderRadius: "6px", border: "1px solid var(--border-subtle)" }}>
            {[
              { label: "1X", val: 1, title: "Real-Time 1x Speed" },
              { label: "3X", val: 3, title: "Active Flight Glide (3x)" },
              { label: "8X", val: 8, title: "Fast-Forward Transit (8x)" },
              { label: "❚❚", val: 0, title: "Pause Motion" },
            ].map((sp) => (
              <button
                key={sp.val}
                title={sp.title}
                onClick={() => setMotionSpeed(sp.val)}
                style={{
                  background: motionSpeed === sp.val ? "var(--cyan)" : "transparent",
                  color: motionSpeed === sp.val ? "#000" : "var(--text-muted)",
                  border: "none",
                  borderRadius: "4px",
                  padding: "3px 8px",
                  fontSize: "10px",
                  fontWeight: 800,
                  cursor: "pointer",
                  transition: "all 0.15s ease",
                }}
              >
                {sp.label}
              </button>
            ))}
          </div>
        </div>

        <div style={{ display: "flex", alignItems: "center", gap: "10px", flexWrap: "wrap" }}>
          {/* Show Directions Toggle Button */}
          <button
            onClick={() => setShowDirections(!showDirections)}
            style={{
              display: "flex",
              alignItems: "center",
              gap: "6px",
              background: showDirections ? "rgba(0, 229, 255, 0.18)" : "rgba(12,20,36,0.8)",
              borderColor: showDirections ? "var(--cyan)" : "var(--border-subtle)",
              color: showDirections ? "var(--cyan)" : "var(--text-muted)",
              border: "1px solid",
              borderRadius: "6px",
              padding: "4px 10px",
              fontSize: "11px",
              fontWeight: 700,
              cursor: "pointer",
              transition: "all 0.15s ease",
            }}
            title="Toggle Forward Flight Direction Vectors"
          >
            <Icon name="Navigation" size={12} />
            Directions: {showDirections ? "ON" : "OFF"}
          </button>

          {/* Route Corridors Toggle Button */}
          <button
            onClick={() => setRouteMode((prev) => (prev === "selected" ? "all" : prev === "all" ? "off" : "selected"))}
            style={{
              display: "flex",
              alignItems: "center",
              gap: "6px",
              background: routeMode !== "off" ? "rgba(168, 85, 247, 0.18)" : "rgba(12,20,36,0.8)",
              borderColor: routeMode !== "off" ? "#a855f7" : "var(--border-subtle)",
              color: routeMode !== "off" ? "#c084fc" : "var(--text-muted)",
              border: "1px solid",
              borderRadius: "6px",
              padding: "4px 10px",
              fontSize: "11px",
              fontWeight: 700,
              cursor: "pointer",
              transition: "all 0.15s ease",
            }}
            title="Toggle Start-to-End Flight Routes (Selected Flight / All Flights / OFF)"
          >
            <Icon name="Route" size={12} />
            Routes: {routeMode === "selected" ? "Selected Flight" : routeMode === "all" ? "All Corridors" : "OFF"}
          </button>

          {/* Map API Key Configuration Button */}
          <button
            onClick={() => setShowKeyModal(true)}
            style={{
              display: "flex",
              alignItems: "center",
              gap: "6px",
              background: hasApiKey ? "rgba(0, 212, 170, 0.18)" : "rgba(245, 158, 11, 0.18)",
              borderColor: hasApiKey ? "var(--green)" : "var(--amber)",
              color: hasApiKey ? "var(--green)" : "var(--amber)",
              border: "1px solid",
              borderRadius: "6px",
              padding: "4px 10px",
              fontSize: "11px",
              fontWeight: 700,
              cursor: "pointer",
              transition: "all 0.15s ease",
            }}
            title="Configure Map API Key (Mapbox Access Token / MapTiler Key)"
          >
            <Icon name="Key" size={12} />
            {hasApiKey ? "Map API Key: ACTIVE ✓" : "🔑 Set Map API Key"}
          </button>

          {/* Active Provider Tag */}
          <span style={{ fontSize: "10px", color: hasApiKey ? "var(--cyan)" : "var(--green)", background: "rgba(12,20,36,0.8)", border: "1px solid var(--border-subtle)", padding: "4px 8px", borderRadius: "5px", fontWeight: 700 }}>
            {hasApiKey ? `✓ ${keyProvider.toUpperCase()} Premium Tiles` : "✓ Open Basemap (Free)"}
          </span>
        </div>
      </div>

      {/* MAP CANVAS */}
      <div ref={mapContainerRef} className="radar-map-element" />

      {/* FLOATING REAL FLIGHT ROUTE HUD OVERLAY (Start ➔ Current Plane ➔ End Destination) */}
      {selectedPlane && selectedPlane.route && selectedPlane.route.has_route && routeMode !== "off" && (
        <div className="flight-route-hud">
          {/* HUD Header */}
          <div className="route-hud-header">
            <div className="route-hud-callsign">
              <span style={{ fontSize: "20px" }}>✈️</span>
              <div>
                <h4 style={{ margin: 0, display: "flex", alignItems: "center", gap: "8px" }}>
                  {selectedPlane.callsign || selectedPlane.icao24}
                  <span style={{ fontSize: "11px", fontWeight: 700, color: "var(--cyan)", background: "rgba(0, 229, 255, 0.12)", padding: "1px 6px", borderRadius: "4px", fontFamily: "var(--font-mono)" }}>
                    {selectedPlane.route.route_code}
                  </span>
                </h4>
                <span style={{ fontSize: "11px", color: "var(--text-muted)" }}>
                  {selectedPlane.aircraft_type ? `${selectedPlane.aircraft_type} • ` : ""}
                  {selectedPlane.flight_level || (selectedPlane.baro_altitude ? `FL${Math.round(selectedPlane.baro_altitude * 3.28084 / 100)}` : "FL--")} • {selectedPlane.speed_kts || Math.round((selectedPlane.velocity || 0) * 1.94384)} kts
                </span>
              </div>
            </div>

            <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
              <span className="badge-route" title="Current Heading Direction">
                <Icon name="Navigation" size={12} /> {fmtHdg(selectedPlane.heading)}
              </span>
              <button
                onClick={() => { if (onSelectPlane) onSelectPlane(null); }}
                style={{ background: "rgba(255,255,255,0.08)", border: "none", color: "#94a3b8", borderRadius: "50%", width: "22px", height: "22px", cursor: "pointer", display: "flex", alignItems: "center", justifyContent: "center" }}
                title="Dismiss Route HUD"
              >
                <Icon name="X" size={12} />
              </button>
            </div>
          </div>

          {/* Airport Corridor & Animated Progress */}
          <div className="route-hud-corridor">
            {/* Origin Airport (Start) */}
            <div className="route-apt-block" style={{ textAlign: "left", minWidth: "120px" }}>
              <span className="route-apt-tag" style={{ color: "var(--green)" }}>🛫 START (ORIGIN)</span>
              <div className="route-apt-code" style={{ color: "var(--green)" }}>
                {selectedPlane.route.origin?.iata || selectedPlane.route.origin?.code || "ORIGIN"}
              </div>
              <div className="route-apt-name" title={selectedPlane.route.origin?.name}>
                {selectedPlane.route.origin?.city || selectedPlane.route.origin?.name || "Departure"}
              </div>
            </div>

            {/* Middle: Traveled vs Remaining Progress Track */}
            <div className="route-mid-visual">
              <div style={{ display: "flex", justifyContent: "space-between", width: "100%", fontSize: "11px" }}>
                <span style={{ color: "var(--green)", fontWeight: 700 }}>
                  {selectedPlane.route.traveled_km ? `${Math.round(selectedPlane.route.traveled_km)} km flown` : "Flown"}
                </span>
                <span style={{ color: "var(--cyan)", fontWeight: 800, fontFamily: "var(--font-mono)" }}>
                  {selectedPlane.route.progress_pct !== undefined ? `${selectedPlane.route.progress_pct}%` : "50%"}
                </span>
                <span style={{ color: "var(--crimson)", fontWeight: 700 }}>
                  {selectedPlane.route.remaining_km ? `${Math.round(selectedPlane.route.remaining_km)} km remaining` : "Remaining"}
                </span>
              </div>

              <div className="route-progress-track">
                <div
                  className="route-progress-fill"
                  style={{ width: `${Math.min(Math.max(selectedPlane.route.progress_pct || 0, 5), 100)}%` }}
                />
              </div>

              <div className="route-progress-labels">
                <span>Departed</span>
                <span style={{ color: "var(--sky)", display: "flex", alignItems: "center", gap: "4px" }}>
                  <Icon name="Navigation" size={10} /> En Route • Track {Math.round(selectedPlane.heading || 0)}° ({getCardinalDirection(selectedPlane.heading)})
                </span>
                <span>Destination</span>
              </div>
            </div>

            {/* Destination Airport (End) */}
            <div className="route-apt-block" style={{ textAlign: "right", minWidth: "120px" }}>
              <span className="route-apt-tag" style={{ color: "var(--crimson)" }}>🛬 END (DESTINATION)</span>
              <div className="route-apt-code" style={{ color: "var(--crimson)" }}>
                {selectedPlane.route.destination?.iata || selectedPlane.route.destination?.code || "DEST"}
              </div>
              <div className="route-apt-name" title={selectedPlane.route.destination?.name}>
                {selectedPlane.route.destination?.city || selectedPlane.route.destination?.name || "Arrival"}
              </div>
            </div>
          </div>

          {/* Route Metrics Bottom Bar */}
          <div className="route-metrics-bar">
            <div className="route-metric-item">
              <Icon name="Compass" size={13} color="var(--cyan)" />
              <span>Bearing to Dest: <b>{selectedPlane.route.bearing_to_dest ? `${selectedPlane.route.bearing_to_dest}° (${getCardinalDirection(selectedPlane.route.bearing_to_dest)})` : "Direct"}</b></span>
            </div>
            <div className="route-metric-item">
              <Icon name="Activity" size={13} color="var(--green)" />
              <span>Total Distance: <b>{selectedPlane.route.total_km ? `${Math.round(selectedPlane.route.total_km)} km` : "N/A"}</b></span>
            </div>
            {selectedPlane.route.eta_minutes !== undefined && (
              <div className="route-metric-item">
                <Icon name="Clock" size={13} color="var(--amber)" />
                <span>En-Route ETA: <b>~{Math.floor(selectedPlane.route.eta_minutes / 60)}h {selectedPlane.route.eta_minutes % 60}m</b></span>
              </div>
            )}
            <div className="route-metric-item" style={{ marginLeft: "auto", fontSize: "11px", color: "var(--text-muted)" }}>
              <span>Trajectory: <b>Great-Circle Airway Corridor</b></span>
            </div>
          </div>
        </div>
      )}

      {/* MAP API KEY CONFIGURATION MODAL */}
      {showKeyModal && (
        <div
          style={{
            position: "fixed",
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            background: "rgba(0, 0, 0, 0.75)",
            backdropFilter: "blur(6px)",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            zIndex: 99999,
            padding: "20px",
          }}
          onClick={(e) => {
            if (e.target === e.currentTarget) setShowKeyModal(false);
          }}
        >
          <div
            className="glass-panel"
            style={{
              width: "100%",
              maxWidth: "520px",
              background: "rgba(10, 16, 30, 0.98)",
              border: "1px solid var(--border-subtle)",
              padding: "24px",
              boxShadow: "0 20px 50px rgba(0, 0, 0, 0.8)",
            }}
          >
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "16px" }}>
              <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
                <Icon name="Key" size={20} color="var(--cyan)" />
                <h3 style={{ fontSize: "16px", fontWeight: 800, color: "#fff", margin: 0 }}>
                  Map API Key Configuration
                </h3>
              </div>
              <button
                onClick={() => setShowKeyModal(false)}
                style={{ background: "transparent", border: "none", color: "var(--text-muted)", cursor: "pointer" }}
              >
                <Icon name="X" size={18} />
              </button>
            </div>

            <p style={{ fontSize: "12px", color: "var(--text-muted)", lineHeight: 1.6, marginBottom: "16px" }}>
              AeroGuardian AI operates with <b>100% free Esri Dark Aerospace tiles (no key needed)</b>. To enable CARTO Dark or vector styling, you can enter a free <b>CARTO Key</b>, <b>Mapbox Token</b>, or <b>MapTiler Key</b> below.
            </p>

            {/* Provider Tabs */}
            <div style={{ display: "flex", gap: "8px", marginBottom: "14px" }}>
              {[
                { id: "carto", label: "CARTO (Free Key)" },
                { id: "mapbox", label: "Mapbox" },
                { id: "maptiler", label: "MapTiler" },
                { id: "custom", label: "Custom Key" },
              ].map((p) => (
                <button
                  key={p.id}
                  onClick={() => setKeyProvider(p.id)}
                  style={{
                    flex: 1,
                    padding: "6px 10px",
                    fontSize: "11px",
                    fontWeight: 700,
                    borderRadius: "6px",
                    border: "1px solid",
                    borderColor: keyProvider === p.id ? "var(--cyan)" : "var(--border-subtle)",
                    background: keyProvider === p.id ? "rgba(0, 229, 255, 0.15)" : "rgba(15, 23, 42, 0.5)",
                    color: keyProvider === p.id ? "var(--cyan)" : "var(--text-muted)",
                    cursor: "pointer",
                  }}
                >
                  {p.label}
                </button>
              ))}
            </div>

            {/* Input Field */}
            <div style={{ marginBottom: "16px" }}>
              <label style={{ display: "block", fontSize: "11px", fontWeight: 700, color: "#94a3b8", marginBottom: "6px" }}>
                {keyProvider === "carto"
                  ? "CARTO API Key (Free at carto.com/basemaps/apikey):"
                  : (keyProvider === "mapbox" ? "Mapbox Public Access Token (starts with pk.):" : `${keyProvider.toUpperCase()} API Key:`)}
              </label>
              <input
                type="text"
                value={keyInput}
                onChange={(e) => setKeyInput(e.target.value)}
                placeholder={keyProvider === "carto" ? "Enter free CARTO API key..." : (keyProvider === "mapbox" ? "pk.eyJ1IjoieW91ci11c2VybmFtZSIsImEiOiJ..." : "Enter your API key...")}
                style={{
                  width: "100%",
                  padding: "10px 12px",
                  background: "rgba(7, 11, 19, 0.8)",
                  border: "1px solid var(--border-subtle)",
                  borderRadius: "6px",
                  color: "#f1f5f9",
                  fontSize: "12px",
                  fontFamily: "var(--font-mono)",
                  outline: "none",
                }}
              />
              <div style={{ fontSize: "10px", color: "var(--text-muted)", marginTop: "4px" }}>
                {keyProvider === "mapbox" && "Free token available at https://account.mapbox.com"}
                {keyProvider === "maptiler" && "Free key available at https://cloud.maptiler.com"}
              </div>
            </div>

            {/* Save Status Alert */}
            {saveStatus && (
              <div
                style={{
                  padding: "8px 12px",
                  borderRadius: "6px",
                  fontSize: "11px",
                  fontWeight: 700,
                  marginBottom: "14px",
                  background: saveStatus.type === "success" ? "rgba(0, 212, 170, 0.15)" : "rgba(255, 51, 102, 0.15)",
                  color: saveStatus.type === "success" ? "var(--green)" : "var(--crimson)",
                  border: `1px solid ${saveStatus.type === "success" ? "var(--green)" : "var(--crimson)"}`,
                }}
              >
                {saveStatus.msg}
              </div>
            )}

            {/* Action Buttons */}
            <div style={{ display: "flex", justifyContent: "space-between", gap: "10px" }}>
              <button
                onClick={() => handleSaveApiKey(true)}
                disabled={savingKey}
                style={{
                  padding: "8px 14px",
                  fontSize: "11px",
                  background: "transparent",
                  border: "1px solid var(--border-subtle)",
                  color: "var(--text-muted)",
                  borderRadius: "6px",
                  cursor: "pointer",
                }}
              >
                Clear Key (Use Free Basemap)
              </button>

              <div style={{ display: "flex", gap: "8px" }}>
                <button
                  onClick={() => setShowKeyModal(false)}
                  style={{
                    padding: "8px 14px",
                    fontSize: "11px",
                    background: "transparent",
                    border: "1px solid var(--border-subtle)",
                    color: "#f1f5f9",
                    borderRadius: "6px",
                    cursor: "pointer",
                  }}
                >
                  Cancel
                </button>
                <button
                  onClick={() => handleSaveApiKey(false)}
                  disabled={savingKey}
                  className="btn-primary"
                  style={{ padding: "8px 18px", fontSize: "11px" }}
                >
                  <Icon name="Check" size={13} /> {savingKey ? "Saving..." : "Save & Activate Key"}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};


// ============================================================
// 5. WORKLOAD GAUGE (SVG Research Prototype Visualizer)
// ============================================================

const WorkloadGauge = ({ score = 0, level = "LOW" }) => {
  const radius = 80;
  const stroke = 14;
  const normalizedRadius = radius - stroke * 2;
  const circumference = normalizedRadius * 2 * Math.PI;
  const strokeDashoffset = circumference - (score / 100) * circumference;

  let color = "#00d4aa";
  if (score >= 75) color = "#ff3366";
  else if (score >= 50) color = "#f59e0b";
  else if (score >= 28) color = "#fbbf24";

  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", position: "relative" }}>
      <svg height={radius * 2} width={radius * 2} style={{ transform: "rotate(-90deg)" }}>
        <circle
          stroke="rgba(30, 41, 59, 0.6)"
          fill="transparent"
          strokeWidth={stroke}
          r={normalizedRadius}
          cx={radius}
          cy={radius}
        />
        <circle
          stroke={color}
          fill="transparent"
          strokeWidth={stroke}
          strokeDasharray={`${circumference} ${circumference}`}
          style={{ strokeDashoffset, transition: "stroke-dashoffset 0.8s ease, stroke 0.4s ease" }}
          strokeLinecap="round"
          r={normalizedRadius}
          cx={radius}
          cy={radius}
        />
      </svg>
      <div style={{ position: "absolute", textAlign: "center" }}>
        <div style={{ fontSize: "28px", fontWeight: 800, color: "#fff", fontFamily: "var(--font-mono)" }}>
          {score}%
        </div>
        <div style={{ fontSize: "11px", fontWeight: 700, color, letterSpacing: "1px" }}>
          {level}
        </div>
      </div>
    </div>
  );
};


// ============================================================
// 6. MASTER APP COMPONENT
// ============================================================

function App() {
  const [activeTab, setActiveTab] = useState("welcome");
  const [region, setRegion] = useState("India");
  const [aircraft, setAircraft] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [alertCounts, setAlertCounts] = useState({ CRITICAL: 0, HIGH: 0, MEDIUM: 0, LOW: 0 });
  const [weatherStations, setWeatherStations] = useState([]);
  const [workload, setWorkload] = useState({ workload_index: 0, level: "LOW", contributing_factors: [] });
  const [situation, setSituation] = useState({ summary_text: "Loading live airspace telemetry..." });
  const [systemStatus, setSystemStatus] = useState(null);
  
  const [selectedPlane, setSelectedPlane] = useState(null);
  const [planeDiagnostic, setPlaneDiagnostic] = useState(null);
  const [selectedWxIcao, setSelectedWxIcao] = useState("VIDP");
  const [stationWx, setStationWx] = useState(null);

  // Settings & Toggles
  const [autoRefresh, setAutoRefresh] = useState(true);
  const [refreshCountdown, setRefreshCountdown] = useState(15);
  const [audioAlerts, setAudioAlerts] = useState(true);
  const [showRadarSweep, setShowRadarSweep] = useState(true);
  const [loading, setLoading] = useState(false);
  const [dashboardLayout, setDashboardLayout] = useState("split"); // "split" | "full"

  // Assistant Chat State
  const [chatMessages, setChatMessages] = useState([
    {
      role: "assistant",
      content: "Hello! I am AeroGuardian AI's decision-support assistant. I continuously monitor real-time OpenSky aircraft telemetry and NOAA Aviation Weather Center reports. Ask me about monitored flights, active priority alerts, or workload conditions.",
    },
  ]);
  const [inputQuery, setInputQuery] = useState("");
  const [chatLoading, setChatLoading] = useState(false);

  // Search & Filter States
  const [searchFilter, setSearchFilter] = useState("");
  const [statusFilter, setStatusFilter] = useState("ALL");
  const [phaseFilter, setPhaseFilter] = useState("ALL");
  const [priorityFilter, setPriorityFilter] = useState("ALL");
  const [checkedChecklists, setCheckedChecklists] = useState({});

  const toggleChecklistItem = (key) => {
    setCheckedChecklists((prev) => ({
      ...prev,
      [key]: !prev[key],
    }));
  };

  // Fetch All Operational Data
  const fetchData = useCallback(async (force = false) => {
    setLoading(true);
    try {
      // 1. Telemetry
      const resAcft = await fetch(`/api/aircraft?region=${region}&refresh=${force}`);
      const dataAcft = await resAcft.json();
      setAircraft(dataAcft.aircraft || []);

      // 2. Weather Overview
      const resWx = await fetch(`/api/weather/overview`);
      const dataWx = await resWx.json();
      setWeatherStations(dataWx.stations || []);

      // 3. Alerts
      const resAlerts = await fetch(`/api/alerts?priority=ALL&include_acknowledged=true`);
      const dataAlerts = await resAlerts.json();
      setAlerts(dataAlerts.alerts || []);
      if (dataAlerts.counts) setAlertCounts(dataAlerts.counts);

      // Play audio chime if critical/high alert exists
      if (audioAlerts && dataAlerts.counts && (dataAlerts.counts.CRITICAL > 0 || dataAlerts.counts.HIGH > 0)) {
        playCautionChime();
      }

      // 4. Workload
      const resWl = await fetch(`/api/workload`);
      const dataWl = await resWl.json();
      setWorkload(dataWl);

      // 5. Situation
      const resSit = await fetch(`/api/situation`);
      const dataSit = await resSit.json();
      setSituation(dataSit);

      // 6. Status
      const resStat = await fetch(`/api/status`);
      const dataStat = await resStat.json();
      setSystemStatus(dataStat);
    } catch (err) {
      console.error("Data pipeline fetch error:", err);
    } finally {
      setLoading(false);
      setRefreshCountdown(15);
    }
  }, [region, audioAlerts]);

  // Initial Load
  useEffect(() => {
    fetchData(false);
  }, [fetchData]);

  // Auto-refresh countdown timer
  useEffect(() => {
    if (!autoRefresh) return;
    const interval = setInterval(() => {
      setRefreshCountdown((prev) => {
        if (prev <= 1) {
          fetchData(false);
          return 15;
        }
        return prev - 1;
      });
    }, 1000);
    return () => clearInterval(interval);
  }, [autoRefresh, fetchData]);

  // Fetch Station Weather when requested
  useEffect(() => {
    if (!selectedWxIcao) return;
    fetch(`/api/weather/station/${selectedWxIcao}`)
      .then((r) => r.json())
      .then((data) => setStationWx(data))
      .catch((e) => console.error(e));
  }, [selectedWxIcao]);

  // Fetch Aircraft Diagnostic when selected
  useEffect(() => {
    if (!selectedPlane) {
      setPlaneDiagnostic(null);
      return;
    }
    fetch(`/api/aircraft/${selectedPlane.icao24}/diagnostic`)
      .then((r) => r.json())
      .then((d) => setPlaneDiagnostic(d))
      .catch((e) => console.error(e));
  }, [selectedPlane]);

  // Acknowledge alert handler
  const handleAcknowledge = async (alertId, isAck) => {
    const endpoint = isAck ? `/api/alerts/${alertId}/unacknowledge` : `/api/alerts/${alertId}/acknowledge`;
    await fetch(endpoint, { method: "POST" });
    fetchData(false);
  };

  // Assistant Send
  const handleSendAssistant = async (queryText) => {
    const q = queryText || inputQuery;
    if (!q.trim()) return;

    const newMsgs = [...chatMessages, { role: "user", content: q }];
    setChatMessages(newMsgs);
    setInputQuery("");
    setChatLoading(true);

    try {
      const res = await fetch("/api/assistant", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: q }),
      });
      const data = await res.json();
      setChatMessages([...newMsgs, { role: "assistant", content: data.response }]);
    } catch (e) {
      setChatMessages([...newMsgs, { role: "assistant", content: "Error communicating with AI assistant." }]);
    } finally {
      setChatLoading(false);
    }
  };

  // CSV Export
  const exportTelemetryCSV = () => {
    if (!aircraft.length) return;
    const headers = ["Callsign", "ICAO24", "Country", "Latitude", "Longitude", "Altitude_m", "Speed_ms", "Heading_deg", "Vertical_Rate_ms", "Squawk", "On_Ground"];
    const rows = aircraft.map((p) => [
      p.callsign || "N/A",
      p.icao24,
      p.country,
      p.latitude,
      p.longitude,
      p.baro_altitude,
      p.velocity,
      p.heading,
      p.vertical_rate,
      p.squawk || "N/A",
      p.on_ground,
    ]);
    const csvContent = "data:text/csv;charset=utf-8," + [headers.join(","), ...rows.map((e) => e.join(","))].join("\n");
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", `aeroguardian_telemetry_${Date.now()}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  // Filtered Aircraft
  const filteredAircraft = useMemo(() => {
    return aircraft.filter((p) => {
      const q = searchFilter.toLowerCase();
      const matchSearch =
        !q ||
        (p.callsign && p.callsign.toLowerCase().includes(q)) ||
        (p.icao24 && p.icao24.toLowerCase().includes(q)) ||
        (p.country && p.country.toLowerCase().includes(q));

      let matchStatus = true;
      if (statusFilter === "AIRBORNE") matchStatus = !p.on_ground;
      else if (statusFilter === "GROUND") matchStatus = p.on_ground;
      else if (statusFilter === "ATTENTION") {
        matchStatus = alerts.some((a) => a.icao24 === p.icao24);
      }

      let matchPhase = true;
      if (phaseFilter !== "ALL") {
        const code = p.flight_phase?.code || (p.on_ground ? "GROUND" : "CRUISE");
        if (phaseFilter === "CRUISE") matchPhase = code === "CRUISE" || code === "LEVEL";
        else if (phaseFilter === "CLIMB") matchPhase = code === "CLIMB" || code === "TAKEOFF";
        else if (phaseFilter === "DESCENT") matchPhase = code === "DESCENT" || code === "APPROACH";
        else if (phaseFilter === "GROUND") matchPhase = code === "GROUND";
      }

      return matchSearch && matchStatus && matchPhase;
    });
  }, [aircraft, searchFilter, statusFilter, phaseFilter, alerts]);


  // ============================================================
  // RENDER SECTIONS
  // ============================================================

  return (
    <div className="app-container">
      {/* SIDEBAR NAVIGATION */}
      <aside className="sidebar">
        <div className="brand-header">
          <div className="brand-logo-icon">
            <Icon name="Shield" size={22} color="#fff" />
          </div>
          <div className="brand-text">
            <h1>AeroGuardian</h1>
            <p>AI Human-Factor Guardian</p>
          </div>
        </div>

        <div className="theme-tag">
          <b>Theme:</b> Smart Systems for a Safer Future in Aviation
        </div>

        {/* Navigation Items */}
        <ul className="nav-list">
          {[
            { id: "welcome", label: "Welcome & Mission", icon: "Home" },
            { id: "dashboard", label: "Mission Dashboard", icon: "Activity" },
            { id: "aircraft", label: "Live Aircraft", icon: "Plane", badge: aircraft.length },
            { id: "weather", label: "Aviation Weather", icon: "Wind" },
            { id: "guardian", label: "AI Guardian", icon: "Shield" },
            { id: "workload", label: "Workload Analysis", icon: "Gauge" },
            { id: "alerts", label: "Alert Center", icon: "AlertTriangle", badge: alerts.length, isCrit: alertCounts.CRITICAL > 0 },
            { id: "analytics", label: "Analytics", icon: "BarChart3" },
            { id: "assistant", label: "AI Assistant", icon: "Terminal" },
            { id: "about", label: "About", icon: "Info" },
          ].map((item) => (
            <li key={item.id}>
              <button
                className={`nav-item-btn ${activeTab === item.id ? "active" : ""}`}
                onClick={() => setActiveTab(item.id)}
              >
                <Icon name={item.icon} size={17} color={activeTab === item.id ? "var(--cyan)" : "var(--text-muted)"} />
                <span>{item.label}</span>
                {item.badge !== undefined && (
                  <span className={`nav-badge ${item.isCrit ? "badge-crit" : ""}`}>
                    {item.badge}
                  </span>
                )}
              </button>
            </li>
          ))}
        </ul>

        {/* Sidebar Controls */}
        <div className="sidebar-footer">
          <div className="control-pill">
            <span>Airspace Region</span>
            <select
              value={region}
              onChange={(e) => setRegion(e.target.value)}
              style={{ padding: "4px 8px", fontSize: "11px" }}
            >
              <option value="India">India</option>
              <option value="Global">Global</option>
              <option value="Europe">Europe</option>
              <option value="North America">North America</option>
              <option value="Southeast Asia">Southeast Asia</option>
              <option value="Middle East">Middle East</option>
            </select>
          </div>

          <div className="control-pill">
            <span>Auto-Refresh ({refreshCountdown}s)</span>
            <button
              onClick={() => setAutoRefresh(!autoRefresh)}
              style={{ background: "transparent", border: "none", color: autoRefresh ? "var(--cyan)" : "var(--text-muted)", cursor: "pointer" }}
            >
              <Icon name={autoRefresh ? "RefreshCw" : "X"} size={14} />
            </button>
          </div>

          <div className="control-pill">
            <span>Avionics Chime</span>
            <button
              onClick={() => setAudioAlerts(!audioAlerts)}
              style={{ background: "transparent", border: "none", color: audioAlerts ? "var(--green)" : "var(--crimson)", cursor: "pointer" }}
            >
              <Icon name={audioAlerts ? "Volume2" : "VolumeX"} size={15} />
            </button>
          </div>

          <button className="btn-primary" style={{ width: "100%", justifyContent: "center" }} onClick={() => fetchData(true)}>
            <Icon name="RefreshCw" size={14} /> {loading ? "Updating..." : "Force Refresh"}
          </button>
        </div>
      </aside>

      {/* MAIN WRAPPER */}
      <main className="main-wrapper">
        {/* Top Header */}
        <header className="top-header">
          <div className="header-left">
            <div className="header-title-block">
              <h2>AeroGuardian AI Decision Support</h2>
              <p>Pilot Workload & Information Overload Guardian • {region} Airspace</p>
            </div>
          </div>

          <div className="header-right">
            {/* Status Pills */}
            <span className="status-tag status-tag-ok">
              <Icon name="Radio" size={12} color="var(--green)" /> OpenSky: Connected
            </span>
            <span className="status-tag status-tag-ok">
              <Icon name="CloudRain" size={12} color="var(--green)" /> NOAA AWC: Live
            </span>
            <span className="status-tag status-tag-ok">
              <Icon name="Cpu" size={12} color="var(--green)" /> AI Engine: Active
            </span>
          </div>
        </header>

        {/* Page Content */}
        <div className="page-content">
          {/* Permanent Academic Disclaimer Banner */}
          <div className="safety-disclaimer-strip">
            <Icon name="AlertTriangle" size={18} color="var(--cyan)" />
            <span>
              <b>ACADEMIC & RESEARCH DISCLAIMER:</b> AeroGuardian AI is an educational and human-factor decision-support prototype.
              It is <b>not certified aviation software</b> and must never be used for aircraft flight control or operational clearances.
              All observations use cautious scientific framing (<i>'Potential concern detected'</i>, <i>'Further verification recommended'</i>).
            </span>
          </div>

          {/* ========================================================
              TAB 0: WELCOME & MISSION OVERVIEW
             ======================================================== */}
          {activeTab === "welcome" && (
            <div className="welcome-container">
              {/* Hero Banner */}
              <div className="welcome-hero">
                <div className="welcome-hero-badge">
                  <Icon name="Shield" size={14} color="var(--cyan)" />
                  <span>AEROGUARDIAN AI v3.2 • HUMAN-FACTOR FLIGHT SAFETY</span>
                </div>
                <h1 className="welcome-hero-title">
                  Next-Generation Airspace Guardian &amp; Pilot Decision Support
                </h1>
                <p className="welcome-hero-desc">
                  Welcome to <b>AeroGuardian AI</b> — an intelligent aeronautical decision-support system designed to mitigate pilot and air traffic controller cognitive overload. Fusing real-time Mode-S / ADS-B transponder telemetry with official NOAA Aviation Weather observations, AeroGuardian AI delivers continuous conflict prediction, situational awareness, and intelligent human-factor safety guardrails.
                </p>

                {/* Primary Action Buttons */}
                <div className="welcome-cta-group">
                  <button className="welcome-btn-primary" onClick={() => setActiveTab("dashboard")}>
                    <Icon name="Activity" size={16} color="#070b13" /> Launch Mission Dashboard
                    <Icon name="ArrowRight" size={15} color="#070b13" />
                  </button>
                  <button className="welcome-btn-secondary" onClick={() => setActiveTab("aircraft")}>
                    <Icon name="Plane" size={16} color="var(--cyan)" /> Live Aircraft Radar ({aircraft.length})
                  </button>
                  <button className="welcome-btn-secondary" onClick={() => setActiveTab("guardian")}>
                    <Icon name="Shield" size={16} color="var(--green)" /> AI Guardian Reasoner
                  </button>
                  <button className="welcome-btn-secondary" onClick={() => setActiveTab("assistant")}>
                    <Icon name="Terminal" size={16} color="var(--sky)" /> Aviation Copilot
                  </button>
                </div>

                {/* Airspace Quick Selectors */}
                <div style={{ marginTop: "20px", display: "flex", alignItems: "center", gap: "10px", flexWrap: "wrap", fontSize: "12px", color: "var(--text-muted)" }}>
                  <span style={{ fontWeight: 600, color: "#cbd5e1" }}>Quick Launch Airspace:</span>
                  {["India", "North America", "Europe", "Southeast Asia", "Middle East", "Global"].map((r) => (
                    <button
                      key={r}
                      onClick={() => {
                        setRegion(r);
                        setActiveTab("dashboard");
                      }}
                      style={{
                        background: region === r ? "rgba(0, 229, 255, 0.2)" : "rgba(15, 23, 42, 0.8)",
                        border: region === r ? "1px solid var(--cyan)" : "1px solid var(--border-subtle)",
                        color: region === r ? "var(--cyan)" : "#cbd5e1",
                        padding: "4px 10px",
                        borderRadius: "14px",
                        cursor: "pointer",
                        fontSize: "11px",
                        fontWeight: 600,
                        transition: "all 0.15s ease",
                      }}
                    >
                      {r}
                    </button>
                  ))}
                </div>
              </div>

              {/* Live Airspace Readiness Stat Strip */}
              <div className="welcome-stat-strip">
                <div className="welcome-stat-card">
                  <div className="welcome-stat-icon-box" style={{ background: "rgba(0, 229, 255, 0.12)", color: "var(--cyan)" }}>
                    <Icon name="Plane" size={22} color="var(--cyan)" />
                  </div>
                  <div>
                    <div className="welcome-stat-val">{aircraft.length}</div>
                    <div className="welcome-stat-label">Live Aircraft ({region})</div>
                  </div>
                </div>

                <div className="welcome-stat-card">
                  <div className="welcome-stat-icon-box" style={{ background: "rgba(0, 212, 170, 0.12)", color: "var(--green)" }}>
                    <Icon name="Activity" size={22} color="var(--green)" />
                  </div>
                  <div>
                    <div className="welcome-stat-val">{aircraft.filter((p) => !p.on_ground).length}</div>
                    <div className="welcome-stat-label">Airborne Transponders ({aircraft.filter((p) => p.on_ground).length} Ground)</div>
                  </div>
                </div>

                <div className="welcome-stat-card">
                  <div className="welcome-stat-icon-box" style={{ background: alertCounts.CRITICAL > 0 ? "rgba(255, 51, 102, 0.15)" : "rgba(245, 158, 11, 0.15)", color: alertCounts.CRITICAL > 0 ? "var(--crimson)" : "var(--amber)" }}>
                    <Icon name="AlertTriangle" size={22} color={alertCounts.CRITICAL > 0 ? "var(--crimson)" : "var(--amber)"} />
                  </div>
                  <div>
                    <div className="welcome-stat-val" style={{ color: alertCounts.CRITICAL > 0 ? "var(--crimson)" : "#fff" }}>
                      {alerts.length}
                    </div>
                    <div className="welcome-stat-label">Active Safety Cautions ({alertCounts.CRITICAL} Crit)</div>
                  </div>
                </div>

                <div className="welcome-stat-card">
                  <div className="welcome-stat-icon-box" style={{ background: workload.workload_index >= 75 ? "rgba(255, 51, 102, 0.15)" : "rgba(56, 189, 248, 0.12)", color: workload.workload_index >= 75 ? "var(--crimson)" : "var(--sky)" }}>
                    <Icon name="Gauge" size={22} color={workload.workload_index >= 75 ? "var(--crimson)" : "var(--sky)"} />
                  </div>
                  <div>
                    <div className="welcome-stat-val" style={{ color: workload.workload_index >= 75 ? "var(--crimson)" : "#fff" }}>
                      {workload.workload_index}%
                    </div>
                    <div className="welcome-stat-label">Cognitive Workload ({workload.level})</div>
                  </div>
                </div>
              </div>

              {/* Core Aerospace Decision-Support Modules */}
              <div>
                <h3 style={{ fontSize: "16px", fontWeight: 700, marginBottom: "14px", display: "flex", alignItems: "center", gap: "8px" }}>
                  <Icon name="Compass" size={18} color="var(--cyan)" /> Core Aerospace Modules &amp; Decision Tools
                </h3>
                <div className="welcome-modules-grid">
                  <div className="welcome-module-card" onClick={() => setActiveTab("dashboard")}>
                    <div>
                      <div className="welcome-module-header">
                        <div className="welcome-module-icon">
                          <Icon name="Activity" size={20} />
                        </div>
                        <div className="welcome-module-title">Mission Radar Dashboard</div>
                      </div>
                      <div className="welcome-module-desc">
                        Tactical radar visualization with heading vectors, dynamic aircraft interpolation, conflict proximity warnings, and multi-layer custom map basemaps.
                      </div>
                    </div>
                    <div className="welcome-module-action">
                      <span>Launch Mission Radar</span>
                      <Icon name="ArrowRight" size={14} />
                    </div>
                  </div>

                  <div className="welcome-module-card" onClick={() => setActiveTab("aircraft")}>
                    <div>
                      <div className="welcome-module-header">
                        <div className="welcome-module-icon">
                          <Icon name="Plane" size={20} />
                        </div>
                        <div className="welcome-module-title">Live Mode-S Telemetry</div>
                      </div>
                      <div className="welcome-module-desc">
                        Deep flight state vectors including Mach numbers, vertical climb/descent rates, barometric altitudes, squawk codes, flight phases, and CSV export.
                      </div>
                    </div>
                    <div className="welcome-module-action">
                      <span>Inspect Aircraft Fleet</span>
                      <Icon name="ArrowRight" size={14} />
                    </div>
                  </div>

                  <div className="welcome-module-card" onClick={() => setActiveTab("weather")}>
                    <div>
                      <div className="welcome-module-header">
                        <div className="welcome-module-icon">
                          <Icon name="Wind" size={20} />
                        </div>
                        <div className="welcome-module-title">Aviation Weather &amp; METAR/TAF</div>
                      </div>
                      <div className="welcome-module-desc">
                        Official NOAA Aviation Weather Center terminal aerodrome reports, flight categories (VFR/MVFR/IFR/LIFR), altimeter settings, and wind vectors.
                      </div>
                    </div>
                    <div className="welcome-module-action">
                      <span>View Weather Stations</span>
                      <Icon name="ArrowRight" size={14} />
                    </div>
                  </div>

                  <div className="welcome-module-card" onClick={() => setActiveTab("guardian")}>
                    <div>
                      <div className="welcome-module-header">
                        <div className="welcome-module-icon">
                          <Icon name="Shield" size={20} />
                        </div>
                        <div className="welcome-module-title">AI Guardian Reasoning</div>
                      </div>
                      <div className="welcome-module-desc">
                        Autonomous natural-language situational report evaluating airspace density, adverse weather intersections, and cognitive overload risk factors.
                      </div>
                    </div>
                    <div className="welcome-module-action">
                      <span>Examine AI Guardian</span>
                      <Icon name="ArrowRight" size={14} />
                    </div>
                  </div>

                  <div className="welcome-module-card" onClick={() => setActiveTab("workload")}>
                    <div>
                      <div className="welcome-module-header">
                        <div className="welcome-module-icon">
                          <Icon name="Gauge" size={20} />
                        </div>
                        <div className="welcome-module-title">Workload Factor Analysis</div>
                      </div>
                      <div className="welcome-module-desc">
                        Human-factors cognitive saturation model computing aircraft volume, maneuvering transitions, adverse weather stress, and alert frequencies.
                      </div>
                    </div>
                    <div className="welcome-module-action">
                      <span>Analyze Workload Model</span>
                      <Icon name="ArrowRight" size={14} />
                    </div>
                  </div>

                  <div className="welcome-module-card" onClick={() => setActiveTab("assistant")}>
                    <div>
                      <div className="welcome-module-header">
                        <div className="welcome-module-icon">
                          <Icon name="Terminal" size={20} />
                        </div>
                        <div className="welcome-module-title">AI Aviation Copilot</div>
                      </div>
                      <div className="welcome-module-desc">
                        Interactive conversational assistant grounded in real-time telemetry, aerodynamic principles, standard ATC phraseology, and flight regulations.
                      </div>
                    </div>
                    <div className="welcome-module-action">
                      <span>Open Copilot Assistant</span>
                      <Icon name="ArrowRight" size={14} />
                    </div>
                  </div>
                </div>
              </div>

              {/* 3-Step Decision Intelligence Process */}
              <div>
                <h3 style={{ fontSize: "16px", fontWeight: 700, marginBottom: "14px", display: "flex", alignItems: "center", gap: "8px" }}>
                  <Icon name="Radio" size={18} color="var(--sky)" /> How AeroGuardian AI Safeguards Airspace
                </h3>
                <div className="welcome-steps-grid">
                  <div className="welcome-step-card">
                    <div className="welcome-step-num">01</div>
                    <div className="welcome-step-title">Telemetry &amp; Weather Ingestion</div>
                    <div className="welcome-step-desc">
                      Continuous ingest of real-time OpenSky Network ADS-B transponder state vectors coupled with live NOAA Aviation Weather Center aerodrome reports.
                    </div>
                  </div>

                  <div className="welcome-step-card">
                    <div className="welcome-step-num">02</div>
                    <div className="welcome-step-title">Multi-Layer Risk &amp; Conflict Fusion</div>
                    <div className="welcome-step-desc">
                      Automated calculations for horizontal &amp; vertical separation loss, excessive climb/descent rates, emergency squawk codes (7700/7600/7500), and terminal convective storm overlap.
                    </div>
                  </div>

                  <div className="welcome-step-card">
                    <div className="welcome-step-num">03</div>
                    <div className="welcome-step-title">Human-Centered Decision Support</div>
                    <div className="welcome-step-desc">
                      Prioritized cognitive alerts and plain-language situation digests designed to augment pilot and air traffic controller decision-making without overriding human authority.
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* ========================================================
              TAB 1: MISSION DASHBOARD
             ======================================================== */}
          {activeTab === "dashboard" && (
            <>
              {/* KPI Cards */}
              <div className="kpi-grid">
                <div className="kpi-card">
                  <div className="kpi-card-header">
                    <span className="kpi-label">Live Aircraft</span>
                    <Icon name="Plane" size={16} className="kpi-icon" />
                  </div>
                  <div className="kpi-value">{aircraft.length}</div>
                  <div className="kpi-sub">{region} Airspace</div>
                </div>

                <div className="kpi-card">
                  <div className="kpi-card-header">
                    <span className="kpi-label">Airborne</span>
                    <Icon name="Activity" size={16} className="kpi-icon" />
                  </div>
                  <div className="kpi-value">{aircraft.filter((p) => !p.on_ground).length}</div>
                  <div className="kpi-sub">{aircraft.filter((p) => p.on_ground).length} on ground</div>
                </div>

                <div className="kpi-card" style={{ borderTopColor: alertCounts.CRITICAL > 0 ? "var(--crimson)" : alertCounts.HIGH > 0 ? "var(--amber)" : "var(--green)" }}>
                  <div className="kpi-card-header">
                    <span className="kpi-label">Attention Items</span>
                    <Icon name="AlertTriangle" size={16} style={{ color: alertCounts.CRITICAL > 0 ? "var(--crimson)" : "var(--amber)" }} />
                  </div>
                  <div className="kpi-value" style={{ color: alertCounts.CRITICAL > 0 ? "var(--crimson)" : "#fff" }}>
                    {alerts.length}
                  </div>
                  <div className="kpi-sub">{alertCounts.CRITICAL} Crit • {alertCounts.HIGH} High • {alertCounts.MEDIUM} Med</div>
                </div>

                <div className="kpi-card">
                  <div className="kpi-card-header">
                    <span className="kpi-label">Weather Stations</span>
                    <Icon name="Wind" size={16} className="kpi-icon" />
                  </div>
                  <div className="kpi-value">{weatherStations.length}</div>
                  <div className="kpi-sub">NOAA AWC Real-time</div>
                </div>

                <div className="kpi-card" style={{ borderTopColor: workload.workload_index >= 75 ? "var(--crimson)" : workload.workload_index >= 50 ? "var(--amber)" : "var(--cyan)" }}>
                  <div className="kpi-card-header">
                    <span className="kpi-label">Workload Index</span>
                    <Icon name="Gauge" size={16} className="kpi-icon" />
                  </div>
                  <div className="kpi-value" style={{ color: workload.workload_index >= 75 ? "var(--crimson)" : workload.workload_index >= 50 ? "var(--amber)" : "var(--cyan)" }}>
                    {workload.workload_index}%
                  </div>
                  <div className="kpi-sub">{workload.level} (Research Model)</div>
                </div>
              </div>

              {/* Main Dashboard Row: Header */}
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "10px" }}>
                <h3 style={{ fontSize: "16px", fontWeight: 700, display: "flex", alignItems: "center", gap: "8px" }}>
                  <Icon name="Compass" size={18} color="var(--cyan)" /> Real-Time Aircraft Radar Map
                </h3>
                <span style={{ fontSize: "11px", color: "var(--text-muted)", display: "flex", alignItems: "center", gap: "6px" }}>
                  <span className="pulse-dot" /> 100% Full Tactical Scope • Live OpenSky ADS-B Telemetry
                </span>
              </div>

              {/* 1. FULL-WIDTH TACTICAL RADAR SCOPE (100% CONTAINER WIDTH) */}
              <div style={{ width: "100%", marginBottom: "16px" }}>
                <RadarMap
                  aircraft={aircraft}
                  alerts={alerts}
                  region={region}
                  selectedPlane={selectedPlane}
                  onSelectPlane={(p) => {
                    setSelectedPlane(p);
                    setActiveTab("aircraft");
                  }}
                />
              </div>

              {/* 2. AIRSPACE FLIGHT PATHS & ROUTING STATUS BAR (TOTALLY BELOW MAP) */}
              <div className="glass-panel" style={{ padding: "14px 20px", marginBottom: "16px", display: "flex", justifyContent: "space-between", alignItems: "center", flexWrap: "wrap", gap: "12px", background: "rgba(10, 16, 30, 0.85)", border: "1px solid var(--border-subtle)" }}>
                <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
                  <Icon name="Route" size={18} color="var(--cyan)" />
                  <div>
                    <div style={{ fontSize: "12px", fontWeight: 700, textTransform: "uppercase", color: "var(--cyan)", letterSpacing: "1px" }}>
                      Airspace Flight Paths & Navigation Routing
                    </div>
                    <div style={{ fontSize: "13px", color: "#f1f5f9", marginTop: "2px" }}>
                      <b>{aircraft.length} Active Vectors</b> • <b>{aircraft.filter((p) => p.route && p.route.has_route).length} Corridors Resolved (Start ➔ End)</b> • <b>{aircraft.filter((p) => !p.on_ground).length} En-Route</b>
                    </div>
                  </div>
                </div>

                <div style={{ display: "flex", gap: "16px", alignItems: "center", flexWrap: "wrap" }}>
                  <div style={{ fontSize: "12px", color: "var(--text-muted)" }}>
                    Airway Trajectory: <b style={{ color: "var(--cyan)" }}>Great-Circle Geodesic</b>
                  </div>
                  <div style={{ fontSize: "12px", color: "var(--text-muted)" }}>
                    Active Terminal Hubs: <b style={{ color: "#c084fc" }}>{weatherStations.map(w => w.icao).join(" • ")}</b>
                  </div>
                  <div style={{ fontSize: "12px", color: "var(--text-muted)" }}>
                    Lateral Separation: <b style={{ color: "var(--green)" }}>Standard ICAO</b>
                  </div>
                </div>
              </div>

              {/* 3. AI SITUATION AWARENESS & WORKLOAD MODEL (2 EQUAL COLUMNS TOTALLY BELOW MAP) */}
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "16px", marginBottom: "16px" }}>
                <div className="glass-panel" style={{ background: "var(--bg-card-highlight)" }}>
                  <div style={{ display: "flex", alignItems: "center", gap: "8px", marginBottom: "8px" }}>
                    <Icon name="Shield" size={18} color="var(--cyan)" />
                    <h4 style={{ fontSize: "14px", color: "var(--cyan)", textTransform: "uppercase", letterSpacing: "1px" }}>
                      AI Situation Awareness
                    </h4>
                  </div>
                  <div style={{ fontSize: "12px", color: "var(--text-muted)", marginBottom: "8px" }}>
                    Flights Tracked: <b>{aircraft.length}</b> ({aircraft.filter((p) => !p.on_ground).length} airborne) • Attention Alerts: <b>{alerts.length}</b>
                  </div>
                  <div style={{ background: "rgba(7, 11, 19, 0.6)", padding: "12px", borderRadius: "8px", borderLeft: "3px solid var(--cyan)", fontSize: "13px", lineHeight: "1.6", color: "#f1f5f9" }}>
                    "{situation.summary_text || "Evaluating current real airspace telemetry..."}"
                  </div>
                </div>

                <div className="glass-panel" style={{ display: "flex", alignItems: "center", justifyContent: "space-between", padding: "16px 24px" }}>
                  <div>
                    <div style={{ fontSize: "12px", fontWeight: 700, textTransform: "uppercase", color: "var(--cyan)", letterSpacing: "1px" }}>
                      Cognitive Workload Model
                    </div>
                    <h3 style={{ fontSize: "20px", fontWeight: 800, marginTop: "4px" }}>Level: {workload.level}</h3>
                    <p style={{ fontSize: "12px", color: "var(--text-muted)", marginTop: "4px", maxWidth: "260px" }}>
                      Multi-factor index balancing alert volume, flight state dynamics, and terminal weather.
                    </p>
                  </div>
                  <WorkloadGauge score={workload.workload_index} level={workload.level} />
                </div>
              </div>

              {/* Priority Alerts Feed */}
              <div>
                <h3 style={{ fontSize: "16px", fontWeight: 700, marginBottom: "12px", display: "flex", alignItems: "center", gap: "8px" }}>
                  <Icon name="AlertTriangle" size={18} color="var(--amber)" /> Priority Alerts Feed
                </h3>
                {alerts.length === 0 ? (
                  <div className="alert-row alert-row-low">
                    <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
                      <Icon name="CheckCircle2" size={20} color="var(--green)" />
                      <div>
                        <b>Nominal Airspace Operations:</b> No priority anomalies detected.
                      </div>
                    </div>
                  </div>
                ) : (
                  alerts.slice(0, 4).map((a) => {
                    const sev = a.priority.toLowerCase();
                    return (
                      <div key={a.id} className={`alert-row alert-row-${sev}`}>
                        <div>
                          <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
                            <span className="alert-badge" style={{ background: sev === "critical" ? "rgba(255,51,102,0.2)" : "rgba(245,158,11,0.2)", color: sev === "critical" ? "var(--crimson)" : "var(--amber)", border: `1px solid ${sev === "critical" ? "var(--crimson)" : "var(--amber)"}` }}>
                              {a.priority}
                            </span>
                            <b style={{ fontSize: "14px" }}>{a.alert_title}</b>
                            <span style={{ fontSize: "11px", color: "var(--text-muted)" }}>{a.timestamp}</span>
                          </div>
                          <div style={{ fontSize: "13px", marginTop: "6px", color: "#f8fafc" }}>
                            Flight: <b>{a.callsign}</b> (<code>{a.icao24}</code>) - {a.detected}
                          </div>
                          <div style={{ fontSize: "12px", color: "var(--text-muted)", marginTop: "4px" }}>
                            <b>Trigger:</b> <code>{a.triggering_data}</code> | <b>Action:</b> {a.suggested_verification}
                          </div>
                        </div>

                        <button
                          className="btn-icon"
                          onClick={() => handleAcknowledge(a.id, a.acknowledged)}
                          style={{ borderColor: a.acknowledged ? "var(--green)" : "var(--border-subtle)", color: a.acknowledged ? "var(--green)" : "#fff" }}
                        >
                          <Icon name={a.acknowledged ? "Check" : "Eye"} size={14} />
                          {a.acknowledged ? "Acknowledged" : "Acknowledge"}
                        </button>
                      </div>
                    );
                  })
                )}
              </div>

              {/* Terminal Weather Overview Strip */}
              <div>
                <h3 style={{ fontSize: "16px", fontWeight: 700, marginBottom: "12px", display: "flex", alignItems: "center", gap: "8px" }}>
                  <Icon name="Wind" size={18} color="var(--sky)" /> Terminal Aerodrome Snapshot
                </h3>
                <div style={{ display: "grid", gridTemplateColumns: `repeat(${weatherStations.length || 1}, 1fr)`, gap: "12px" }}>
                  {weatherStations.map((w) => {
                    const cat = w.flight_category || "VFR";
                    let catColor = "var(--green)";
                    if (cat === "LIFR") catColor = "var(--crimson)";
                    else if (cat === "IFR") catColor = "var(--amber)";
                    else if (cat === "MVFR") catColor = "var(--sky)";

                    return (
                      <div key={w.icao} className="wx-card" onClick={() => { setSelectedWxIcao(w.icao); setActiveTab("weather"); }} style={{ cursor: "pointer" }}>
                        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                          <b style={{ fontSize: "15px", color: "#fff" }}>{w.icao}</b>
                          <span style={{ fontSize: "10px", fontWeight: 800, padding: "2px 8px", borderRadius: "12px", background: `${catColor}22`, color: catColor, border: `1px solid ${catColor}` }}>
                            {cat}
                          </span>
                        </div>
                        <div style={{ fontSize: "12px", color: "var(--text-muted)" }}>Wind: {w.wind_speed_kt || "N/A"} kts @ {w.wind_dir_deg || 0}°</div>
                        <div style={{ fontSize: "11px", color: "var(--sky)" }}>Vis: {w.visibility_sm || "N/A"} SM</div>
                      </div>
                    );
                  })}
                </div>
              </div>
            </>
          )}

          {/* ========================================================
              TAB 2: LIVE AIRCRAFT (Radar + Data Grid + Detail Drawer)
             ======================================================== */}
          {activeTab === "aircraft" && (
            <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
              {/* Filter Toolbar & Lifecycle Phase Selector */}
              <div className="glass-panel" style={{ display: "flex", flexDirection: "column", gap: "12px", padding: "14px 20px" }}>
                <div style={{ display: "flex", gap: "14px", alignItems: "center" }}>
                  <div style={{ display: "flex", alignItems: "center", gap: "8px", flexGrow: 1 }}>
                    <Icon name="Search" size={16} color="var(--text-muted)" />
                    <input
                      type="text"
                      placeholder="Search by Callsign, ICAO24, or Country..."
                      value={searchFilter}
                      onChange={(e) => setSearchFilter(e.target.value)}
                      style={{ width: "100%" }}
                    />
                  </div>

                  <select value={statusFilter} onChange={(e) => setStatusFilter(e.target.value)}>
                    <option value="ALL">All Operational Status</option>
                    <option value="AIRBORNE">Airborne Only</option>
                    <option value="GROUND">On Ground Only</option>
                    <option value="ATTENTION">Attention Items Only</option>
                  </select>

                  <button className="btn-icon" onClick={exportTelemetryCSV}>
                    <Icon name="Download" size={14} /> Export CSV
                  </button>
                </div>

                {/* Flight Phase Selector Chips */}
                <div style={{ display: "flex", gap: "8px", alignItems: "center", flexWrap: "wrap", paddingTop: "4px", borderTop: "1px solid var(--border-subtle)" }}>
                  <span style={{ fontSize: "11px", color: "var(--text-muted)", fontWeight: 700, textTransform: "uppercase", letterSpacing: "0.5px" }}>
                    Flight Lifecycle Phase:
                  </span>
                  {[
                    { id: "ALL", label: "All Flights" },
                    { id: "CRUISE", label: "Cruise (FL)" },
                    { id: "CLIMB", label: "Climb / Takeoff" },
                    { id: "DESCENT", label: "Descent / App" },
                    { id: "GROUND", label: "Surface / Taxi" },
                  ].map((f) => (
                    <button
                      key={f.id}
                      className={`btn-icon ${phaseFilter === f.id ? "active" : ""}`}
                      onClick={() => setPhaseFilter(f.id)}
                      style={{
                        padding: "4px 12px",
                        fontSize: "11px",
                        borderRadius: "14px",
                        background: phaseFilter === f.id ? "rgba(0, 229, 255, 0.15)" : "rgba(15, 23, 42, 0.6)",
                        borderColor: phaseFilter === f.id ? "var(--cyan)" : "var(--border-subtle)",
                        color: phaseFilter === f.id ? "var(--cyan)" : "var(--text-muted)",
                      }}
                    >
                      {f.label}
                    </button>
                  ))}
                </div>
              </div>

              {/* 1. FULL-WIDTH TACTICAL RADAR SCOPE (100% CONTAINER WIDTH) */}
              <div style={{ width: "100%", marginBottom: "16px" }}>
                <RadarMap
                  aircraft={filteredAircraft}
                  alerts={alerts}
                  region={region}
                  selectedPlane={selectedPlane}
                  onSelectPlane={(p) => setSelectedPlane(p)}
                />
              </div>

              {/* 2. SELECTED AIRCRAFT OPERATIONAL & FLIGHT PATH SUITE (TOTALLY BELOW MAP) */}
              {selectedPlane && (
                <div className="glass-panel" style={{ display: "flex", flexDirection: "column", gap: "16px", marginBottom: "16px", border: "1px solid rgba(0, 229, 255, 0.35)", background: "rgba(10, 16, 30, 0.95)" }}>
                  {/* Header */}
                  <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", borderBottom: "1px solid var(--border-subtle)", paddingBottom: "12px" }}>
                    <div>
                      <div style={{ display: "flex", alignItems: "center", gap: "10px", flexWrap: "wrap" }}>
                        <h3 style={{ fontSize: "20px", color: "#fff", display: "flex", alignItems: "center", gap: "8px" }}>
                          ✈️ {selectedPlane.callsign || "No-Callsign"}
                        </h3>
                        <span style={{ fontSize: "13px", color: "var(--text-muted)" }}>
                          ICAO24: <code style={{ color: "var(--cyan)" }}>{selectedPlane.icao24}</code>
                        </span>
                        <span style={{ fontSize: "13px", color: "var(--text-muted)" }}>• {selectedPlane.country}</span>
                        {selectedPlane.registration && (
                          <span style={{ fontSize: "12px", background: "rgba(0,229,255,0.1)", color: "var(--cyan)", padding: "2px 8px", borderRadius: "4px" }}>
                            REG: {selectedPlane.registration}
                          </span>
                        )}
                        {selectedPlane.aircraft_type && (
                          <span style={{ fontSize: "12px", background: "rgba(168,85,247,0.15)", color: "#c084fc", padding: "2px 8px", borderRadius: "4px" }}>
                            TYPE: {selectedPlane.aircraft_type}
                          </span>
                        )}
                      </div>

                      <div style={{ display: "flex", gap: "8px", alignItems: "center", marginTop: "8px", flexWrap: "wrap" }}>
                        <span className={`phase-badge phase-badge-${selectedPlane.flight_phase?.color || 'cruise'}`}>
                          {selectedPlane.flight_phase?.name || (selectedPlane.on_ground ? "Surface Taxi" : "Cruise")}
                        </span>
                        {selectedPlane.wake_category && (
                          <span className="status-tag" style={{ background: "rgba(148, 163, 184, 0.12)", color: "#cbd5e1", border: "1px solid rgba(148, 163, 184, 0.3)", fontSize: "11px", padding: "2px 8px" }}>
                            WAKE: {selectedPlane.wake_category.category} ({selectedPlane.wake_category.code})
                          </span>
                        )}
                        {selectedPlane.squawk && (
                          <span style={{ fontSize: "11px", color: "var(--text-muted)", fontFamily: "var(--font-mono)" }}>
                            SQUAWK: <b style={{ color: "#fff" }}>{selectedPlane.squawk}</b>
                          </span>
                        )}
                        {selectedPlane.telemetry_age !== undefined && (
                          <span style={{ fontSize: "11px", color: "var(--text-muted)", display: "flex", alignItems: "center", gap: "4px" }}>
                            <Icon name="Clock" size={12} /> {selectedPlane.telemetry_age}s latency
                          </span>
                        )}
                      </div>
                    </div>

                    <div style={{ display: "flex", gap: "8px", alignItems: "center" }}>
                      <button
                        className="btn-primary"
                        style={{ padding: "6px 14px", fontSize: "12px", display: "flex", alignItems: "center", gap: "6px" }}
                        onClick={() => {
                          const callsign = selectedPlane.callsign || selectedPlane.icao24;
                          handleSendAssistant(`Tell me all details about flight ${callsign}`);
                          setActiveTab("assistant");
                        }}
                      >
                        <Icon name="MessageSquare" size={14} /> Ask AI About This Aeroplane
                      </button>
                      <button className="btn-icon" onClick={() => setSelectedPlane(null)} title="Close Selection">
                        <Icon name="X" size={16} />
                      </button>
                    </div>
                  </div>

                  {/* REAL-WORLD START-TO-END FLIGHT PATH JOURNEY CARD */}
                  {selectedPlane.route && selectedPlane.route.has_route && (
                    <div style={{
                      background: "linear-gradient(135deg, rgba(10, 25, 47, 0.95) 0%, rgba(15, 23, 42, 0.98) 100%)",
                      border: "1px solid rgba(0, 229, 255, 0.35)",
                      borderRadius: "10px",
                      padding: "16px 20px",
                      boxShadow: "0 4px 20px rgba(0, 229, 255, 0.12)",
                      display: "flex",
                      flexDirection: "column",
                      gap: "12px",
                    }}>
                      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", borderBottom: "1px solid rgba(56, 189, 248, 0.15)", paddingBottom: "8px", flexWrap: "wrap", gap: "8px" }}>
                        <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
                          <span style={{ fontSize: "16px" }}>🛫</span>
                          <h4 style={{ fontSize: "13px", color: "var(--cyan)", textTransform: "uppercase", letterSpacing: "1px", margin: 0 }}>
                            Real Flight Path: {selectedPlane.route.origin?.city || selectedPlane.route.origin?.code} ➔ {selectedPlane.route.destination?.city || selectedPlane.route.destination?.code}
                          </h4>
                          <span style={{ fontSize: "11px", background: "rgba(0, 229, 255, 0.15)", color: "var(--cyan)", padding: "2px 8px", borderRadius: "12px", fontFamily: "var(--font-mono)", fontWeight: 700 }}>
                            {selectedPlane.route.route_code}
                          </span>
                        </div>
                        <div style={{ fontSize: "11px", color: "var(--text-muted)", display: "flex", alignItems: "center", gap: "6px" }}>
                          <span>Corridor: <b>Great-Circle Airway</b></span>
                          <span>•</span>
                          <span>Detection: <b>{selectedPlane.route.origin_detected_by || "ADS-B Vector Alignment"}</b></span>
                        </div>
                      </div>

                      {/* Origin - Active Progress Track - Destination Graphic */}
                      <div style={{ display: "grid", gridTemplateColumns: "1fr 2fr 1fr", gap: "16px", alignItems: "center" }}>
                        {/* Starting Airport (Origin) */}
                        <div style={{ background: "rgba(7, 11, 19, 0.7)", padding: "12px 14px", borderRadius: "8px", border: "1px solid rgba(0, 212, 170, 0.3)" }}>
                          <div style={{ fontSize: "10px", color: "var(--green)", fontWeight: 800, letterSpacing: "1px", textTransform: "uppercase" }}>
                            🛫 STARTING AIRPORT (ORIGIN)
                          </div>
                          <div style={{ fontSize: "22px", fontWeight: 900, color: "#fff", fontFamily: "var(--font-mono)", marginTop: "2px" }}>
                            {selectedPlane.route.origin?.iata || selectedPlane.route.origin?.code}
                          </div>
                          <div style={{ fontSize: "12px", color: "var(--sky)", fontWeight: 600 }}>
                            {selectedPlane.route.origin?.name}
                          </div>
                          <div style={{ fontSize: "11px", color: "var(--text-muted)", marginTop: "4px" }}>
                            {selectedPlane.route.origin?.city}, {selectedPlane.route.origin?.country}
                          </div>
                          <div style={{ fontSize: "10px", color: "var(--green)", marginTop: "6px", fontFamily: "var(--font-mono)" }}>
                            ✓ Departed & Airborne
                          </div>
                        </div>

                        {/* Middle: Active Journey Progress & Dynamic Flight Motion */}
                        <div style={{ display: "flex", flexDirection: "column", gap: "8px", padding: "0 10px" }}>
                          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline" }}>
                            <span style={{ fontSize: "11px", color: "var(--green)", fontWeight: 700 }}>
                              {Math.round(selectedPlane.route.traveled_km || 0)} km Flown
                            </span>
                            <div style={{ textAlign: "center" }}>
                              <span style={{ fontSize: "18px", fontWeight: 900, color: "var(--cyan)", fontFamily: "var(--font-mono)" }}>
                                {selectedPlane.route.progress_pct !== undefined ? `${selectedPlane.route.progress_pct}%` : "50%"}
                              </span>
                              <span style={{ fontSize: "10px", color: "var(--text-muted)", marginLeft: "4px" }}>Completed</span>
                            </div>
                            <span style={{ fontSize: "11px", color: "var(--crimson)", fontWeight: 700 }}>
                              {Math.round(selectedPlane.route.remaining_km || 0)} km Remaining
                            </span>
                          </div>

                          {/* Dynamic Multi-Color Progress Bar */}
                          <div style={{ width: "100%", height: "8px", background: "rgba(15, 23, 42, 0.9)", borderRadius: "4px", overflow: "hidden", border: "1px solid rgba(56, 189, 248, 0.25)" }}>
                            <div style={{
                              width: `${Math.min(Math.max(selectedPlane.route.progress_pct || 0, 5), 100)}%`,
                              height: "100%",
                              background: "linear-gradient(90deg, #00d4aa 0%, #00e5ff 60%, #a855f7 100%)",
                              boxShadow: "0 0 10px rgba(0, 229, 255, 0.6)",
                              transition: "width 0.3s ease",
                            }} />
                          </div>

                          {/* Live Vector & Time Metrics */}
                          <div style={{ display: "flex", justifyContent: "space-between", fontSize: "11px", color: "#cbd5e1" }}>
                            <span>
                              Track: <b>{Math.round(selectedPlane.heading || 0)}° ({getCardinalDirection(selectedPlane.heading)})</b>
                            </span>
                            <span>
                              Bearing to Dest: <b>{selectedPlane.route.bearing_to_dest ? `${selectedPlane.route.bearing_to_dest}°` : "Direct"}</b>
                            </span>
                            {selectedPlane.route.eta_minutes !== undefined && (
                              <span style={{ color: "var(--amber)", fontWeight: 700 }}>
                                ⏱️ En-Route ETA: ~{Math.floor(selectedPlane.route.eta_minutes / 60)}h {selectedPlane.route.eta_minutes % 60}m
                              </span>
                            )}
                          </div>
                        </div>

                        {/* Ending Airport (Destination) */}
                        <div style={{ background: "rgba(7, 11, 19, 0.7)", padding: "12px 14px", borderRadius: "8px", border: "1px solid rgba(255, 51, 102, 0.3)", textAlign: "right" }}>
                          <div style={{ fontSize: "10px", color: "var(--crimson)", fontWeight: 800, letterSpacing: "1px", textTransform: "uppercase" }}>
                            🛬 ENDING AIRPORT (DESTINATION)
                          </div>
                          <div style={{ fontSize: "22px", fontWeight: 900, color: "#fff", fontFamily: "var(--font-mono)", marginTop: "2px" }}>
                            {selectedPlane.route.destination?.iata || selectedPlane.route.destination?.code}
                          </div>
                          <div style={{ fontSize: "12px", color: "var(--sky)", fontWeight: 600 }}>
                            {selectedPlane.route.destination?.name}
                          </div>
                          <div style={{ fontSize: "11px", color: "var(--text-muted)", marginTop: "4px" }}>
                            {selectedPlane.route.destination?.city}, {selectedPlane.route.destination?.country}
                          </div>
                          <div style={{ fontSize: "10px", color: "var(--crimson)", marginTop: "6px", fontFamily: "var(--font-mono)" }}>
                            Target Inbound Sector
                          </div>
                        </div>
                      </div>
                    </div>
                  )}

                  {/* 2-Column Responsive Layout for Cockpit Tapes and Aerodrome/Diagnostics */}
                  <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "16px" }}>
                    {/* Left Column: Cockpit Avionics Primary Flight Instrument Tape Grid & Aerodrome Vector */}
                    <div style={{ display: "flex", flexDirection: "column", gap: "12px" }}>
                      <h4 style={{ fontSize: "12px", color: "var(--cyan)", textTransform: "uppercase", letterSpacing: "1px", display: "flex", alignItems: "center", gap: "6px" }}>
                        <Icon name="Compass" size={14} /> Cockpit Avionics Primary Flight Instruments
                      </h4>

                      {/* Cockpit Avionics Primary Flight Instrument Tape Grid */}
                      <div className="cockpit-tape-grid" style={{ gridTemplateColumns: "repeat(4, 1fr)" }}>
                        {/* Airspeed Tape */}
                        <div className="cockpit-instrument">
                          <div className="instrument-label">Airspeed / Mach</div>
                          <div className="instrument-val">
                            {selectedPlane.speed_kts !== undefined ? selectedPlane.speed_kts : Math.round((selectedPlane.velocity || 0) * 1.94384)} <span style={{ fontSize: "11px", color: "var(--text-muted)" }}>KTS</span>
                          </div>
                          <div className="instrument-sub">
                            {selectedPlane.mach ? `M ${selectedPlane.mach}` : `${selectedPlane.speed_kmh || Math.round((selectedPlane.velocity || 0) * 3.6)} km/h`}
                          </div>
                        </div>

                        {/* Altitude Tape */}
                        <div className="cockpit-instrument">
                          <div className="instrument-label">Baro Altitude</div>
                          <div className="instrument-val">
                            {selectedPlane.flight_level || `FL${Math.round((selectedPlane.baro_altitude || 0) * 3.28084 / 100)}`}
                          </div>
                          <div className="instrument-sub">
                            {(selectedPlane.altitude_ft || Math.round((selectedPlane.baro_altitude || 0) * 3.28084)).toLocaleString()} FT
                          </div>
                        </div>

                        {/* Vertical Speed Indicator */}
                        <div className="cockpit-instrument">
                          <div className="instrument-label">Vertical Speed</div>
                          <div className="instrument-val" style={{ color: (selectedPlane.vertical_rate || 0) > 1 ? "var(--green)" : (selectedPlane.vertical_rate || 0) < -1 ? "var(--amber)" : "#fff" }}>
                            {(selectedPlane.vertical_rate || 0) > 0 ? "+" : ""}{selectedPlane.vertical_rate_fpm !== undefined ? selectedPlane.vertical_rate_fpm : Math.round((selectedPlane.vertical_rate || 0) * 196.85)} <span style={{ fontSize: "11px", color: "var(--text-muted)" }}>FPM</span>
                          </div>
                          <div className="instrument-sub">
                            {Math.abs(selectedPlane.vertical_rate || 0) < 0.5 ? "LEVEL" : (selectedPlane.vertical_rate || 0) > 0 ? "CLIMB" : "DESCENT"}
                          </div>
                        </div>

                        {/* Track & Compass */}
                        <div className="cockpit-instrument">
                          <div className="instrument-label">True Track</div>
                          <div className="instrument-val">
                            {Math.round(selectedPlane.heading || 0)}°
                          </div>
                          <div className="instrument-sub">
                            {fmtHdg(selectedPlane.heading).split(" ")[1] || "HDG"}
                          </div>
                        </div>
                      </div>

                      {/* Nearest Aerodrome & Runway Wind Component Card */}
                      {selectedPlane.nearest_airport && (
                        <div className="aerodrome-wind-box">
                          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                            <div style={{ display: "flex", alignItems: "center", gap: "6px" }}>
                              <Icon name="MapPin" size={14} color="var(--cyan)" />
                              <b style={{ fontSize: "13px", color: "#fff" }}>Flight Path Destination / Nearest Aerodrome: {selectedPlane.nearest_airport.icao}</b>
                            </div>
                            <span className="status-tag" style={{
                              background: selectedPlane.nearest_airport.flight_category === "VFR" ? "rgba(0, 212, 170, 0.15)" : "rgba(245, 158, 11, 0.15)",
                              color: selectedPlane.nearest_airport.flight_category === "VFR" ? "var(--green)" : "var(--amber)",
                              fontSize: "10px",
                              padding: "2px 6px"
                            }}>
                              {selectedPlane.nearest_airport.flight_category}
                            </span>
                          </div>

                          <div style={{ fontSize: "12px", color: "var(--text-muted)", marginTop: "4px" }}>
                            {selectedPlane.nearest_airport.name} • <b>{selectedPlane.nearest_airport.distance_nm} NM</b> @ {selectedPlane.nearest_airport.bearing_deg}° Bearing Corridor
                          </div>

                          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "8px", marginTop: "6px", background: "rgba(7, 11, 19, 0.6)", padding: "8px 12px", borderRadius: "6px" }}>
                            <div>
                              <span style={{ fontSize: "10px", color: "var(--text-muted)", textTransform: "uppercase" }}>Surface Wind</span>
                              <div style={{ fontSize: "12px", fontWeight: 700, color: "var(--sky)" }}>
                                {selectedPlane.nearest_airport.wind_speed_kt || 0} kts @ {selectedPlane.nearest_airport.wind_dir_deg || 0}°
                              </div>
                            </div>
                            <div>
                              <span style={{ fontSize: "10px", color: "var(--text-muted)", textTransform: "uppercase" }}>Runway Crosswind</span>
                              <div style={{
                                fontSize: "12px",
                                fontWeight: 700,
                                color: (selectedPlane.nearest_airport.crosswind_kt || 0) > 15 ? "var(--crimson)" : (selectedPlane.nearest_airport.crosswind_kt || 0) > 10 ? "var(--amber)" : "var(--green)"
                              }}>
                                {selectedPlane.nearest_airport.crosswind_kt || 0} kts {selectedPlane.nearest_airport.crosswind_dir ? `(${selectedPlane.nearest_airport.crosswind_dir})` : ""}
                                {(selectedPlane.nearest_airport.crosswind_kt || 0) > 15 && " ⚠️ HIGH"}
                              </div>
                            </div>
                          </div>
                        </div>
                      )}
                    </div>

                    {/* Right Column: Decision-Support Checklist & AI Diagnostics */}
                    <div style={{ display: "flex", flexDirection: "column", gap: "12px" }}>
                      {/* Interactive Pilot / Controller Decision-Support Checklist */}
                      {planeDiagnostic?.checklist && planeDiagnostic.checklist.length > 0 && (
                        <div>
                          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "6px" }}>
                            <h4 style={{ fontSize: "12px", color: "var(--cyan)", textTransform: "uppercase", letterSpacing: "1px", display: "flex", alignItems: "center", gap: "6px" }}>
                              <Icon name="CheckSquare" size={14} /> Decision-Support Checklist
                            </h4>
                            <span style={{ fontSize: "11px", color: "var(--text-muted)" }}>
                              {planeDiagnostic.checklist.filter((c) => checkedChecklists[`${selectedPlane.icao24}-${c.id}`]).length}/{planeDiagnostic.checklist.length} Verified
                            </span>
                          </div>

                          <div className="checklist-container">
                            {planeDiagnostic.checklist.map((c) => {
                              const itemKey = `${selectedPlane.icao24}-${c.id}`;
                              const isDone = !!checkedChecklists[itemKey];
                              return (
                                <div
                                  key={c.id}
                                  className={`checklist-item ${isDone ? "checked" : ""} ${c.urgent ? "urgent" : ""}`}
                                  onClick={() => toggleChecklistItem(itemKey)}
                                >
                                  <div className={`checklist-checkbox ${isDone ? "active" : ""}`}>
                                    {isDone ? <Icon name="Check" size={12} color="#070b13" /> : null}
                                  </div>
                                  <span style={{ flexGrow: 1 }}>{c.item}</span>
                                </div>
                              );
                            })}
                          </div>
                        </div>
                      )}

                      {/* AI Guardian Explainable Observations */}
                      <div>
                        <h4 style={{ fontSize: "12px", color: "var(--cyan)", marginBottom: "6px", textTransform: "uppercase", letterSpacing: "1px" }}>
                          AI Guardian Safety Diagnostics
                        </h4>
                        {planeDiagnostic?.observations?.length > 0 ? (
                          planeDiagnostic.observations.map((obs, idx) => (
                            <div key={idx} style={{ background: "rgba(7, 11, 19, 0.7)", padding: "8px 10px", borderRadius: "6px", borderLeft: "3px solid var(--cyan)", marginBottom: "6px" }}>
                              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                                <b style={{ fontSize: "12px" }}>{obs.title}</b>
                                {obs.priority && (
                                  <span className="alert-badge" style={{
                                    background: obs.priority === "CRITICAL" ? "rgba(255, 51, 102, 0.2)" : "rgba(245, 158, 11, 0.2)",
                                    color: obs.priority === "CRITICAL" ? "var(--crimson)" : "var(--amber)",
                                    fontSize: "9px",
                                    padding: "1px 5px"
                                  }}>
                                    {obs.priority}
                                  </span>
                                )}
                              </div>
                              <div style={{ fontSize: "11px", color: "#cbd5e1", marginTop: "3px" }}><b>Detected:</b> {obs.what_detected}</div>
                              <div style={{ fontSize: "11px", color: "var(--sky)", marginTop: "2px" }}><b>Action:</b> {obs.suggested_action}</div>
                            </div>
                          ))
                        ) : (
                          <div style={{ fontSize: "12px", color: "var(--text-muted)", fontStyle: "italic", background: "rgba(7, 11, 19, 0.5)", padding: "10px", borderRadius: "6px" }}>
                            No abnormal aerodynamic, altitude, or transponder deviations detected. Aircraft operating within nominal envelope.
                          </div>
                        )}
                      </div>

                      {/* Telemetry Completeness Audit */}
                      {planeDiagnostic && (
                        <div>
                          <div style={{ display: "flex", justifyContent: "space-between", fontSize: "11px", color: "var(--text-muted)", marginBottom: "4px" }}>
                            <span>Mode-S ADS-B Telemetry Integrity</span>
                            <b>{planeDiagnostic.data_completeness_pct}% Complete</b>
                          </div>
                          <div style={{ background: "rgba(15, 23, 42, 0.8)", height: "5px", borderRadius: "3px", overflow: "hidden" }}>
                            <div style={{ width: `${planeDiagnostic.data_completeness_pct}%`, height: "100%", background: "var(--cyan)" }} />
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              )}

              {/* 3. TRANSMITTED TELEMETRY DATA GRID (TOTALLY BELOW MAP) */}
              <div style={{ width: "100%" }}>
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "8px" }}>
                  <h4 style={{ fontSize: "14px", fontWeight: 700, display: "flex", alignItems: "center", gap: "6px" }}>
                    <Icon name="Activity" size={16} color="var(--cyan)" />
                    Transmitted Mode-S / ADS-B Live Telemetry ({filteredAircraft.length} flights)
                  </h4>
                  <span style={{ fontSize: "11px", color: "var(--text-muted)" }}>Click flight row to inspect diagnostic below map</span>
                </div>

                <div className="table-container" style={{ maxHeight: "380px" }}>
                  <table className="telemetry-table">
                    <thead>
                      <tr>
                        <th>Callsign</th>
                        <th>Route (Start ➔ End)</th>
                        <th>Phase</th>
                        <th>Altitude / FL</th>
                        <th>Speed / Mach</th>
                        <th>VSI</th>
                        <th>Track</th>
                        <th>Nearest Aerodrome</th>
                        <th>Squawk</th>
                        <th>Status</th>
                      </tr>
                    </thead>
                    <tbody>
                      {filteredAircraft.map((p) => (
                        <tr
                          key={p.icao24}
                          onClick={() => setSelectedPlane(p)}
                          style={{ background: selectedPlane?.icao24 === p.icao24 ? "rgba(0, 229, 255, 0.12)" : "transparent", cursor: "pointer" }}
                        >
                          <td>
                            <div style={{ display: "flex", flexDirection: "column" }}>
                              <b>{p.callsign || "N/A"}</b>
                              <span style={{ fontSize: "10px", color: "var(--text-muted)" }}><code>{p.icao24}</code></span>
                            </div>
                          </td>
                          <td>
                            {p.route?.route_code ? (
                              <span
                                className="badge-route"
                                title={`${p.route.origin?.city || p.route.origin?.code} to ${p.route.destination?.city || p.route.destination?.code} (${Math.round(p.route.progress_pct || 0)}% completed)`}
                              >
                                {p.route.origin?.iata || p.route.origin?.code} ✈️ {p.route.destination?.iata || p.route.destination?.code}
                              </span>
                            ) : (
                              <span style={{ fontSize: "11px", color: "var(--text-muted)" }}>En Route</span>
                            )}
                          </td>
                          <td>
                            <span className={`phase-badge phase-badge-${p.flight_phase?.color || 'cruise'}`}>
                              {p.flight_phase?.name || (p.on_ground ? "Surface" : "Cruise")}
                            </span>
                          </td>
                          <td>
                            <div style={{ display: "flex", flexDirection: "column" }}>
                              <b style={{ color: "var(--cyan)" }}>{p.flight_level || `FL${Math.round((p.baro_altitude || 0) * 3.28084 / 100)}`}</b>
                              <span style={{ fontSize: "10px", color: "var(--text-muted)" }}>{fmtAlt(p.baro_altitude)}</span>
                            </div>
                          </td>
                          <td>
                            <div style={{ display: "flex", flexDirection: "column" }}>
                              <b>{fmtSpd(p.velocity)}</b>
                              {p.mach ? <span style={{ fontSize: "10px", color: "var(--sky)" }}>M {p.mach}</span> : null}
                            </div>
                          </td>
                          <td>{fmtVR(p.vertical_rate)}</td>
                          <td>{fmtHdg(p.heading)}</td>
                          <td>
                            {p.nearest_airport ? (
                              <span style={{ fontSize: "11px", color: "var(--text-muted)" }}>
                                <b>{p.nearest_airport.icao}</b> ({p.nearest_airport.distance_nm} NM)
                              </span>
                            ) : (
                              <span style={{ fontSize: "11px", color: "var(--text-muted)" }}>—</span>
                            )}
                          </td>
                          <td><code>{p.squawk || "N/A"}</code></td>
                          <td>{p.on_ground ? "Surface" : "Airborne"}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          )}

          {/* ========================================================
              TAB 3: AVIATION WEATHER
             ======================================================== */}
          {activeTab === "weather" && (
            <div style={{ display: "flex", flexDirection: "column", gap: "20px" }}>
              {/* Station Selector */}
              <div className="glass-panel" style={{ display: "flex", gap: "16px", alignItems: "center" }}>
                <span style={{ fontSize: "13px", fontWeight: 700 }}>Monitored Hub Preset:</span>
                <select value={selectedWxIcao} onChange={(e) => setSelectedWxIcao(e.target.value)}>
                  {["VIDP", "VOBL", "VABB", "VOHS", "VECC", "VOMM", "OMDB", "EGLL", "KJFK", "WSSS"].map((code) => (
                    <option key={code} value={code}>{code}</option>
                  ))}
                </select>

                <div style={{ display: "flex", alignItems: "center", gap: "8px", marginLeft: "auto" }}>
                  <input
                    type="text"
                    placeholder="Enter Custom ICAO (e.g. VIDP)"
                    maxLength={4}
                    onKeyDown={(e) => {
                      if (e.key === "Enter") setSelectedWxIcao(e.target.value.toUpperCase());
                    }}
                    style={{ width: "220px", textTransform: "uppercase" }}
                  />
                  <button className="btn-primary" onClick={() => {
                    const input = document.querySelector('input[placeholder="Enter Custom ICAO (e.g. VIDP)"]');
                    if (input && input.value) setSelectedWxIcao(input.value.toUpperCase());
                  }}>
                    Query
                  </button>
                </div>
              </div>

              {/* Station Report */}
              {stationWx?.metar ? (
                <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
                  <div className="glass-panel">
                    <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                      <div>
                        <h2 style={{ fontSize: "22px", fontWeight: 800 }}>{stationWx.metar.icao} — {stationWx.metar.name}</h2>
                        <span style={{ fontSize: "12px", color: "var(--text-muted)" }}>Report Time: {stationWx.metar.report_time || "Latest"}</span>
                      </div>
                      <span className="status-tag" style={{ background: "rgba(0,212,170,0.15)", color: "var(--green)", border: "1px solid var(--green)" }}>
                        ● {stationWx.metar.flight_category}
                      </span>
                    </div>

                    <div style={{ background: "rgba(7, 11, 19, 0.7)", padding: "12px", borderRadius: "6px", fontFamily: "var(--font-mono)", fontSize: "13px", color: "var(--sky)", marginTop: "14px" }}>
                      {stationWx.metar.raw_text}
                    </div>
                  </div>

                  {/* Weather KPI Grid */}
                  <div className="kpi-grid">
                    <div className="kpi-card">
                      <span className="kpi-label">Wind</span>
                      <div className="kpi-value" style={{ fontSize: "20px" }}>{stationWx.metar.wind_speed_kt || 0} kts @ {stationWx.metar.wind_dir_deg || 0}°</div>
                      <div className="kpi-sub">{stationWx.metar.wind_gust_kt ? `Gusts: ${stationWx.metar.wind_gust_kt} kts` : "Steady"}</div>
                    </div>
                    <div className="kpi-card">
                      <span className="kpi-label">Visibility</span>
                      <div className="kpi-value" style={{ fontSize: "20px" }}>{stationWx.metar.visibility_sm || "N/A"} SM</div>
                      <div className="kpi-sub">Wx: {stationWx.metar.weather_string || "None"}</div>
                    </div>
                    <div className="kpi-card">
                      <span className="kpi-label">Temp / Dewpoint</span>
                      <div className="kpi-value" style={{ fontSize: "20px" }}>{stationWx.metar.temperature_c}°C / {stationWx.metar.dewpoint_c}°C</div>
                      <div className="kpi-sub">Spread: {stationWx.metar.temp_dewpoint_spread}°C</div>
                    </div>
                    <div className="kpi-card">
                      <span className="kpi-label">Altimeter (QNH)</span>
                      <div className="kpi-value" style={{ fontSize: "20px" }}>{stationWx.metar.altimeter_hpa || "N/A"} hPa</div>
                      <div className="kpi-sub">Standard Pressure</div>
                    </div>
                    <div className="kpi-card">
                      <span className="kpi-label">Ceiling</span>
                      <div className="kpi-value" style={{ fontSize: "20px" }}>{stationWx.metar.ceiling_ft ? `${stationWx.metar.ceiling_ft.toLocaleString()} ft` : "Unlimited"}</div>
                      <div className="kpi-sub">{stationWx.metar.has_cumulonimbus ? "⚠️ Convective CB" : "Nominal Cloud"}</div>
                    </div>
                  </div>

                  {/* TAF Forecast */}
                  {stationWx.taf && (
                    <div className="glass-panel">
                      <h4 style={{ fontSize: "14px", fontWeight: 700, marginBottom: "8px", display: "flex", alignItems: "center", gap: "8px" }}>
                        <Icon name="CloudRain" size={16} color="var(--sky)" /> Terminal Aerodrome Forecast (TAF)
                      </h4>
                      <div style={{ background: "rgba(7, 11, 19, 0.7)", padding: "12px", borderRadius: "6px", fontFamily: "var(--font-mono)", fontSize: "12px", color: "var(--green)", maxHeight: "150px", overflowY: "auto" }}>
                        {stationWx.taf.raw_text}
                      </div>
                    </div>
                  )}
                </div>
              ) : (
                <div className="glass-panel">Loading METAR observations...</div>
              )}
            </div>
          )}

          {/* ========================================================
              TAB 4: AI GUARDIAN
             ======================================================== */}
          {activeTab === "guardian" && (
            <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
              <div className="glass-panel" style={{ background: "var(--bg-card-highlight)" }}>
                <h3 style={{ fontSize: "16px", color: "var(--cyan)", marginBottom: "8px" }}>
                  AI Guardian Executive Situation Assessment
                </h3>
                <div style={{ fontSize: "14px", lineHeight: "1.6" }}>
                  {situation.summary_text}
                </div>
              </div>

              <div>
                <h3 style={{ fontSize: "16px", fontWeight: 700, marginBottom: "12px" }}>
                  Prioritized Attention & Anomaly Verification Cards
                </h3>
                {alerts.map((a) => (
                  <div key={a.id} className={`alert-row alert-row-${a.priority.toLowerCase()}`} style={{ display: "block" }}>
                    <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                      <span className="alert-badge" style={{ background: a.priority === "CRITICAL" ? "rgba(255,51,102,0.2)" : "rgba(245,158,11,0.2)", color: a.priority === "CRITICAL" ? "var(--crimson)" : "var(--amber)", border: `1px solid ${a.priority === "CRITICAL" ? "var(--crimson)" : "var(--amber)"}` }}>
                        {a.priority}
                      </span>
                      <span style={{ fontSize: "11px", color: "var(--text-muted)" }}>{a.timestamp}</span>
                    </div>

                    <h4 style={{ fontSize: "15px", marginTop: "8px" }}>{a.alert_title} - {a.callsign} (<code>{a.icao24}</code>)</h4>

                    <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "14px", marginTop: "10px" }}>
                      <div>
                        <div style={{ fontSize: "13px", color: "#f1f5f9" }}><b>What was detected:</b> {a.detected}</div>
                        <div style={{ fontSize: "12px", color: "var(--text-muted)", marginTop: "4px" }}><b>Why it matters:</b> {a.why_it_matters}</div>
                      </div>
                      <div>
                        <div style={{ fontSize: "12px", color: "var(--sky)" }}><b>Triggering Telemetry:</b> <code>{a.triggering_data}</code></div>
                        <div style={{ fontSize: "12px", color: "var(--text-muted)", marginTop: "4px" }}><b>Confidence:</b> {a.confidence}</div>
                        <div style={{ fontSize: "12px", color: "var(--cyan)", marginTop: "4px" }}><b>Recommended Verification:</b> {a.suggested_verification}</div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* ========================================================
              TAB 5: WORKLOAD ANALYSIS
             ======================================================== */}
          {activeTab === "workload" && (
            <div style={{ display: "flex", flexDirection: "column", gap: "20px" }}>
              <div className="glass-panel" style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
                <div>
                  <div style={{ fontSize: "12px", fontWeight: 700, color: "var(--cyan)", textTransform: "uppercase" }}>
                    AI-Assisted Workload Indicator — Research Prototype
                  </div>
                  <h2 style={{ fontSize: "28px", fontWeight: 800, marginTop: "4px" }}>{workload.workload_index}% — {workload.level}</h2>
                  <p style={{ fontSize: "13px", color: "var(--text-muted)", marginTop: "4px" }}>{workload.level_description}</p>
                </div>
                <WorkloadGauge score={workload.workload_index} level={workload.level} />
              </div>

              {/* Factors Breakdown Table */}
              <div className="glass-panel">
                <h3 style={{ fontSize: "16px", fontWeight: 700, marginBottom: "12px" }}>Multi-Factor Weighting Breakdown</h3>
                <div className="table-container">
                  <table className="telemetry-table">
                    <thead>
                      <tr>
                        <th>Factor</th>
                        <th>Weight</th>
                        <th>Score</th>
                        <th>Observable Metrics</th>
                      </tr>
                    </thead>
                    <tbody>
                      {workload.contributing_factors?.map((f, i) => (
                        <tr key={i}>
                          <td><b>{f.factor}</b></td>
                          <td>{f.weight}</td>
                          <td><b>{f.score}/100</b></td>
                          <td>{f.details}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          )}

          {/* ========================================================
              TAB 6: ALERT CENTER
             ======================================================== */}
          {activeTab === "alerts" && (
            <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
              <div className="glass-panel" style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                <div style={{ display: "flex", gap: "10px" }}>
                  {["ALL", "CRITICAL", "HIGH", "MEDIUM", "LOW"].map((p) => (
                    <button
                      key={p}
                      className={`btn-icon ${priorityFilter === p ? "active" : ""}`}
                      onClick={() => setPriorityFilter(p)}
                    >
                      {p}
                    </button>
                  ))}
                </div>

                <button className="btn-icon" onClick={() => fetch("/api/alerts/clear-acknowledged", { method: "POST" }).then(() => fetchData())}>
                  Clear Acknowledged
                </button>
              </div>

              {alerts
                .filter((a) => priorityFilter === "ALL" || a.priority === priorityFilter)
                .map((a) => (
                  <div key={a.id} className={`alert-row alert-row-${a.priority.toLowerCase()}`} style={{ opacity: a.acknowledged ? 0.6 : 1 }}>
                    <div>
                      <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
                        <span className="alert-badge">{a.priority}</span>
                        <b>{a.alert_title}</b>
                        <span style={{ fontSize: "11px", color: "var(--text-muted)" }}>{a.timestamp}</span>
                      </div>
                      <div style={{ fontSize: "13px", marginTop: "4px" }}>
                        Flight: <b>{a.callsign}</b> (<code>{a.icao24}</code>) - {a.detected}
                      </div>
                      <div style={{ fontSize: "12px", color: "var(--text-muted)", marginTop: "4px" }}>
                        <b>Trigger:</b> <code>{a.triggering_data}</code> | <b>Action:</b> {a.suggested_verification}
                      </div>
                    </div>

                    <button className="btn-icon" onClick={() => handleAcknowledge(a.id, a.acknowledged)}>
                      <Icon name={a.acknowledged ? "Check" : "Eye"} size={14} />
                      {a.acknowledged ? "Mark Unread" : "Acknowledge"}
                    </button>
                  </div>
                ))}
            </div>
          )}

          {/* ========================================================
              TAB 7: ANALYTICS
             ======================================================== */}
          {activeTab === "analytics" && (
            <div style={{ display: "flex", flexDirection: "column", gap: "20px" }}>
              <div className="kpi-grid">
                <div className="kpi-card">
                  <span className="kpi-label">Total Fleet</span>
                  <div className="kpi-value">{aircraft.length}</div>
                </div>
                <div className="kpi-card">
                  <span className="kpi-label">Airborne</span>
                  <div className="kpi-value">{aircraft.filter((p) => !p.on_ground).length}</div>
                </div>
                <div className="kpi-card">
                  <span className="kpi-label">Active Alerts</span>
                  <div className="kpi-value">{alerts.length}</div>
                </div>
                <div className="kpi-card">
                  <span className="kpi-label">Weather Stations</span>
                  <div className="kpi-value">{weatherStations.length}</div>
                </div>
                <div className="kpi-card">
                  <span className="kpi-label">Workload Score</span>
                  <div className="kpi-value">{workload.workload_index}%</div>
                </div>
              </div>

              <div className="glass-panel">
                <h3 style={{ fontSize: "16px", fontWeight: 700, marginBottom: "10px" }}>Fleet Altitude Band Distribution</h3>
                <div style={{ display: "flex", gap: "8px", alignItems: "flex-end", height: "180px", paddingTop: "20px" }}>
                  {[
                    { label: "0-10k ft", count: aircraft.filter((p) => p.baro_altitude && p.baro_altitude < 3048).length },
                    { label: "10k-20k ft", count: aircraft.filter((p) => p.baro_altitude && p.baro_altitude >= 3048 && p.baro_altitude < 6096).length },
                    { label: "20k-30k ft", count: aircraft.filter((p) => p.baro_altitude && p.baro_altitude >= 6096 && p.baro_altitude < 9144).length },
                    { label: "30k-40k ft", count: aircraft.filter((p) => p.baro_altitude && p.baro_altitude >= 9144 && p.baro_altitude < 12192).length },
                    { label: ">40k ft", count: aircraft.filter((p) => p.baro_altitude && p.baro_altitude >= 12192).length },
                  ].map((band, i) => {
                    const maxCount = Math.max(aircraft.length, 1);
                    const pct = Math.round((band.count / maxCount) * 100);
                    return (
                      <div key={i} style={{ flex: 1, display: "flex", flexDirection: "column", alignItems: "center", gap: "6px" }}>
                        <span style={{ fontSize: "11px", color: "var(--cyan)", fontFamily: "var(--font-mono)" }}>{band.count}</span>
                        <div style={{ width: "100%", height: `${Math.max(pct * 1.5, 6)}px`, background: "linear-gradient(180deg, var(--cyan) 0%, var(--sky) 100%)", borderRadius: "4px 4px 0 0" }} />
                        <span style={{ fontSize: "10px", color: "var(--text-muted)" }}>{band.label}</span>
                      </div>
                    );
                  })}
                </div>
              </div>
            </div>
          )}

          {/* ========================================================
              TAB 8: AI ASSISTANT TERMINAL
             ======================================================== */}
          {activeTab === "assistant" && (
            <div className="glass-panel" style={{ padding: "16px" }}>
              <div style={{ display: "flex", alignItems: "center", gap: "8px", marginBottom: "14px" }}>
                <Icon name="Terminal" size={18} color="var(--cyan)" />
                <h3 style={{ fontSize: "16px", fontWeight: 700 }}>Grounded AI Aviation Assistant</h3>
              </div>

              {/* Quick Inquiry Chips */}
              <div style={{ display: "flex", gap: "8px", marginBottom: "14px", flexWrap: "wrap" }}>
                {[
                  "Tell all details related to aeroplane",
                  "Inspect fastest Mach aircraft",
                  "Inspect highest cruise flight",
                  "What are the emergency transponder squawk codes?",
                  "How does wake turbulence separation work?",
                  "Which aircraft require attention?",
                  "Explain the highest priority alert",
                ].map((chip) => (
                  <button
                    key={chip}
                    className="btn-icon"
                    onClick={() => handleSendAssistant(chip)}
                    style={{ fontSize: "12px", padding: "5px 12px", display: "inline-flex", alignItems: "center", gap: "6px" }}
                  >
                    <Icon name="Plane" size={13} color="var(--cyan)" />
                    {chip}
                  </button>
                ))}
              </div>

              {/* Chat Window */}
              <div className="chat-window">
                <div className="chat-history">
                  {chatMessages.map((msg, idx) => {
                    if (msg.role === "assistant" && window.marked) {
                      return (
                        <div
                          key={idx}
                          className="chat-bubble chat-bubble-ai"
                          dangerouslySetInnerHTML={{ __html: window.marked.parse(msg.content) }}
                        />
                      );
                    }
                    return (
                      <div
                        key={idx}
                        className={`chat-bubble ${msg.role === "user" ? "chat-bubble-user" : "chat-bubble-ai"}`}
                        style={{ whiteSpace: "pre-wrap" }}
                      >
                        {msg.content}
                      </div>
                    );
                  })}
                  {chatLoading && (
                    <div className="chat-bubble chat-bubble-ai" style={{ color: "var(--cyan)" }}>
                      Analyzing live telemetry and weather...
                    </div>
                  )}
                </div>

                <div className="chat-input-bar">
                  <input
                    type="text"
                    className="chat-input"
                    placeholder="Ask about live aircraft, weather, or alerts..."
                    value={inputQuery}
                    onChange={(e) => setInputQuery(e.target.value)}
                    onKeyDown={(e) => {
                      if (e.key === "Enter") handleSendAssistant();
                    }}
                  />
                  <button className="btn-primary" onClick={() => handleSendAssistant()}>
                    Send
                  </button>
                </div>
              </div>
            </div>
          )}

          {/* ========================================================
              TAB 9: ABOUT
             ======================================================== */}
          {activeTab === "about" && (
            <div className="glass-panel" style={{ lineHeight: "1.7", fontSize: "14px" }}>
              <h2 style={{ fontSize: "22px", color: "var(--cyan)", marginBottom: "6px" }}>AeroGuardian AI</h2>
              <p style={{ fontSize: "15px", color: "var(--sky)", fontWeight: 600 }}>
                "An AI Agent for Pilot Workload & Decision Support"
              </p>
              <p style={{ color: "var(--text-muted)", marginBottom: "16px" }}>
                Theme: <b>Smart Systems for a Safer Future in Aviation</b>
              </p>

              <h4 style={{ color: "#fff", marginTop: "14px" }}>1. Academic & Research Mission</h4>
              <p>
                AeroGuardian AI acts as a Human-Factor Guardian. In dense commercial airspace, pilots and controllers must
                process multi-source data continuously. AeroGuardian AI ingests real ADS-B/Mode-S telemetry and NOAA aviation weather,
                synthesizes attention-worthy conditions, and calculates a research workload indicator to reduce cognitive saturation.
              </p>

              <h4 style={{ color: "#fff", marginTop: "14px" }}>2. Real Aviation Data Sources</h4>
              <p>
                Strictly real data only — no simulation, fake telemetry, or synthetic flights:
                <br />- <b>OpenSky Network REST API:</b> Real-time Mode-S / ADS-B transponder state vectors.
                <br />- <b>NOAA Aviation Weather Center Data API:</b> Official METAR and TAF reports.
                <br />- <b>AI Reasoning Agent:</b> Natural language situation reports and grounded assistant.
              </p>

              <h4 style={{ color: "#fff", marginTop: "14px" }}>3. Safety Disclaimer</h4>
              <p style={{ color: "var(--crimson)" }}>
                AeroGuardian AI is a research prototype. It is not certified avionics software and must never be used for aircraft control
                or operational air navigation. It never claims to replace pilots or air traffic controllers.
              </p>
            </div>
          )}
        </div>

        {/* Aerospace Control Room Footer (Eliminates trailing blank space) */}
        <footer className="aerospace-footer">
          <div className="footer-left">
            <span className="footer-brand">AeroGuardian AI</span>
            <span className="footer-sep">•</span>
            <span>Pilot Workload &amp; Decision Support System</span>
            <span className="footer-sep">•</span>
            <span>v3.2</span>
          </div>
          <div className="footer-right">
            <span className="footer-status">
              <Icon name="CheckCircle2" size={13} color="var(--green)" /> Systems Operational
            </span>
            <span className="footer-sep">•</span>
            <span>Region: <b>{region}</b></span>
            <span className="footer-sep">•</span>
            <span>Feeds: <b>OpenSky ADS-B + NOAA AWC</b></span>
          </div>
        </footer>
      </main>
    </div>
  );
}

// Mount React App
ReactDOM.render(<App />, document.getElementById("root"));
