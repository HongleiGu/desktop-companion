export type IterationType = "daily" | "weekly" | "monthly" | "yearly";
export type Todo = {
  id: string;
  title: string;
  completed: boolean;
  not_todo: boolean;
  created_at: string;
  ddl?: string;
  iteration?: IterationType;
  iteration_count: number;
};