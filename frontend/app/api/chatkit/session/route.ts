import { NextRequest, NextResponse } from "next/server";
import OpenAI from "openai";

/**
 * POST /api/chatkit/session
 * Creates an OpenAI ChatKit session for the authenticated user.
 * Requires: Authorization header with Bearer token
 * Returns: { client_secret, session_id }
 *
 * The ChatKit workflow must be pre-configured in the OpenAI dashboard with:
 * - Agent model (e.g., gpt-4o-mini)
 * - MCP tools pointing to our backend /mcp endpoint
 * - System instructions for task management
 * Set CHATKIT_WORKFLOW_ID in environment variables.
 */
export async function POST(request: NextRequest) {
  // 1. Get JWT from Authorization header
  const authHeader = request.headers.get("authorization");
  if (!authHeader?.startsWith("Bearer ")) {
    return NextResponse.json(
      { error: "Authentication required" },
      { status: 401 }
    );
  }
  const token = authHeader.slice(7);

  // 2. Decode JWT payload to get user_id (sub claim)
  try {
    const parts = token.split(".");
    if (parts.length !== 3) {
      throw new Error("Invalid JWT format");
    }

    const payload = JSON.parse(
      Buffer.from(parts[1], "base64url").toString()
    );
    const userId = payload.sub;

    if (!userId) {
      throw new Error("No sub claim found in JWT");
    }

    const workflowId = process.env.CHATKIT_WORKFLOW_ID;
    if (!workflowId) {
      throw new Error("CHATKIT_WORKFLOW_ID environment variable is required");
    }

    // 3. Create OpenAI client and ChatKit session with workflow and user context
    const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

    const session = await openai.beta.chatkit.sessions.create({
      user: userId,
      workflow: {
        id: workflowId,
        state_variables: {
          user_id: userId,
        },
      },
    });

    // 4. Persist session in our database (non-blocking)
    let dbSessionId: string | null = null;
    try {
      const persistRes = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/api/conversations/sessions`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({ openai_thread_id: session.id }),
        }
      );

      if (persistRes.ok) {
        const persistBody = await persistRes.json();
        dbSessionId = persistBody.data?.id || null;
      } else {
        console.warn("Failed to persist session:", await persistRes.text());
      }
    } catch (persistError) {
      console.warn("Failed to persist session:", persistError);
    }

    return NextResponse.json({
      client_secret: session.client_secret,
      session_id: dbSessionId,
    });
  } catch (error) {
    console.error("Session creation failed:", error);
    return NextResponse.json(
      {
        error: "Failed to create session",
        details: error instanceof Error ? error.message : "Unknown error",
      },
      { status: 500 }
    );
  }
}
