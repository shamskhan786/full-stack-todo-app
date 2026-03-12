"use client";

import { useState, useEffect } from "react";
import type { Task } from "@/lib/api";

interface TaskItemProps {
  task: Task;
  onComplete: (taskId: string) => Promise<void>;
  onDelete: (taskId: string) => Promise<void>;
  onEdit: (task: Task) => void;
}

export default function TaskItem({
  task,
  onComplete,
  onDelete,
  onEdit,
}: TaskItemProps) {
  const [loading, setLoading] = useState(false);
  const [confirmDelete, setConfirmDelete] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!confirmDelete) return;
    const timer = setTimeout(() => setConfirmDelete(false), 5000);
    return () => clearTimeout(timer);
  }, [confirmDelete]);

  async function handleComplete() {
    setError("");
    setLoading(true);
    try {
      await onComplete(task.id);
    } catch {
      setError("Failed to complete task");
    } finally {
      setLoading(false);
    }
  }

  async function handleDelete() {
    setError("");
    setLoading(true);
    try {
      await onDelete(task.id);
    } catch {
      setError("Failed to delete task");
    } finally {
      setLoading(false);
      setConfirmDelete(false);
    }
  }

  return (
    <article
      className={`bg-white rounded-lg border p-4 flex flex-col sm:flex-row sm:items-center gap-3 ${
        task.is_completed ? "border-green-200 bg-green-50/50" : "border-gray-200"
      }`}
    >
      <div className="flex-1 min-w-0">
        <h3
          className={`font-medium truncate ${
            task.is_completed ? "line-through text-gray-400" : ""
          }`}
        >
          {task.title}
        </h3>
        {task.description && (
          <p className="text-sm text-gray-500 mt-1 line-clamp-2">
            {task.description}
          </p>
        )}
        <p className="text-xs text-gray-400 mt-1">
          {new Date(task.created_at).toLocaleDateString()}
          {task.is_completed && task.completed_at && (
            <span className="ml-2 text-green-600">
              ✓ Completed {new Date(task.completed_at).toLocaleDateString()}
            </span>
          )}
        </p>
      </div>

      <div className="flex flex-col gap-2">
        <div className="flex items-center gap-2 shrink-0">
          {!task.is_completed && (
            <>
              <button
                onClick={() => onEdit(task)}
                disabled={loading}
                aria-label={`Edit task: ${task.title}`}
                className="text-sm px-3 py-2 min-h-[44px] rounded-md border border-gray-300 hover:bg-gray-50 disabled:opacity-50 transition-colors"
              >
                Edit
              </button>
              <button
                onClick={handleComplete}
                disabled={loading}
                aria-label={`Mark complete: ${task.title}`}
                className="text-sm px-3 py-2 min-h-[44px] rounded-md bg-green-600 text-white hover:bg-green-700 disabled:opacity-50 transition-colors"
              >
                Complete
              </button>
            </>
          )}
          {!confirmDelete ? (
            <button
              onClick={() => setConfirmDelete(true)}
              disabled={loading}
              aria-label={`Delete task: ${task.title}`}
              className="text-sm px-3 py-2 min-h-[44px] rounded-md border border-red-300 text-red-600 hover:bg-red-50 disabled:opacity-50 transition-colors"
            >
              Delete
            </button>
          ) : (
            <>
              <button
                onClick={() => setConfirmDelete(false)}
                disabled={loading}
                className="text-sm px-3 py-2 min-h-[44px] rounded-md border border-gray-300 hover:bg-gray-50 disabled:opacity-50 transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={handleDelete}
                disabled={loading}
                aria-label={`Confirm delete: ${task.title}`}
                className="text-sm px-3 py-2 min-h-[44px] rounded-md bg-red-600 text-white hover:bg-red-700 disabled:opacity-50 transition-colors"
              >
                Confirm
              </button>
            </>
          )}
        </div>
        {error && (
          <p role="alert" className="text-xs text-red-600">
            {error}
          </p>
        )}
      </div>
    </article>
  );
}
