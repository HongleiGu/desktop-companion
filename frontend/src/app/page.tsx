"use client"

import Character from "../components/Character";
import ChatBox from "../components/ChatBox";
import { useStore } from "../store/store";
import { useState } from "react";

export default function Home() {
  const streamedText = useStore((s) => s.currentStreamText);
  const clearStream = useStore((s) => s.clearStream);
  // const [showBubble, setShowBubble] = useState(true);

  return (
    <div className="fixed left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 flex flex-col items-center pointer-events-none">

      {/* Typewriter Bubble */}
      {streamedText && (
        <div className="mb-2 px-3 py-2 bg-white rounded-lg shadow-md text-black max-w-xs text-sm pointer-events-auto
                        max-h-40 overflow-auto relative">
          {streamedText}
          <span className="blink absolute right-2 top-2">|</span>
          {/* Manual close button */}
          <button
            onClick={() => {
              clearStream();
              // setShowBubble(false);
            }}
            className="absolute top-1 right-1 text-gray-500 hover:text-gray-800 text-xs"
          >
            ✕
          </button>
        </div>
      )}

      {/* Character */}
      <div className="pointer-events-auto">
        <Character />
      </div>

      {/* ChatBox */}
      <div className="mt-2 pointer-events-auto w-64">
        <ChatBox />
      </div>
    </div>
  );
}
