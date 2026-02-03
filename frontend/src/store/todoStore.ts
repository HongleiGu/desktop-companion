import { create } from "zustand";
import { supabase } from "@/lib/supabase";
import { Todo } from "@/types/todo";

type TodoState = {
  todos: Todo[];
  fetchTodos: () => Promise<void>;
  addTodo: (todo: Partial<Todo>) => Promise<void>;
  toggleTodo: (id: string, completed: boolean) => Promise<void>;
  incrementIteration: (id: string) => Promise<void>;
  deleteTodo: (id: string) => Promise<void>;
};

export const useTodoStore = create<TodoState>((set, get) => ({
  todos: [],

  fetchTodos: async () => {
    const { data } = await supabase
      .from("todos")
      .select("*")
      .order("created_at", { ascending: false });
    set({ todos: data || [] });
  },

  addTodo: async (todo) => {
    await supabase.from("todos").insert([todo]);
    get().fetchTodos();
  },

  toggleTodo: async (id, completed) => {
    await supabase.from("todos").update({ completed }).eq("id", id);
    get().fetchTodos();
  },

  incrementIteration: async (id) => {
    const todo = get().todos.find((t) => t.id === id);
    if (!todo) return;
    await supabase
      .from("todos")
      .update({ iteration_count: todo.iteration_count + 1 })
      .eq("id", id);
    get().fetchTodos();
  },

  deleteTodo: async (id) => {
    await supabase.from("todos").delete().eq("id", id);
    get().fetchTodos();
  },
}));