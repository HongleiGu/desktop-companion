"use client";
import { useState } from "react";
import { Input, Button, Space } from "antd";
import { useStore } from "../store/store";

export default function UserProfileForm() {
  const userProfile = useStore((s) => s.userProfile);
  const setUserProfile = useStore((s) => s.setUserProfile);
  const [form, setForm] = useState(userProfile);

  const fields = [
    { key: "nickname", label: "昵称" },
    { key: "birthday", label: "生日" },
    { key: "ocName", label: "对OC的称呼" },
    { key: "relation", label: "关系设定" }
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
        onClick={() => setUserProfile(form)}
      >
        保存档案
      </Button>
    </Space>
  );
}
