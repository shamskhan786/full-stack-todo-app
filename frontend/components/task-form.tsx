"use client";

import { useState } from "react";
import type { Task } from "@/lib/api";

interface TaskFormProps {
  initialTask?: Task | null;
  onSubmit: (data: { title: string; description?: string }) => Promise<void>;
  onCancel: () => void;
}

export default function TaskForm({
  initialTask,
  onSubmit,
  onCancel,
}: TaskFormProps) {
  const [title, setTitle] = useState(initialTask?.title || "");
  const [description, setDescription] = useState(
    initialTask?.description || ""
  );
  const [error, setError] = useState("");
  const [titleError, setTitleError] = useState("");
  const [loading, setLoading] = useState(false);

  function validateTitle() {
    const trimmed = title.trim();
    if (!trimmed) {
      setTitleError("Title is required");
      return false;
    }
    if (trimmed.length > 500) {
      setTitleError("Title must be 500 characters or less");
      return false;
    }
    setTitleError("");
    return true;
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");

    if (!validateTitle()) return;

    const trimmedTitle = title.trim();

    setLoading(true);
    try {
      await onSubmit({
        title: trimmedTitle,
        description: description.trim() || undefined,
      });
    } catch {
      setError("Failed to save task");
    } finally {
      setLoading(false);
    }
  }

  const charCountColor =
    title.length > 500 ? "text-red-600" : title.length >= 450 ? "text-amber-600" : "text-gray-400";

  return (
    <form
      onSubmit={handleSubmit}
      className="bg-white rounded-lg border border-gray-200 p-4 flex flex-col gap-4"
    >
      <h2 className="text-lg font-medium">
        {initialTask ? "Edit Task" : "New Task"}
      </h2>

      {error && (
        <div role="alert" aria-live="assertive" className="bg-red-50 border border-red-200 text-red-700 px-3 py-2 rounded text-sm">
          {error}
        </div>
      )}

      <div className="flex flex-col gap-1">
        <label htmlFor="task-title" className="text-sm font-medium text-gray-700">
          Title
        </label>
        <input
          id="task-title"
          type="text"
          placeholder="Task title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          onBlur={validateTitle}
          required
          maxLength={500}
          aria-invalid={!!titleError}
          aria-describedby="title-char-count title-error"
          className="w-full border border-gray-300 rounded-lg px-4 py-2 min-h-[44px] focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <div className="flex justify-between items-center">
          {titleError ? (
            <p id="title-error" role="alert" className="text-sm text-red-600">
              {titleError}
            </p>
          ) : (
            <span />
          )}
          <span id="title-char-count" className={`text-xs ${charCountColor}`}>
            {title.length}/500
          </span>
        </div>
      </div>

      <div className="flex flex-col gap-1">
        <label htmlFor="task-desc" className="text-sm font-medium text-gray-700">
          Description (optional)
        </label>
        <textarea
          id="task-desc"
          placeholder="Description (optional)"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          rows={3}
          className="w-full border border-gray-300 rounded-lg px-4 py-2 min-h-[44px] focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
        />
      </div>

      <div className="flex gap-2 justify-end">
        <button
          type="button"
          onClick={onCancel}
          className="px-4 py-2 min-h-[44px] text-sm rounded-md border border-gray-300 hover:bg-gray-50 transition-colors"
        >
          Cancel
        </button>
        <button
          type="submit"
          disabled={loading}
          className="px-4 py-2 min-h-[44px] text-sm rounded-md bg-blue-600 text-white hover:bg-blue-700 disabled:opacity-50 transition-colors"
        >
          {loading ? "Saving..." : initialTask ? "Update" : "Create"}
        </button>
      </div>
    </form>
  );
}
