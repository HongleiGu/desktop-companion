"use client";
import { useState } from "react";
import { Input, Button, Space } from "antd";
import { useStore } from "../store/store";
// import { CharacterProfile } from "../types";

export default function CharacterProfileForm() {
  const characterProfile = useStore((s) => s.characterProfile);
  const setCharacterProfile = useStore((s) => s.setCharacterProfile);
  const [form, setForm] = useState(characterProfile);

  const fields = [
    { key: "ocName", label: "昵称" },
    { key: "birthday", label: "生日" },
    { key: "relation", label: "关系设定" },
    { key: "description", label: "基本信息及设定" },
    { key: "speakingStyle", label: "说话风格"},
    { key: "personality", label: "性格"}
  ] as const;

  return (
    <Space orientation="vertical" size="small" style={{ width: "100%" }}>
      {fields.map(({ key, label }) => (
        <Input
          key={key}
          placeholder={label}
          value={form[key]}
          onChange={(e) =>
            setForm({
              ...form,
              [key]: e.target.value
            })
          }
        />
      ))}

      <Button
        type="primary"
        size="small"
        onClick={() => setCharacterProfile(form)}
      >
        保存档案
      </Button>
    </Space>
  );
}
