"use client";
import { useStore } from "../store/store";
import { List, Button, Space, Typography, Empty } from "antd";
import { DeleteOutlined } from "@ant-design/icons";
import dayjs from "dayjs";

const { Text } = Typography;

export default function HistoryPanel() {
  const chatHistory = useStore((state) => state.chatHistory);
  const deleteChat = useStore((state) => state.deleteChat);

  return (
    <List
      size="small"
      locale={{ emptyText: <Empty description="暂无记录" /> }}
      dataSource={chatHistory}
      renderItem={(chat) => (
        <List.Item
          actions={[
            <Button
              key="delete"
              type="text"
              danger
              icon={<DeleteOutlined />}
              onClick={() => deleteChat(chat.id)}
            />,
          ]}
        >
          <Space orientation="vertical" size={0}>
            <Text type="secondary" style={{ fontSize: 11 }}>
              {dayjs(chat.timestamp).format("HH:mm:ss")}
            </Text>
            <Text>{chat.content}</Text>
          </Space>
        </List.Item>
      )}
    />
  );
}
