import { authClient } from "./auth-client";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export class ApiError extends Error {
  code: string;
  details?: { field: string; message: string }[];

  constructor(
    message: string,
    code: string,
    details?: { field: string; message: string }[]
  ) {
    super(message);
    this.name = "ApiError";
    this.code = code;
    this.details = details;
  }
}

export interface Task {
  id: string;
  user_id: string;
  title: string;
  description: string | null;
  is_completed: boolean;
  completed_at: string | null;
  created_at: string;
  updated_at: string;
}

interface SuccessResponse<T> {
  success: true;
  data: T;
  message?: string;
}

interface ErrorResponse {
  success: false;
  error: string;
  code: string;
  details?: { field: string; message: string }[];
}

type ApiResponse<T> = SuccessResponse<T> | ErrorResponse;

async function getToken(): Promise<string | null> {
  const { data } = await authClient.token();
  return data?.token ?? null;
}

async function apiFetch<T>(
  path: string,
  options: RequestInit = {}
): Promise<T> {
  const token = await getToken();

  const res = await fetch(`${API_URL}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...options.headers,
    },
  });

  // Check for 401 (expired/invalid token) BEFORE parsing JSON
  if (res.status === 401) {
    if (typeof window !== "undefined") {
      window.location.href = "/signin";
    }
    throw new ApiError("Session expired", "UNAUTHORIZED");
  }

  const body: ApiResponse<T> = await res.json();

  if (!body.success) {
    const errBody = body as ErrorResponse;
    throw new ApiError(
      errBody.error || "Request failed",
      errBody.code || "UNKNOWN",
      errBody.details
    );
  }

  return (body as SuccessResponse<T>).data;
}

export async function listTasks(userId: string): Promise<Task[]> {
  return apiFetch<Task[]>(`/api/${userId}/tasks`);
}

export async function getTask(userId: string, taskId: string): Promise<Task> {
  return apiFetch<Task>(`/api/${userId}/tasks/${taskId}`);
}

export async function createTask(
  userId: string,
  data: { title: string; description?: string }
): Promise<Task> {
  return apiFetch<Task>(`/api/${userId}/tasks`, {
    method: "POST",
    body: JSON.stringify(data),
  });
}

export async function updateTask(
  userId: string,
  taskId: string,
  data: { title: string; description?: string }
): Promise<Task> {
  return apiFetch<Task>(`/api/${userId}/tasks/${taskId}`, {
    method: "PUT",
    body: JSON.stringify(data),
  });
}

export async function deleteTask(
  userId: string,
  taskId: string
): Promise<void> {
  const token = await getToken();

  const res = await fetch(`${API_URL}/api/${userId}/tasks/${taskId}`, {
    method: "DELETE",
    headers: {
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
  });

  // Check for 401 (expired/invalid token) BEFORE parsing JSON
  if (res.status === 401) {
    if (typeof window !== "undefined") {
      window.location.href = "/signin";
    }
    throw new ApiError("Session expired", "UNAUTHORIZED");
  }

  const body = await res.json();
  if (!body.success) {
    throw new ApiError(body.error || "Delete failed", body.code || "UNKNOWN", body.details);
  }
}

export async function completeTask(
  userId: string,
  taskId: string
): Promise<Task> {
  return apiFetch<Task>(`/api/${userId}/tasks/${taskId}/complete`, {
    method: "PATCH",
  });
}
