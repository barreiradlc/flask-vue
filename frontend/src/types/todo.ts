export interface Todo {
  id: number;
  description: string;
  completed: boolean;
  createdAt: Date;
}

export interface NewTodo {
  description: string;
}