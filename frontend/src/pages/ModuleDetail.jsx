import React from 'react';
import { useParams, Link } from 'react-router-dom';
import { BookOpen, CheckCircle2, Circle, ArrowLeft, ArrowRight, Clock, Sparkles } from 'lucide-react';
import roadmapData from '../roadmap-data.json';

export default function ModuleDetail({ completedLessons, onToggleLesson }) {
  const { moduleId } = useParams();
  const moduleData = roadmapData.modules.find((m) => m.slug === moduleId);

  if (!moduleData) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-20 text-center space-y-4">
        <h1 className="text-2xl font-bold text-slate-800">Không tìm thấy module</h1>
        <p className="text-slate-500">Module bạn đang tìm kiếm không tồn tại hoặc đã bị di chuyển.</p>
        <Link to="/" className="inline-flex items-center space-x-2 px-4 py-2 bg-indigo-600 text-white rounded-xl font-semibold hover:bg-indigo-700 transition-colors">
          <ArrowLeft className="w-4 h-4" />
          <span>Trở về Trang Chủ</span>
        </Link>
      </div>
    );
  }

  const totalInMod = moduleData.lessons.length;
  const completedInMod = moduleData.lessons.filter((l) => completedLessons.has(l.id)).length;
  const modPercent = totalInMod > 0 ? Math.round((completedInMod / totalInMod) * 100) : 0;

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-10 space-y-8">
      
      {/* Breadcrumb */}
      <div className="flex items-center space-x-2 text-sm text-slate-500">
        <Link to="/" className="hover:text-indigo-600 transition-colors">Trang chủ</Link>
        <span>/</span>
        <span className="text-slate-800 font-semibold">{moduleData.title}</span>
      </div>

      {/* Module Header Card */}
      <div className="bg-white rounded-3xl border border-slate-200 p-6 sm:p-8 shadow-sm space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div className="space-y-2">
            <div className="inline-flex items-center space-x-2 bg-indigo-50 text-indigo-700 px-3 py-1 rounded-full text-xs font-bold">
              <Sparkles className="w-3.5 h-3.5" />
              <span>Module Học Tập Chuyên Sâu</span>
            </div>
            <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900">
              {moduleData.title}
            </h1>
            <p className="text-slate-600 text-sm sm:text-base">
              Danh sách các bài học chuẩn hóa tiếng Việt giúp bạn nắm vững toàn bộ kiến thức và kỹ năng thực chiến của chủ đề này.
            </p>
          </div>

          <div className="bg-slate-50 border border-slate-200 rounded-2xl p-4 text-center sm:min-w-[160px]">
            <div className="text-2xl font-extrabold text-indigo-600">{completedInMod} / {totalInMod}</div>
            <div className="text-xs text-slate-500 font-medium mt-0.5">Bài đã hoàn thành ({modPercent}%)</div>
          </div>
        </div>

        {/* Progress Bar */}
        <div className="w-full bg-slate-100 rounded-full h-2.5 overflow-hidden">
          <div
            className="bg-indigo-600 h-2.5 rounded-full transition-all duration-500"
            style={{ width: `${modPercent}%` }}
          />
        </div>
      </div>

      {/* Lessons List */}
      <div className="space-y-4">
        <h2 className="text-xl font-bold text-slate-900">Nội Dung Bài Học Trong Module</h2>

        <div className="space-y-3">
          {moduleData.lessons.map((les, index) => {
            const isCompleted = completedLessons.has(les.id);

            return (
              <div
                key={les.id}
                className={`flex items-center justify-between p-4 rounded-2xl border transition-all bg-white ${
                  isCompleted ? 'border-emerald-200 bg-emerald-50/20 shadow-sm' : 'border-slate-200 hover:border-indigo-200 hover:shadow-md'
                }`}
              >
                <div className="flex items-center space-x-4 flex-1 min-w-0 pr-4">
                  <button
                    onClick={() => onToggleLesson(les.id)}
                    className="flex-shrink-0 text-slate-400 hover:text-emerald-600 transition-colors"
                    title={isCompleted ? "Đánh dấu chưa học" : "Đánh dấu đã hoàn thành"}
                  >
                    {isCompleted ? (
                      <CheckCircle2 className="w-6 h-6 text-emerald-600 fill-emerald-100" />
                    ) : (
                      <Circle className="w-6 h-6 text-slate-300" />
                    )}
                  </button>

                  <div className="min-w-0 flex-1">
                    <div className="flex items-center space-x-2">
                      <span className="text-xs font-bold text-slate-400">#{index + 1}</span>
                      <Link
                        to={`/modules/${moduleData.slug}/lessons/${les.slug}`}
                        className="text-base font-bold text-slate-900 hover:text-indigo-600 truncate transition-colors"
                      >
                        {les.title}
                      </Link>
                    </div>
                    {les.original_title && les.original_title !== les.title && (
                      <div className="text-xs text-slate-500 truncate mt-0.5">
                        Bản gốc: {les.original_title}
                      </div>
                    )}
                  </div>
                </div>

                <Link
                  to={`/modules/${moduleData.slug}/lessons/${les.slug}`}
                  className="flex items-center space-x-1.5 px-4 py-2 rounded-xl bg-indigo-50 text-indigo-700 text-xs font-bold hover:bg-indigo-600 hover:text-white transition-all flex-shrink-0"
                >
                  <span>Học Bài</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </Link>
              </div>
            );
          })}
        </div>
      </div>

    </div>
  );
}
