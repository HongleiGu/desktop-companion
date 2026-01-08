"use client";
import { Dropdown, Modal } from "antd";
import type { MenuProps } from "antd";
import { useRef, useState } from "react";

import HistoryPanel from "./HistoryPanel"; // your existing history list
import UserProfileForm from "./UserProfile";
import PromptEditor from "./PromptEditor";

export default function CharacterMenu({
  children
}: {
  children: React.ReactNode;
}) {
  const [openModal, setOpenModal] = useState<
    string | null
  >(null);

  const containerRef = useRef<HTMLDivElement>(null);

  const items: MenuProps["items"] = [
    { key: "history", label: "历史记录" },
    { key: "profile", label: "用户档案" },
    { key: "settings", label: "设置" },
    { type: "divider" },
    { key: "exit", label: "退出" }
  ];

  const onClick: MenuProps["onClick"] = ({ key }) => {
    if (key === "exit") {
      window.close(); // replace with tauri API later
      return;
    }
    setOpenModal(key);
  };

  return (
    <div ref={containerRef} className="pointer-events-auto">
      <Dropdown 
        trigger={["contextMenu"]} // Changed from "click" to "contextMenu"
        menu={{ items, onClick }}
        getPopupContainer={() => containerRef.current!}
      >
        {/* Wrap children in a div that ensures pointer events are active */}
        <div className="pointer-events-auto">{children}</div>
      </Dropdown>

      {/* 历史记录 */}
      <Modal
        open={openModal === "history"}
        onCancel={() => setOpenModal(null)}
        footer={null}
        title="历史记录"
        width={360}
        mask={false}
      >
        <HistoryPanel />
      </Modal>

      {/* 用户档案 */}
      <Modal
        open={openModal === "profile"}
        onCancel={() => setOpenModal(null)}
        footer={null}
        title="用户档案"
        width={360}
        mask={false}
      >
        <UserProfileForm />
      </Modal>

      {/* 设置 */}
      <Modal
        open={openModal === "settings"}
        onCancel={() => setOpenModal(null)}
        footer={null}
        title="设置"
        width={360}
        mask={false}
      >
        <PromptEditor />
      </Modal>
    </div>
  );
}
