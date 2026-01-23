import React from 'react';

export default function Dashboard() {
  return (
    // font-display, text-white, pb-32 등 Stitch의 body class를 여기에 적용
    <div className="font-display text-white pb-32 min-h-screen">
      
      {/* Navbar */}
      <nav className="sticky top-0 z-50 px-6 py-4 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="w-10 h-10 rounded-full liquid-glass flex items-center justify-center border border-white/40">
            <span className="material-symbols-outlined text-accent-cyan text-[24px]">auto_awesome</span>
          </div>
          <h1 className="text-lg font-bold tracking-tight text-glow">AI Agent</h1>
        </div>
        <button className="w-10 h-10 rounded-full liquid-glass flex items-center justify-center">
          <span className="material-symbols-outlined text-white">notifications</span>
        </button>
      </nav>

      {/* Search & Action */}
      <div className="px-6 pt-6 pb-4 space-y-4">
        <div className="relative group">
          <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
            <span className="material-symbols-outlined text-white/60">search</span>
          </div>
          <input 
            className="block w-full pl-12 pr-4 py-4 liquid-glass border-white/20 rounded-full placeholder:text-white/40 text-sm focus:ring-1 focus:ring-white/30 focus:outline-none transition-all" 
            placeholder="Search AI Influencers..." 
            type="text"
          />
        </div>
        <button className="w-full liquid-glass-intense h-14 rounded-full flex items-center justify-center gap-3 text-white font-bold active:scale-[0.98] transition-transform group">
          <span className="material-symbols-outlined text-accent-pink">magic_button</span>
          <span className="text-glow">Generate Deep Report</span>
        </button>
      </div>

      {/* Real-time Analysis (details 태그 사용) */}
      <div className="px-6 py-4">
        <div className="liquid-glass rounded-3xl overflow-hidden">
          <details className="group" open>
            <summary className="flex cursor-pointer items-center justify-between px-6 py-4 list-none">
              <div className="flex items-center gap-3">
                <span className="material-symbols-outlined text-accent-cyan animate-pulse">analytics</span>
                <p className="font-semibold text-sm">Real-time Analysis</p>
              </div>
              <span className="material-symbols-outlined text-white/60 transition-transform group-open:rotate-180">expand_more</span>
            </summary>
            <div className="px-6 pb-6 space-y-5">
              <div className="flex items-start gap-4">
                <div className="size-2 mt-2 rounded-full bg-accent-cyan shadow-[0_0_8px_#00f2ff]"></div>
                <div>
                  <p className="text-xs font-medium text-accent-cyan">Scanning...</p>
                  <p className="text-[11px] text-white/70">Deep-scanning 1,200 visual patterns from latest posts</p>
                </div>
              </div>
              <div className="flex items-start gap-4">
                <div className="size-2 mt-2 rounded-full bg-accent-lavender/40"></div>
                <div>
                  <p className="text-xs font-medium text-white/80">Filtering...</p>
                  <p className="text-[11px] text-white/60">Isolating metadata and stylistic consistency markers</p>
                </div>
              </div>
              <div className="flex items-start gap-4">
                <div className="size-2 mt-2 rounded-full bg-accent-lavender/20"></div>
                <div>
                  <p className="text-xs font-medium text-white/50">Analyzing...</p>
                  <p className="text-[11px] text-white/40">Synthesizing final sentiment and engagement metrics</p>
                </div>
              </div>
            </div>
          </details>
        </div>
      </div>

      {/* Section Header */}
      <div className="px-6 pt-6 pb-2">
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-bold text-glow">Trending Influencers</h3>
          <span className="text-accent-cyan text-xs font-semibold">View All</span>
        </div>
      </div>

      {/* Grid Cards */}
      <div className="px-6 grid grid-cols-2 gap-4">
        {/* Card 1 */}
        <div className="liquid-glass p-4 rounded-[2.5rem] border-white/20">
          <div className="relative mb-4">
            {/* 이미지는 실제 이미지가 없어서 임시 이미지(Unsplash)로 대체합니다. 원본과 동일하게 보이려면 src만 바꾸시면 됩니다. */}
            <img alt="AI Influencer 1" className="w-full aspect-square object-cover rounded-full border-2 border-white/30" src="https://images.unsplash.com/photo-1620067925093-801122ac1408?q=80&w=200&auto=format&fit=crop"/>
            <div className="absolute -bottom-1 -right-1 liquid-glass p-1 rounded-full border-white/40">
              <span className="material-symbols-outlined text-accent-cyan text-xs fill-1">verified</span>
            </div>
          </div>
          <h4 className="font-bold text-sm truncate text-glow">Luna Cyber</h4>
          <div className="mt-4 space-y-1.5">
            <div className="flex justify-between text-[10px] font-bold text-accent-lavender">
              <span>Consistency</span>
              <span>98%</span>
            </div>
            <div className="h-1.5 w-full bg-white/10 rounded-full overflow-hidden border border-white/5">
              <div className="h-full bg-gradient-to-r from-accent-cyan to-accent-lavender rounded-full shadow-[0_0_8px_rgba(0,242,255,0.4)]" style={{width: "98%"}}></div>
            </div>
          </div>
          <p className="mt-3 text-[10px] text-white/60 leading-relaxed italic line-clamp-2">
            "High stylistic retention across posts. Natural face-mesh sync detected."
          </p>
        </div>

        {/* Card 2 */}
        <div className="liquid-glass p-4 rounded-[2.5rem] border-white/20">
          <div className="relative mb-4">
             <img alt="AI Influencer 2" className="w-full aspect-square object-cover rounded-full border-2 border-white/30" src="https://images.unsplash.com/photo-1534528741775-53994a69daeb?q=80&w=200&auto=format&fit=crop"/>
            <div className="absolute -bottom-1 -right-1 liquid-glass p-1 rounded-full border-white/40">
              <span className="material-symbols-outlined text-accent-cyan text-xs fill-1">verified</span>
            </div>
          </div>
          <h4 className="font-bold text-sm truncate text-glow">Nexus 7</h4>
          <div className="mt-4 space-y-1.5">
            <div className="flex justify-between text-[10px] font-bold text-accent-lavender">
              <span>Consistency</span>
              <span>84%</span>
            </div>
            <div className="h-1.5 w-full bg-white/10 rounded-full overflow-hidden border border-white/5">
              <div className="h-full bg-gradient-to-r from-accent-cyan to-accent-lavender rounded-full" style={{width: "84%"}}></div>
            </div>
          </div>
          <p className="mt-3 text-[10px] text-white/60 leading-relaxed italic line-clamp-2">
            "Minor variance in skin-texture metadata. Prompt drift identified."
          </p>
        </div>
      </div>

      {/* Bottom Nav (Fixed) */}
      <div className="fixed bottom-8 inset-x-0 flex justify-center px-8 z-50">
        <div className="liquid-glass h-16 w-full max-w-[320px] rounded-full flex items-center justify-around px-6 shadow-2xl border-white/30">
          <button className="text-accent-cyan drop-shadow-[0_0_8px_rgba(0,242,255,0.5)] flex items-center justify-center">
            <span className="material-symbols-outlined text-[28px] fill-1">home</span>
          </button>
          <button className="text-white/60 flex items-center justify-center">
            <span className="material-symbols-outlined text-[28px]">search</span>
          </button>
          <button className="text-white/60 flex items-center justify-center">
            <span className="material-symbols-outlined text-[28px]">insert_chart</span>
          </button>
          <button className="text-white/60 flex items-center justify-center">
            <span className="material-symbols-outlined text-[28px]">person</span>
          </button>
        </div>
      </div>

    </div>
  );
}