"use client";

import { useState, useEffect, useCallback } from "react";
import { useSession } from "@/lib/auth-client";
import {
  listTasks,
  createTask,
  updateTask,
  deleteTask,
  completeTask,
  type Task,
} from "@/lib/api";
import TaskItem from "./task-item";
import TaskForm from "./task-form";
import Toast from "./toast";

export default function TaskList() {
  const { data: session } = useSession();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [showForm, setShowForm] = useState(false);
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [toast, setToast] = useState<{ message: string; type: "success" | "error" } | null>(null);

  const userId = session?.user?.id;

  const fetchTasks = useCallback(async () => {
    if (!userId) return;
    try {
      setError("");
      const data = await listTasks(userId);
      setTasks(data);
    } catch {
      setError("Failed to load tasks");
    } finally {
      setLoading(false);
    }
  }, [userId]);

  useEffect(() => {
    fetchTasks();
  }, [fetchTasks]);

  async function handleCreate(data: {
    title: string;
    description?: string;
  }) {
    if (!userId) return;
    const newTask = await createTask(userId, data);
    setTasks((prev) => [...prev, newTask]);
    setShowForm(false);
    setToast({ message: "Task created successfully", type: "success" });
  }

  async function handleUpdate(data: {
    title: string;
    description?: string;
  }) {
    if (!userId || !editingTask) return;
    const updated = await updateTask(userId, editingTask.id, data);
    setTasks((prev) =>
      prev.map((t) => (t.id === updated.id ? updated : t))
    );
    setEditingTask(null);
    setToast({ message: "Task updated successfully", type: "success" });
  }

  async function handleComplete(taskId: string) {
    if (!userId) return;
    try {
      const completed = await completeTask(userId, taskId);
      setTasks((prev) =>
        prev.map((t) => (t.id === completed.id ? completed : t))
      );
      setToast({ message: "Task completed", type: "success" });
    } catch {
      setToast({ message: "Failed to complete task", type: "error" });
      throw new Error("Failed to complete task");
    }
  }

  async function handleDelete(taskId: string) {
    if (!userId) return;
    try {
      await deleteTask(userId, taskId);
      setTasks((prev) => prev.filter((t) => t.id !== taskId));
      setToast({ message: "Task deleted", type: "success" });
    } catch {
      setToast({ message: "Failed to delete task", type: "error" });
      throw new Error("Failed to delete task");
    }
  }

  if (loading) {
    return (
      <div role="status" aria-live="polite" className="text-center py-12 text-gray-400">Loading tasks...</div>
    );
  }

  if (error) {
    return (
      <div role="alert" aria-live="assertive" className="text-center py-12">
        <p className="text-red-500 mb-4">{error}</p>
        <button
          onClick={fetchTasks}
          className="text-blue-600 hover:underline text-sm min-h-[44px]"
        >
          Try again
        </button>
      </div>
    );
  }

  const incompleteTasks = tasks.filter((t) => !t.is_completed);
  const completedTasks = tasks.filter((t) => t.is_completed);

  return (
    <section aria-label="Task list" className="space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-lg font-semibold">
          Tasks{" "}
          <span className="text-sm font-normal text-gray-500">
            ({incompleteTasks.length} active)
          </span>
        </h2>
        {!showForm && !editingTask && (
          <button
            onClick={() => setShowForm(true)}
            className="px-4 py-2 min-h-[44px] text-sm rounded-md bg-blue-600 text-white hover:bg-blue-700 transition-colors"
          >
            + New Task
          </button>
        )}
      </div>

      {showForm && (
        <TaskForm
          onSubmit={handleCreate}
          onCancel={() => setShowForm(false)}
        />
      )}

      {editingTask && (
        <TaskForm
          initialTask={editingTask}
          onSubmit={handleUpdate}
          onCancel={() => setEditingTask(null)}
        />
      )}

      {tasks.length === 0 && !showForm ? (
        <div className="text-center py-12 text-gray-400">
          <p className="text-lg mb-2">No tasks yet</p>
          <p className="text-sm">Create your first task to get started</p>
        </div>
      ) : (
        <div className="space-y-3">
          {incompleteTasks.map((task) => (
            <TaskItem
              key={task.id}
              task={task}
              onComplete={handleComplete}
              onDelete={handleDelete}
              onEdit={setEditingTask}
            />
          ))}

          {completedTasks.length > 0 && (
            <>
              <h3 className="text-sm font-medium text-gray-500 pt-4">
                Completed ({completedTasks.length})
              </h3>
              {completedTasks.map((task) => (
                <TaskItem
                  key={task.id}
                  task={task}
                  onComplete={handleComplete}
                  onDelete={handleDelete}
                  onEdit={setEditingTask}
                />
              ))}
            </>
          )}
        </div>
      )}

      {toast && (
        <Toast
          message={toast.message}
          type={toast.type}
          onClose={() => setToast(null)}
        />
      )}
    </section>
  );
}
