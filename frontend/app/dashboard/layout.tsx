"use client";

import { useState, useEffect } from "react";
import { useRouter, usePathname } from "next/navigation";
import { useSession, signOut } from "@/lib/auth-client";
import Sidebar from "@/components/ui/sidebar";
import FloatingChat from "@/components/ui/floating-chat";

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const router = useRouter();
  const pathname = usePathname();
  const { data: session, isPending } = useSession();
  const [sidebarOpen, setSidebarOpen] = useState(false);

  useEffect(() => {
    if (!isPending && !session) {
      router.replace("/signin");
    }
  }, [session, isPending, router]);

  if (isPending) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-slate-900">
        <div className="flex flex-col items-center gap-3">
          <div className="w-10 h-10 border-2 border-blue-600 border-t-transparent rounded-full animate-spin" />
          <p className="text-gray-400 dark:text-slate-500 text-sm">Loading...</p>
        </div>
      </div>
    );
  }

  if (!session) return null;

  const handleSignOut = () => {
    signOut().then(() => router.push("/signin"));
  };

  const showFloatingChat = pathname !== "/dashboard/chat";

  return (
    <div className="h-screen flex overflow-hidden bg-gray-50 dark:bg-slate-900 transition-colors duration-200">
      <Sidebar
        isOpen={sidebarOpen}
        onClose={() => setSidebarOpen(false)}
        userEmail={session.user.email}
        onSignOut={handleSignOut}
      />

      {/* Main content area */}
      <div className="flex-1 lg:pl-64 flex flex-col min-h-0">
        {/* Mobile top bar */}
        <header className="lg:hidden bg-white dark:bg-slate-800 border-b border-gray-200 dark:border-slate-700 flex items-center gap-3 px-4 h-14 flex-shrink-0 transition-colors">
          <button
            onClick={() => setSidebarOpen(true)}
            className="p-2 -ml-2 rounded-lg text-gray-500 dark:text-slate-400 hover:bg-gray-100 dark:hover:bg-slate-700 transition-colors"
            aria-label="Open sidebar"
          >
            <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>
          <h1 className="text-lg font-bold text-gray-900 dark:text-white">Todo AI</h1>
        </header>

        <main className="flex-1 overflow-hidden">{children}</main>
      </div>

      {showFloatingChat && <FloatingChat />}
    </div>
  );
}
