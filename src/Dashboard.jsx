import React, { useState } from 'react';

export default function Dashboard() {
  // 1. 상태 관리 (변수 만들기)
  const [searchTerm, setSearchTerm] = useState(""); // 검색어 저장
  const [influencers, setInfluencers] = useState([]); // 받아온 인플루언서 목록 저장
  const [loading, setLoading] = useState(false); // 로딩 중인지 확인
  const [searched, setSearched] = useState(false); // 검색을 한 번이라도 했는지

  // 2. 백엔드 요청 함수 (버튼 누르면 실행)
  const handleGenerateReport = async () => {
    if (!searchTerm) return alert("Please enter a category (e.g., Tech, Beauty)");

    setLoading(true); // 로딩 시작
    try {
      // 파이썬 서버로 요청 보내기 (POST)
      const response = await fetch("http://127.0.0.1:8000/recommend", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          category: searchTerm, // 입력한 카테고리 보냄
        }),
      });

      const data = await response.json(); // 응답(JSON) 받기
      setInfluencers(data.results); // 목록 업데이트
      setSearched(true); // 검색 완료 표시

    } catch (error) {
      console.error("Error fetching data:", error);
      alert("백엔드 서버가 켜져 있는지 확인해주세요!");
    } finally {
      setLoading(false); // 로딩 끝
    }
  };

  return (
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
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleGenerateReport()}
            className="block w-full pl-12 pr-4 py-4 liquid-glass border-white/20 rounded-full placeholder:text-white/40 text-sm focus:ring-1 focus:ring-white/30 focus:outline-none transition-all" 
            placeholder="Search AI Influencers..." 
            type="text"
          />
        </div>
        <button 
          onClick={handleGenerateReport}
          disabled={loading}
          className="w-full liquid-glass-intense h-14 rounded-full flex items-center justify-center gap-3 text-white font-bold active:scale-[0.98] transition-transform group disabled:opacity-50"
        >
          {loading ? (
            <span className="material-symbols-outlined animate-spin">refresh</span>
          ) : (
            <span className="material-symbols-outlined text-accent-pink">magic_button</span>
          )}
          <span className="text-glow">
            {loading ? "Analyzing Database..." : "Generate Deep Report"}
          </span>
        </button>
      </div>

      {/* Real-time Analysis (장식용) */}
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
          <h3 className="text-lg font-bold text-glow">
            {searched ? `Found ${influencers.length} Results` : "Trending Influencers"}
          </h3>
          <span className="text-accent-cyan text-xs font-semibold">View All</span>
        </div>
      </div>

      {/* Grid Cards (데이터 연동됨!) */}
      <div className="px-6 grid grid-cols-2 gap-4">
        {influencers.length > 0 ? (
          // 데이터가 있으면 map으로 반복해서 보여줌
          influencers.map((inf) => (
            // [수정 포인트] 원본 HTML과 맞추기 위해 hover 효과를 제거했습니다.
            <div key={inf.id} className="liquid-glass p-4 rounded-[2.5rem] border-white/20">
              <div className="relative mb-4">
                <img 
                  alt={inf.name} 
                  className="w-full aspect-square object-cover rounded-full border-2 border-white/30" 
                  src={inf.image}
                />
                <div className="absolute -bottom-1 -right-1 liquid-glass p-1 rounded-full border-white/40">
                  <span className="material-symbols-outlined text-accent-cyan text-xs fill-1">verified</span>
                </div>
              </div>
              <h4 className="font-bold text-sm truncate text-glow">{inf.name}</h4>
              <p className="text-[10px] text-accent-pink mb-2">{inf.category}</p>
              
              <div className="mt-2 space-y-1.5">
                <div className="flex justify-between text-[10px] font-bold text-accent-lavender">
                  <span>Consistency</span>
                  <span>{inf.consistency_score}%</span>
                </div>
                <div className="h-1.5 w-full bg-white/10 rounded-full overflow-hidden border border-white/5">
                  <div 
                    className="h-full bg-gradient-to-r from-accent-cyan to-accent-lavender rounded-full shadow-[0_0_8px_rgba(0,242,255,0.4)]" 
                    style={{width: `${inf.consistency_score}%`}}
                  ></div>
                </div>
              </div>
              <p className="mt-3 text-[10px] text-white/60 leading-relaxed italic line-clamp-2">
                "{inf.description}"
              </p>
            </div>
          ))
        ) : (
          // 데이터가 없을 때 보여줄 안내 문구
          <div className="col-span-2 text-center py-10 opacity-60">
            <span className="material-symbols-outlined text-4xl mb-2">search_off</span>
            <p className="text-sm">Search for a category to see results.</p>
            <p className="text-xs text-white/50">(Try: Tech, Beauty, Gaming)</p>
          </div>
        )}
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