"use client";

import { useEffect, useRef } from "react";
import Character from "../components/Character";
import CharacterMenu from "../components/CharacterMenu";
import ChatBox from "../components/ChatBox";
import { useStore } from "../store/store";

export default function Home() {
  const streamedText = useStore((s) => s.currentStreamText);
  const clearStream = useStore((s) => s.clearStream);
  const openModal = useStore((s) => s.openModal);

  const uiRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      if (!uiRef.current) return;
      console.log(openModal)
      // ✅ If any modal is open, allow all mouse events
      if (openModal) {
        window.electronAPI.setIgnoreMouseEvents(false);
        return;
      }

      const rect = uiRef.current.getBoundingClientRect();
      const isInside =
        e.clientX >= rect.left &&
        e.clientX <= rect.right &&
        e.clientY >= rect.top &&
        e.clientY <= rect.bottom;

      // Click-through outside UI
      window.electronAPI.setIgnoreMouseEvents(!isInside, { forward: true });
    };

    window.addEventListener("mousemove", handleMouseMove);
    return () => window.removeEventListener("mousemove", handleMouseMove);
  }, [openModal]);

  return (
    <main className="w-screen h-screen bg-transparent">
      <div
        ref={uiRef}
        className="fixed left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 flex flex-col items-center p-6"
      >
        {streamedText && (
          <div className="mb-2 px-3 py-2 bg-white rounded-lg shadow-md text-black relative">
            {streamedText}
            <button
              onClick={clearStream}
              className="absolute -top-2 -right-2 bg-red-500 text-white rounded-full w-5 h-5 text-xs"
            >
              ✕
            </button>
          </div>
        )}

        <CharacterMenu>
          <Character />
        </CharacterMenu>

        <div className="mt-2 w-64">
          <ChatBox />
        </div>
      </div>
    </main>
  );
}
