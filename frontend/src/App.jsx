import React, { useState, useEffect } from 'react';
import { Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Sidebar from './components/Sidebar';
import SearchModal from './components/SearchModal';
import Home from './pages/Home';
import ModuleDetail from './pages/ModuleDetail';
import LessonView from './pages/LessonView';

export default function App() {
  const [isSearchOpen, setIsSearchOpen] = useState(false);
  const [isMobileSidebarOpen, setIsMobileSidebarOpen] = useState(false);

  // Completed lessons stored in localStorage
  const [completedLessons, setCompletedLessons] = useState(() => {
    try {
      const saved = localStorage.getItem('ai_roadmap_completed_lessons');
      return saved ? new Set(JSON.parse(saved)) : new Set();
    } catch {
      return new Set();
    }
  });

  useEffect(() => {
    try {
      localStorage.setItem(
        'ai_roadmap_completed_lessons',
        JSON.stringify(Array.from(completedLessons))
      );
    } catch (err) {
      console.error('Failed to save progress to localStorage', err);
    }
  }, [completedLessons]);

  const handleToggleLesson = (lessonId) => {
    setCompletedLessons((prev) => {
      const next = new Set(prev);
      if (next.has(lessonId)) {
        next.delete(lessonId);
      } else {
        next.add(lessonId);
      }
      return next;
    });
  };

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col">
      <Navbar
        onOpenSearch={() => setIsSearchOpen(true)}
        onToggleMobileSidebar={() => setIsMobileSidebarOpen(!isMobileSidebarOpen)}
        completedCount={completedLessons.size}
      />

      <div className="flex-1 flex">
        <Sidebar
          completedLessons={completedLessons}
          isOpen={isMobileSidebarOpen}
          onClose={() => setIsMobileSidebarOpen(false)}
        />

        <main className="flex-1 min-w-0">
          <Routes>
            <Route path="/" element={<Home completedLessons={completedLessons} />} />
            <Route
              path="/modules/:moduleId"
              element={
                <ModuleDetail
                  completedLessons={completedLessons}
                  onToggleLesson={handleToggleLesson}
                />
              }
            />
            <Route
              path="/modules/:moduleId/lessons/:lessonId"
              element={
                <LessonView
                  completedLessons={completedLessons}
                  onToggleLesson={handleToggleLesson}
                />
              }
            />
          </Routes>
        </main>
      </div>

      <SearchModal
        isOpen={isSearchOpen}
        onClose={() => setIsSearchOpen(false)}
      />
    </div>
  );
}
