import { auth } from "@/lib/auth";
import { toNextJsHandler } from "better-auth/next-js";
import { NextRequest } from "next/server";

const handler = toNextJsHandler(auth);

export async function GET(req: NextRequest) {
  try {
    return await handler.GET(req);
  } catch (e) {
    console.error("AUTH GET ERROR FULL:", e);
    return new Response(JSON.stringify({ error: String(e) }), { status: 500 });
  }
}

export async function POST(req: NextRequest) {
  try {
    return await handler.POST(req);
  } catch (e) {
    console.error("AUTH POST ERROR FULL:", e);
    return new Response(JSON.stringify({ error: String(e) }), { status: 500 });
  }
}
