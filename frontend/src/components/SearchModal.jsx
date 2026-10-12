import React, { useState, useEffect } from 'react';
import { Search, X, BookOpen, FileText, ArrowRight } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import roadmapData from '../roadmap-data.json';

export default function SearchModal({ isOpen, onClose }) {
  const [query, setQuery] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const handleKeyDown = (e) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        if (isOpen) onClose();
        else {
          // trigger open
        }
      }
      if (e.key === 'Escape' && isOpen) {
        onClose();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  // Flatten modules and lessons for searching
  const results = [];
  if (query.trim().length > 0) {
    const q = query.toLowerCase();
    roadmapData.modules.forEach((mod) => {
      if (mod.title.toLowerCase().includes(q) || mod.slug.toLowerCase().includes(q)) {
        results.push({ type: 'module', title: mod.title, slug: mod.slug, moduleSlug: mod.slug });
      }
      mod.lessons.forEach((les) => {
        if (les.title.toLowerCase().includes(q) || les.original_title.toLowerCase().includes(q) || les.content.toLowerCase().includes(q)) {
          results.push({
            type: 'lesson',
            title: les.title,
            originalTitle: les.original_title,
            slug: les.slug,
            moduleSlug: mod.slug,
            moduleTitle: mod.title
          });
        }
      });
    });
  }

  return (
    <div className="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-sm flex items-start justify-center pt-20 px-4">
      <div className="bg-white rounded-2xl shadow-2xl w-full max-w-2xl overflow-hidden border border-slate-200 animate-in fade-in zoom-in duration-200">
        <div className="flex items-center px-4 py-3 border-b border-slate-100">
          <Search className="w-5 h-5 text-slate-400 mr-3" />
          <input
            type="text"
            placeholder="Tìm kiếm module, bài học, hoặc từ khóa (VD: RAG, MCP, Prompt)..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            autoFocus
            className="w-full text-slate-800 placeholder-slate-400 outline-none text-base"
          />
          <button
            onClick={onClose}
            className="p-1.5 text-slate-400 hover:text-slate-600 rounded-lg hover:bg-slate-100 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="max-h-[60vh] overflow-y-auto p-4 space-y-2">
          {query.trim().length === 0 ? (
            <div className="text-center py-12 text-slate-400">
              <Search className="w-10 h-10 mx-auto mb-3 opacity-40" />
              <p className="text-sm font-medium">Nhập từ khóa để tìm kiếm trong toàn bộ 20 module và 311 bài học.</p>
            </div>
          ) : results.length === 0 ? (
            <div className="text-center py-12 text-slate-400">
              <p className="text-sm font-medium">Không tìm thấy kết quả nào cho "{query}"</p>
            </div>
          ) : (
            results.slice(0, 30).map((item, idx) => (
              <div
                key={idx}
                onClick={() => {
                  if (item.type === 'module') {
                    navigate(`/modules/${item.slug}`);
                  } else {
                    navigate(`/modules/${item.moduleSlug}/lessons/${item.slug}`);
                  }
                  onClose();
                }}
                className="flex items-center justify-between p-3 rounded-xl hover:bg-indigo-50/80 cursor-pointer transition-colors group border border-transparent hover:border-indigo-100"
              >
                <div className="flex items-center space-x-3">
                  <div className={`p-2 rounded-lg ${item.type === 'module' ? 'bg-indigo-100 text-indigo-600' : 'bg-slate-100 text-slate-600 group-hover:bg-indigo-200 group-hover:text-indigo-700'}`}>
                    {item.type === 'module' ? <BookOpen className="w-4 h-4" /> : <FileText className="w-4 h-4" />}
                  </div>
                  <div>
                    <div className="text-sm font-semibold text-slate-800 group-hover:text-indigo-900">{item.title}</div>
                    {item.type === 'lesson' && (
                      <div className="text-xs text-slate-500">Module: {item.moduleTitle}</div>
                    )}
                  </div>
                </div>
                <ArrowRight className="w-4 h-4 text-slate-400 group-hover:text-indigo-600 group-hover:translate-x-0.5 transition-all" />
              </div>
            ))
          )}
        </div>

        <div className="bg-slate-50 px-4 py-2.5 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
          <span>Gợi ý: Nhấn <kbd className="px-1.5 py-0.5 bg-white border border-slate-200 rounded shadow-sm">ESC</kbd> để đóng</span>
          <span>Hiển thị tối đa 30 kết quả</span>
        </div>
      </div>
    </div>
  );
}
