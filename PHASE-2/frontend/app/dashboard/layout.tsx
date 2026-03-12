"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useSession, signOut } from "@/lib/auth-client";

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const router = useRouter();
  const { data: session, isPending } = useSession();

  useEffect(() => {
    if (!isPending && !session) {
      router.replace("/signin");
    }
  }, [session, isPending, router]);

  if (isPending) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-pulse text-gray-400">Loading...</div>
      </div>
    );
  }

  if (!session) return null;

  return (
    <div className="min-h-screen">
      <header className="bg-white border-b border-gray-200 px-4 sm:px-6 py-4">
        <div className="max-w-4xl mx-auto flex items-center justify-between">
          <h1 className="text-lg sm:text-xl font-bold">Todo App</h1>
          <nav aria-label="User actions" className="flex items-center gap-4">
            <span className="text-sm text-gray-600 hidden sm:inline">
              {session.user.email}
            </span>
            <button
              onClick={() => signOut().then(() => router.push("/signin"))}
              aria-label="Sign out"
              className="text-sm text-red-600 hover:text-red-700 font-medium min-h-[44px] px-2 focus:outline-none focus:ring-2 focus:ring-red-500 rounded"
            >
              Sign Out
            </button>
          </nav>
        </div>
      </header>
      <main className="max-w-4xl mx-auto px-4 sm:px-6 py-6">{children}</main>
    </div>
  );
}
