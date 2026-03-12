"use client";

import { useEffect } from "react";

interface ToastProps {
  message: string;
  type: "success" | "error";
  onClose: () => void;
}

export default function Toast({ message, type, onClose }: ToastProps) {
  useEffect(() => {
    const timer = setTimeout(onClose, 3000);
    return () => clearTimeout(timer);
  }, [onClose]);

  return (
    <div
      aria-live="polite"
      role="status"
      className={`fixed bottom-4 right-4 z-50 flex items-center gap-3 px-4 py-3 rounded-lg shadow-lg text-white text-sm ${
        type === "success" ? "bg-green-600" : "bg-red-600"
      }`}
    >
      <span>{message}</span>
      <button
        onClick={onClose}
        aria-label="Dismiss notification"
        className="min-h-[44px] min-w-[44px] flex items-center justify-center rounded hover:opacity-80 transition-opacity"
      >
        ✕
      </button>
    </div>
  );
}
