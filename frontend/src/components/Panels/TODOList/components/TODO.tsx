"use client";

import { useEffect, useState } from "react";
import { List, Checkbox, Button, Input, Space, Typography, Select, DatePicker } from "antd";
import { DeleteOutlined, PlusOutlined } from "@ant-design/icons";
import { useTodoStore } from "@/store/todoStore";
import dayjs from "dayjs";
import { IterationType } from "@/types/todo";

const { Text } = Typography;

export default function TodoList() {
  const { todos, fetchTodos, addTodo, toggleTodo, incrementIteration, deleteTodo } =
    useTodoStore();
  const [title, setTitle] = useState("");
  const [ddl, setDdl] = useState<dayjs.Dayjs | null>(null);
  const [iteration, setIteration] = useState<string | undefined>(undefined);
  const [notTodo, setNotTodo] = useState(false);

  useEffect(() => {
    fetchTodos();
  }, []);

  return (
    <List
      size="small"
      bordered
      header={<Text strong>ToDo / Habit Tracker</Text>}
      style={{ width: "100%" }}
    >
      {/* Add new todo/habit */}
      <List.Item>
        <Space style={{ width: "100%" }} wrap>
          <Input
            size="small"
            placeholder="Task or habit..."
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            onPressEnter={() => {
              if (!title.trim()) return;
              addTodo({
                title,
                ddl: ddl?.toISOString(),
                iteration: iteration as IterationType,
                not_todo: notTodo,
              });
              setTitle(""); setDdl(null); setIteration(undefined); setNotTodo(false);
            }}
          />
          <DatePicker
            size="small"
            value={ddl}
            onChange={(date) => setDdl(date)}
            placeholder="Deadline"
          />
          <Select
            size="small"
            style={{ width: 120 }}
            placeholder="Iteration"
            value={iteration}
            onChange={(val) => setIteration(val)}
            options={[
              { label: "Daily", value: "daily" },
              { label: "Weekly", value: "weekly" },
              { label: "Monthly", value: "monthly" },
              { label: "Yearly", value: "yearly" },
            ]}
          />
          <Checkbox checked={notTodo} onChange={(e) => setNotTodo(e.target.checked)}>
            Not ToDo
          </Checkbox>
          <Button
            size="small"
            type="primary"
            onClick={() => {
              if (!title.trim()) return;
              addTodo({
                title,
                ddl: ddl?.toISOString(),
                iteration: iteration as IterationType,
                not_todo: notTodo,
              });
              setTitle(""); setDdl(null); setIteration(undefined); setNotTodo(false);
            }}
          >
            Add
          </Button>
        </Space>
      </List.Item>

      {/* List existing todos/habits */}
      {todos.map((todo) => (
        <List.Item
          key={todo.id}
          actions={[
            <Button
              key="increment"
              size="small"
              icon={<PlusOutlined />}
              onClick={() => incrementIteration(todo.id)}
            >
              {todo.iteration_count}
            </Button>,
            <Button
              key="delete"
              size="small"
              danger
              icon={<DeleteOutlined />}
              onClick={() => deleteTodo(todo.id)}
            />,
          ]}
        >
          <Space orientation="vertical">
            <Checkbox
              checked={todo.completed}
              onChange={(e) => toggleTodo(todo.id, e.target.checked)}
            >
              <Text delete={todo.completed} type={todo.not_todo ? "secondary" : undefined}>
                {todo.title} {todo.ddl ? `(Due: ${dayjs(todo.ddl).format("YYYY-MM-DD")})` : ""}
              </Text>
            </Checkbox>
            {todo.iteration && <Text type="secondary">Iteration: {todo.iteration}</Text>}
          </Space>
        </List.Item>
      ))}
    </List>
  );
}
