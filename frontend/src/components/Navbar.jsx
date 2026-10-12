import React from 'react';
import { Search, Compass, Menu, CheckCircle2, BookOpen } from 'lucide-react';
import { Link } from 'react-router-dom';
import roadmapData from '../roadmap-data.json';

export default function Navbar({ onOpenSearch, onToggleMobileSidebar, completedCount }) {
  const totalLessons = roadmapData.total_lessons || 167;
  const progressPercent = Math.round((completedCount / totalLessons) * 100) || 0;

  return (
    <header className="sticky top-0 z-40 bg-white/90 backdrop-blur-md border-b border-slate-200/80">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        
        {/* Left: Brand + Mobile Menu */}
        <div className="flex items-center space-x-3">
          <button
            onClick={onToggleMobileSidebar}
            className="md:hidden p-2 text-slate-600 hover:text-slate-900 rounded-lg hover:bg-slate-100 transition-colors"
            aria-label="Toggle menu"
          >
            <Menu className="w-5 h-5" />
          </button>
          
          <Link to="/" className="flex items-center space-x-2.5 group">
            <div className="w-10 h-10 rounded-xl bg-indigo-600 text-white flex items-center justify-center font-bold shadow-md shadow-indigo-200 group-hover:bg-indigo-700 transition-colors">
              <Compass className="w-6 h-6" />
            </div>
            <div>
              <span className="font-bold text-slate-900 tracking-tight text-lg group-hover:text-indigo-600 transition-colors">
                AI Engineering VN
              </span>
              <span className="hidden sm:block text-xs text-slate-500 font-medium">
                Lộ trình Kỹ sư AI Tiếng Việt
              </span>
            </div>
          </Link>
        </div>

        {/* Center: Search Trigger */}
        <div className="flex-1 max-w-md mx-4 hidden md:block">
          <button
            onClick={onOpenSearch}
            className="w-full flex items-center justify-between px-4 py-2 bg-slate-100 hover:bg-slate-200/70 border border-slate-200 rounded-xl text-slate-500 text-sm transition-all shadow-sm group"
          >
            <div className="flex items-center space-x-2">
              <Search className="w-4 h-4 text-slate-400 group-hover:text-slate-600" />
              <span>Tìm kiếm bài học, module, kỹ thuật...</span>
            </div>
            <kbd className="hidden lg:inline-flex items-center px-2 py-0.5 text-xs font-semibold text-slate-500 bg-white border border-slate-200 rounded shadow-sm">
              Ctrl K
            </kbd>
          </button>
        </div>

        {/* Right: Progress Indicator & Mobile Search */}
        <div className="flex items-center space-x-3">
          <button
            onClick={onOpenSearch}
            className="md:hidden p-2 text-slate-600 hover:text-slate-900 rounded-lg hover:bg-slate-100 transition-colors"
            aria-label="Search"
          >
            <Search className="w-5 h-5" />
          </button>

          <div className="hidden sm:flex items-center space-x-2.5 bg-indigo-50 border border-indigo-100 px-3 py-1.5 rounded-xl">
            <CheckCircle2 className="w-4 h-4 text-indigo-600" />
            <div className="text-xs">
              <span className="font-bold text-indigo-900">{completedCount}</span>
              <span className="text-indigo-700"> / {totalLessons} bài ({progressPercent}%)</span>
            </div>
          </div>
        </div>

      </div>
    </header>
  );
}
