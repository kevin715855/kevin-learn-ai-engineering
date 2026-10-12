import React from 'react';
import { Link } from 'react-router-dom';
import { BookOpen, CheckCircle2, Trophy, ArrowRight, Sparkles, Compass } from 'lucide-react';
import roadmapData from '../roadmap-data.json';

export default function Home({ completedLessons }) {
  const totalModules = roadmapData.modules.length;
  const totalLessons = roadmapData.total_lessons;
  const completedCount = completedLessons.size;
  const progressPercent = Math.round((completedCount / totalLessons) * 100) || 0;

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-10 space-y-12">
      
      {/* Hero Banner */}
      <div className="bg-gradient-to-br from-indigo-900 via-indigo-800 to-slate-900 rounded-3xl p-8 sm:p-12 text-white shadow-xl relative overflow-hidden">
        <div className="absolute right-0 top-0 translate-x-12 -translate-y-12 w-96 h-96 bg-indigo-500/20 rounded-full blur-3xl pointer-events-none" />
        
        <div className="relative z-10 max-w-2xl space-y-4">
          <div className="inline-flex items-center space-x-2 bg-indigo-500/30 border border-indigo-400/30 px-3 py-1 rounded-full text-xs font-semibold text-indigo-200">
            <Sparkles className="w-3.5 h-3.5 text-indigo-300" />
            <span>Phiên bản Tiếng Việt Hoàn Chỉnh</span>
          </div>
          
          <h1 className="text-3xl sm:text-4xl lg:text-5xl font-extrabold tracking-tight leading-tight">
            Lộ Trình Kỹ Sư AI (AI Engineer Roadmap)
          </h1>
          
          <p className="text-slate-300 text-base sm:text-lg leading-relaxed">
            Nền tảng học tập toàn diện từ cơ bản đến nâng cao: Mô hình ngôn ngữ lớn (LLM), Prompt Engineering, RAG, AI Agents, Vector Databases và MLOps.
          </p>

          <div className="pt-4 flex flex-wrap items-center gap-4">
            <Link
              to={`/modules/${roadmapData.modules[0]?.slug}`}
              className="px-6 py-3 bg-white text-indigo-900 font-bold rounded-xl shadow-lg hover:bg-indigo-50 transition-all flex items-center space-x-2"
            >
              <span>Bắt Đầu Học Ngay</span>
              <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
        </div>

        {/* Progress Card Inside Hero */}
        <div className="mt-8 pt-8 border-t border-indigo-700/60 grid grid-cols-2 sm:grid-cols-3 gap-6">
          <div>
            <div className="text-2xl sm:text-3xl font-extrabold text-white">{totalModules}</div>
            <div className="text-xs sm:text-sm text-indigo-200 font-medium">Module Chủ Đề</div>
          </div>
          <div>
            <div className="text-2xl sm:text-3xl font-extrabold text-white">{totalLessons}</div>
            <div className="text-xs sm:text-sm text-indigo-200 font-medium">Bài Học Chi Tiết</div>
          </div>
          <div className="col-span-2 sm:col-span-1">
            <div className="flex items-center justify-between mb-1">
              <span className="text-xs sm:text-sm text-indigo-200 font-medium">Tiến độ của bạn</span>
              <span className="text-xs sm:text-sm font-bold text-white">{progressPercent}%</span>
            </div>
            <div className="w-full bg-indigo-950/80 rounded-full h-2.5 overflow-hidden">
              <div
                className="bg-emerald-400 h-2.5 rounded-full transition-all duration-500"
                style={{ width: `${progressPercent}%` }}
              />
            </div>
          </div>
        </div>
      </div>

      {/* Modules Grid */}
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <h2 className="text-2xl font-bold text-slate-900">Danh Sách Các Module Học Tập</h2>
          <span className="text-sm font-semibold text-slate-500">{totalModules} chủ đề chính</span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {roadmapData.modules.map((mod, index) => {
            const completedInMod = mod.lessons.filter((l) => completedLessons.has(l.id)).length;
            const totalInMod = mod.lessons.length;
            const modPercent = totalInMod > 0 ? Math.round((completedInMod / totalInMod) * 100) : 0;
            const isFinished = completedInMod === totalInMod && totalInMod > 0;

            return (
              <Link
                key={mod.id}
                to={`/modules/${mod.slug}`}
                className="group bg-white rounded-2xl border border-slate-200 p-6 shadow-sm hover:shadow-xl hover:border-indigo-200 transition-all flex flex-col justify-between space-y-4 relative overflow-hidden"
              >
                {/* Top accent */}
                <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-indigo-500 to-violet-500 opacity-0 group-hover:opacity-100 transition-opacity" />

                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="w-8 h-8 rounded-xl bg-indigo-50 text-indigo-600 font-bold flex items-center justify-center text-sm group-hover:bg-indigo-600 group-hover:text-white transition-colors">
                      {index + 1}
                    </span>
                    {isFinished ? (
                      <span className="inline-flex items-center space-x-1 px-2.5 py-1 bg-emerald-50 text-emerald-700 text-xs font-bold rounded-full">
                        <CheckCircle2 className="w-3.5 h-3.5" />
                        <span>Hoàn thành</span>
                      </span>
                    ) : (
                      <span className="text-xs font-semibold text-slate-400">
                        {completedInMod}/{totalInMod} bài
                      </span>
                    )}
                  </div>

                  <h3 className="text-lg font-bold text-slate-900 group-hover:text-indigo-600 transition-colors">
                    {mod.title}
                  </h3>

                  <p className="text-xs text-slate-500 line-clamp-2">
                    Khám phá {totalInMod} bài học chuyên sâu về {mod.title} theo chuẩn roadmap.sh được dịch thuật và chuẩn hóa sang tiếng Việt.
                  </p>
                </div>

                <div className="space-y-3 pt-4 border-t border-slate-100">
                  {/* Progress bar */}
                  <div className="w-full bg-slate-100 rounded-full h-1.5 overflow-hidden">
                    <div
                      className="bg-indigo-600 h-1.5 rounded-full transition-all duration-300"
                      style={{ width: `${modPercent}%` }}
                    />
                  </div>

                  <div className="flex items-center justify-between text-xs font-semibold text-indigo-600 group-hover:translate-x-1 transition-transform">
                    <span>Xem chi tiết module</span>
                    <ArrowRight className="w-4 h-4" />
                  </div>
                </div>
              </Link>
            );
          })}
        </div>
      </div>

    </div>
  );
}
