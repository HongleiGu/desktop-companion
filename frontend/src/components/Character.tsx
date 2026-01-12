"use client";

import { useEffect, useRef } from "react";
import { IMAGE_MAP } from "../utils/const";
import { useStore } from "../store/store";
import ChatBox from "./ChatBox";

export default function Character() {
  const setCharacterState = useStore((s) => s.setCharacterState);
  const characterState = useStore((s) => s.characterState);
  const setFiles = useStore((s) => s.setFiles)


  // Track timers + previous state safely
  const timerRef = useRef<number | null>(null);
  const baseStateRef = useRef<typeof characterState | null>(null);

  // --- Idle → Blink logic ---
  useEffect(() => {
    if (characterState !== "idle") return;

    const delay = 2000 + Math.random() * 4000; // 2–6s

    timerRef.current = window.setTimeout(() => {
      // still idle? then blink
      if (useStore.getState().characterState !== "idle") return;

      baseStateRef.current = "idle";
      setCharacterState("blink");

      // blink duration
      setTimeout(() => {
        // restore only if nothing else took over
        if (useStore.getState().characterState === "blink") {
          setCharacterState("idle");
        }
      }, 150);
    }, delay);

    return () => {
      if (timerRef.current) {
        clearTimeout(timerRef.current);
        timerRef.current = null;
      }
    };
  }, [characterState, setCharacterState]);

  // --- Thinking → eyes closed logic ---
  useEffect(() => {
    if (characterState !== "thinking-eyes-open") return;

    const delay = 2500 + Math.random() * 3000;

    timerRef.current = window.setTimeout(() => {
      if (useStore.getState().characterState !== "thinking-eyes-open") return;

      baseStateRef.current = "thinking-eyes-open";
      setCharacterState("thinking-eyes-closed");

      setTimeout(() => {
        if (
          useStore.getState().characterState === "thinking-eyes-closed"
        ) {
          setCharacterState("thinking-eyes-open");
        }
      }, 200);
    }, delay);

    return () => {
      if (timerRef.current) {
        clearTimeout(timerRef.current);
        timerRef.current = null;
      }
    };
  }, [characterState, setCharacterState]);

  // --- Mouse interactions ---
  const handleMouseDown = (e: React.MouseEvent) => {
    e.preventDefault();
    if (e.button === 0) {
      setCharacterState("drag");
    }
  };

  const handleMouseUp = (e: React.MouseEvent) => {
    e.preventDefault();

    // restore to safe base
    const current = useStore.getState().characterState;
    if (current === "drag") {
      setCharacterState("idle");
    }
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault(); // allow drop
    setCharacterState("awaiting-file"); // optional visual feedback
  };

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault();
    setCharacterState("idle"); // reset visual
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    const files = Array.from(e.dataTransfer.files); // get the files

    if (files.length > 0) {
      setFiles(files)
    }

    setCharacterState("idle"); // reset after drop
  };


  return (
    <div 
      style={{
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        flexDirection: "column"
      }}
    >
      <div
        onMouseDown={handleMouseDown}
        onMouseUp={handleMouseUp}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        style={{
          width: 150,
          height: 150,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          userSelect: "none",
        }}
      >
        <img
          src={IMAGE_MAP[characterState]}
          alt="Character"
          draggable={false}
          style={{
            width: "100%",
            height: "100%",
            objectFit: "contain",
            pointerEvents: "none",
          }}
        />
      </div>
      <div className="mt-2 w-64">
        <ChatBox />
      </div>
    </div>
  );
}
