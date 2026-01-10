"use client";

import { Dropdown } from "antd";
import type { MenuProps } from "antd";
import { useRef } from "react";
import Modals from "./Modals";
import { useStore } from "../store/store";

type MenuType = "history" | "profile" | "settings" | "exit";

export default function CharacterMenu({ children }: { children: React.ReactNode }) {
  const containerRef = useRef<HTMLDivElement>(null);

  // ✅ Use global store for modal state
  const openModal = useStore((s) => s.openModal);
  const setOpenModal = useStore((s) => s.setOpenModal);

  // Menu items
  const items: MenuProps["items"] = [
    { key: "history", label: "历史记录" },
    { key: "profile", label: "用户档案" },
    { key: "settings", label: "设置" },
    { type: "divider" },
    { key: "exit", label: "退出" }
  ];

  // Menu click handler
  const onClick: MenuProps["onClick"] = ({ key }) => {
    const typedKey = key as MenuType;
    if (typedKey === "exit") {
      window.close();
      return;
    }

    // ✅ Open the selected modal
    setOpenModal(typedKey);
  };

  // Electron drag logic
  const handleMouseDown = (e: React.MouseEvent) => {
    if (e.button === 0) {
      window.electronAPI.startDrag();

      const handleMouseUp = () => {
        window.electronAPI.stopDrag();
        window.removeEventListener("mouseup", handleMouseUp);
      };
      window.addEventListener("mouseup", handleMouseUp);
    }
  };

  return (
    <div ref={containerRef} className="interactive">
      <Dropdown
        trigger={["contextMenu"]}
        menu={{ items, onClick }}
        getPopupContainer={() => containerRef.current!}
      >
        <div 
          onMouseDown={handleMouseDown}
          className="cursor-grab active:cursor-grabbing"
        >
          {children}
        </div>
      </Dropdown>

      {/* ✅ Modals read from global state */}
      <Modals />
    </div>
  );
}
