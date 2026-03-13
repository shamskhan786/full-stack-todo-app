import { NextRequest, NextResponse } from "next/server";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

/**
 * GET /api/chatkit/history
 * Retrieves conversation history for the authenticated user.
 * Query params: limit (default: 50)
 * Requires: Authorization header with Bearer token
 * Returns: { messages: Array<{ id, role, content, created_at, ... }> }
 */
export async function GET(request: NextRequest) {
  // 1. Get JWT from Authorization header
  const authHeader = request.headers.get("authorization");
  if (!authHeader?.startsWith("Bearer ")) {
    return NextResponse.json(
      { error: "Authentication required" },
      { status: 401 }
    );
  }

  // 2. Get limit from query params
  const limit = request.nextUrl.searchParams.get("limit") || "50";

  // 3. Call backend to retrieve messages
  try {
    const res = await fetch(
      `${API_URL}/api/conversations/messages?limit=${limit}`,
      {
        headers: { Authorization: authHeader },
      }
    );

    if (!res.ok) {
      const errorBody = await res.json().catch(() => ({}));
      return NextResponse.json(
        { error: errorBody.error || "Failed to load history" },
        { status: res.status }
      );
    }

    const body = await res.json();

    // Backend returns { success: true, data: [...] }
    // We return { messages: [...] } to match frontend expectation
    return NextResponse.json({ messages: body.data || [] });
  } catch (error) {
    console.error("History fetch failed:", error);
    return NextResponse.json(
      { error: "Failed to load history" },
      { status: 500 }
    );
  }
}
