import React, { useState } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import rehypeRaw from 'rehype-raw';
import { ArrowLeft, ArrowRight, CheckCircle2, Circle, Copy, Check, BookOpen, Share2 } from 'lucide-react';
import roadmapData from '../roadmap-data.json';

export default function LessonView({ completedLessons, onToggleLesson }) {
  const { moduleId, lessonId } = useParams();
  const navigate = useNavigate();

  // Find module
  const moduleData = roadmapData.modules.find((m) => m.slug === moduleId);
  const lessons = moduleData ? moduleData.lessons : [];
  const lessonIndex = lessons.findIndex((l) => l.slug === lessonId);
  const lessonData = lessonIndex !== -1 ? lessons[lessonIndex] : null;

  const [copiedCode, setCopiedCode] = useState(null);

  if (!moduleData || !lessonData) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-20 text-center space-y-4">
        <h1 className="text-2xl font-bold text-slate-800">Không tìm thấy bài học</h1>
        <p className="text-slate-500">Bài học bạn yêu cầu không tồn tại.</p>
        <Link to="/" className="inline-flex items-center space-x-2 px-4 py-2 bg-indigo-600 text-white rounded-xl font-semibold hover:bg-indigo-700 transition-colors">
          <ArrowLeft className="w-4 h-4" />
          <span>Trở về Trang Chủ</span>
        </Link>
      </div>
    );
  }

  const isCompleted = completedLessons.has(lessonData.id);
  const prevLesson = lessonIndex > 0 ? lessons[lessonIndex - 1] : null;
  const nextLesson = lessonIndex < lessons.length - 1 ? lessons[lessonIndex + 1] : null;

  const handleCopy = (code, idx) => {
    navigator.clipboard.writeText(code);
    setCopiedCode(idx);
    setTimeout(() => setCopiedCode(null), 2000);
  };

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-10 space-y-8">
      
      {/* Breadcrumb */}
      <div className="flex items-center space-x-2 text-sm text-slate-500 flex-wrap gap-y-1">
        <Link to="/" className="hover:text-indigo-600 transition-colors">Trang chủ</Link>
        <span>/</span>
        <Link to={`/modules/${moduleData.slug}`} className="hover:text-indigo-600 transition-colors">{moduleData.title}</Link>
        <span>/</span>
        <span className="text-slate-800 font-semibold truncate max-w-xs">{lessonData.title}</span>
      </div>

      {/* Lesson Header Card */}
      <div className="bg-white rounded-3xl border border-slate-200 p-6 sm:p-8 shadow-sm space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div className="space-y-2">
            <span className="text-xs font-bold text-indigo-600 uppercase tracking-wider">
              Bài {lessonIndex + 1} / {lessons.length} trong module {moduleData.title}
            </span>
            <h1 className="text-2xl sm:text-4xl font-extrabold text-slate-900 leading-tight">
              {lessonData.title}
            </h1>
            {lessonData.original_title && lessonData.original_title !== lessonData.title && (
              <p className="text-sm text-slate-500">
                Tiêu đề gốc: <span className="italic">{lessonData.original_title}</span>
              </p>
            )}
          </div>

          <button
            onClick={() => onToggleLesson(lessonData.id)}
            className={`flex items-center space-x-2 px-5 py-3 rounded-2xl font-bold text-sm transition-all shadow-sm ${
              isCompleted
                ? 'bg-emerald-100 text-emerald-800 border border-emerald-200 hover:bg-emerald-200'
                : 'bg-indigo-600 text-white hover:bg-indigo-700 shadow-indigo-200'
            }`}
          >
            {isCompleted ? (
              <>
                <CheckCircle2 className="w-5 h-5 text-emerald-600" />
                <span>Đã Hoàn Thành</span>
              </>
            ) : (
              <>
                <Circle className="w-5 h-5" />
                <span>Đánh Dấu Hoàn Thành</span>
              </>
            )}
          </button>
        </div>
      </div>

      {/* Markdown Content Pane */}
      <article className="bg-white rounded-3xl border border-slate-200 p-6 sm:p-10 shadow-sm prose prose-slate max-w-none prose-headings:font-bold prose-headings:text-slate-900 prose-a:text-indigo-600 prose-code:text-indigo-700 prose-code:bg-indigo-50 prose-code:px-1.5 prose-code:py-0.5 prose-code:rounded prose-code:font-mono prose-code:text-sm prose-pre:bg-slate-950 prose-pre:text-slate-100 prose-pre:rounded-2xl">
        <ReactMarkdown
          remarkPlugins={[remarkGfm]}
          rehypePlugins={[rehypeRaw]}
          components={{
            code({ node, inline, className, children, ...props }) {
              const match = /language-(\w+)/.exec(className || '');
              const codeString = String(children).replace(/\n$/, '');
              const codeId = Math.random().toString();

              if (!inline && match) {
                return (
                  <div className="relative group my-6">
                    <div className="absolute right-3 top-3 z-10 flex items-center space-x-2">
                      <span className="text-xs uppercase text-slate-400 font-mono bg-slate-800 px-2 py-0.5 rounded">
                        {match[1]}
                      </span>
                      <button
                        onClick={() => handleCopy(codeString, codeId)}
                        className="p-1.5 rounded-lg bg-slate-800 text-slate-300 hover:text-white hover:bg-slate-700 transition-colors shadow"
                        title="Copy code"
                      >
                        {copiedCode === codeId ? <Check className="w-4 h-4 text-emerald-400" /> : <Copy className="w-4 h-4" />}
                      </button>
                    </div>
                    <pre className="!bg-slate-950 !p-4 !rounded-2xl overflow-x-auto text-sm font-mono text-slate-100">
                      <code className={className} {...props}>
                        {children}
                      </code>
                    </pre>
                  </div>
                );
              }
              return (
                <code className={className} {...props}>
                  {children}
                </code>
              );
            }
          }}
        >
          {lessonData.content.replace(/^---[\s\S]*?---/, '')}
        </ReactMarkdown>
      </article>

      {/* Bottom Navigation Footer */}
      <div className="flex flex-col sm:flex-row items-center justify-between gap-4 pt-4 border-t border-slate-200">
        {prevLesson ? (
          <Link
            to={`/modules/${moduleData.slug}/lessons/${prevLesson.slug}`}
            className="w-full sm:w-auto flex items-center space-x-3 px-5 py-3 rounded-2xl bg-white border border-slate-200 text-slate-700 hover:border-indigo-300 hover:text-indigo-600 transition-all font-semibold text-sm shadow-sm"
          >
            <ArrowLeft className="w-4 h-4" />
            <div className="text-left">
              <div className="text-xs text-slate-400 font-normal">Bài trước</div>
              <div className="truncate max-w-xs">{prevLesson.title}</div>
            </div>
          </Link>
        ) : <div />}

        {nextLesson ? (
          <Link
            to={`/modules/${moduleData.slug}/lessons/${nextLesson.slug}`}
            onClick={() => {
              if (!isCompleted) onToggleLesson(lessonData.id);
            }}
            className="w-full sm:w-auto flex items-center justify-end space-x-3 px-6 py-3 rounded-2xl bg-indigo-600 text-white hover:bg-indigo-700 transition-all font-semibold text-sm shadow-md shadow-indigo-200 ml-auto"
          >
            <div className="text-right">
              <div className="text-xs text-indigo-200 font-normal">Tiếp theo & Hoàn thành</div>
              <div className="truncate max-w-xs">{nextLesson.title}</div>
            </div>
            <ArrowRight className="w-4 h-4" />
          </Link>
        ) : (
          <Link
            to={`/modules/${moduleData.slug}`}
            className="w-full sm:w-auto flex items-center justify-center space-x-2 px-6 py-3 rounded-2xl bg-emerald-600 text-white hover:bg-emerald-700 transition-all font-semibold text-sm shadow-md shadow-emerald-200 ml-auto"
          >
            <CheckCircle2 className="w-4 h-4" />
            <span>Hoàn thành Module này</span>
          </Link>
        )}
      </div>

    </div>
  );
}
