import React from 'react';
import { Link, useParams } from 'react-router-dom';
import { BookOpen, CheckCircle2, ChevronRight, Home } from 'lucide-react';
import roadmapData from '../roadmap-data.json';

export default function Sidebar({ completedLessons, isOpen, onClose }) {
  const { moduleId, lessonId } = useParams();

  return (
    <>
      {/* Mobile Backdrop */}
      {isOpen && (
        <div
          onClick={onClose}
          className="fixed inset-0 z-40 bg-slate-900/50 backdrop-blur-sm md:hidden"
        />
      )}

      <aside
        className={`fixed md:sticky top-16 z-40 h-[calc(100vh-4rem)] w-80 bg-white border-r border-slate-200 overflow-y-auto transition-transform duration-300 transform ${
          isOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0'
        }`}
      >
        <div className="p-4 space-y-6">
          {/* Home Link */}
          <Link
            to="/"
            onClick={onClose}
            className={`flex items-center space-x-3 px-3 py-2.5 rounded-xl text-sm font-semibold transition-colors ${
              !moduleId ? 'bg-indigo-600 text-white shadow-md shadow-indigo-100' : 'text-slate-700 hover:bg-slate-100'
            }`}
          >
            <Home className="w-4 h-4" />
            <span>Trang Chủ / Tổng Quan</span>
          </Link>

          {/* Modules Navigation */}
          <div className="space-y-4">
            <div className="px-3 text-xs font-bold text-slate-400 uppercase tracking-wider">
              Danh Sách Module ({roadmapData.modules.length})
            </div>

            <div className="space-y-1.5">
              {roadmapData.modules.map((mod, index) => {
                const isCurrentModule = moduleId === mod.slug;
                const modCompleted = mod.lessons.filter((l) => completedLessons.has(l.id)).length;
                const isModFinished = modCompleted === mod.lessons.length && mod.lessons.length > 0;

                return (
                  <div key={mod.id} className="space-y-1">
                    <Link
                      to={`/modules/${mod.slug}`}
                      onClick={onClose}
                      className={`flex items-center justify-between px-3 py-2.5 rounded-xl text-sm font-medium transition-all ${
                        isCurrentModule
                          ? 'bg-indigo-50 text-indigo-700 font-semibold border border-indigo-100'
                          : 'text-slate-700 hover:bg-slate-100'
                      }`}
                    >
                      <div className="flex items-center space-x-2.5 truncate">
                        <span className={`w-6 h-6 rounded-lg flex items-center justify-center text-xs font-bold ${
                          isModFinished ? 'bg-emerald-100 text-emerald-700' : 'bg-slate-100 text-slate-600'
                        }`}>
                          {index + 1}
                        </span>
                        <span className="truncate">{mod.title}</span>
                      </div>
                      {isModFinished && <CheckCircle2 className="w-4 h-4 text-emerald-600 flex-shrink-0" />}
                    </Link>

                    {/* If module is active, list its lessons */}
                    {isCurrentModule && (
                      <div className="pl-6 pr-1 space-y-1 py-1 border-l-2 border-indigo-200 ml-5 my-1">
                        {mod.lessons.map((les) => {
                          const isCurrentLesson = lessonId === les.slug;
                          const isCompleted = completedLessons.has(les.id);

                          return (
                            <Link
                              key={les.id}
                              to={`/modules/${mod.slug}/lessons/${les.slug}`}
                              onClick={onClose}
                              className={`flex items-center justify-between px-2.5 py-1.5 rounded-lg text-xs transition-colors ${
                                isCurrentLesson
                                  ? 'bg-indigo-600 text-white font-semibold shadow-sm'
                                  : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
                              }`}
                            >
                              <span className="truncate pr-2">{les.title}</span>
                              {isCompleted && (
                                <CheckCircle2 className={`w-3.5 h-3.5 flex-shrink-0 ${isCurrentLesson ? 'text-white' : 'text-emerald-600'}`} />
                              )}
                            </Link>
                          );
                        })}
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      </aside>
    </>
  );
}
