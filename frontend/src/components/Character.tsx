"use client";

import CharacterMenu from "./CharacterMenu";
import { getCurrentWindow } from "@tauri-apps/api/window";

export default function Character() {
  
  const handleMouseDown = async (e: React.MouseEvent) => {
    // 0 = Left Click, 1 = Middle Click, 2 = Right Click
    if (e.button === 0) {
      try {
        const win = getCurrentWindow();
        await win.startDragging();
      } catch (err) {
        console.error("Failed to start dragging:", err);
      }
    }
    // We do NOT call e.preventDefault() here so that 
    // the right-click event can still bubble up to the Dropdown.
  };

  return (
    <CharacterMenu>
      <div
        onMouseDown={handleMouseDown}
        style={{
          width: 150,
          height: 150,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          cursor: "grab",
          // Essential for frameless: prevents ghosting and text selection
          userSelect: "none",
          // WebkitAppRegion: "no-drag" // Ensures CSS doesn't conflict with Tauri's manual drag
        }}
      >
        <img
          src="/character/idle.png"
          alt="Character"
          draggable={false} // Prevents browser image-dragging behavior
          style={{
            width: "100%",
            height: "100%",
            objectFit: "contain",
            pointerEvents: "none" 
          }}
        />
      </div>
    </CharacterMenu>
  );
}