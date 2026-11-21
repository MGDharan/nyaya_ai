import { withSupabase, createSupabaseContext } from "@supabase/server";

/**
 * Example Server API Handler using @supabase/server
 * Handles inbound request verification (JWT, Secret, or Publishable)
 */

// 1. High-level wrapper with user authentication
export const handleUserRequest = withSupabase(
  { auth: "user" },
  async (req, ctx) => {
    // Injected context contains pre-authenticated Supabase client and user claims
    const { data: profile, error } = await ctx.supabase
      .from("profiles")
      .select("*")
      .single();

    if (error) {
      return Response.json({ error: error.message }, { status: 400 });
    }

    return Response.json({
      authMode: ctx.authMode,
      claims: ctx.claims,
      profile,
    });
  }
);

// 2. Secret/Admin handler for backend services and webhooks
export const handleAdminRequest = withSupabase(
  { auth: "secret" },
  async (req, ctx) => {
    // Service role / admin client with bypass RLS
    const { data: users, error } = await ctx.supabase.auth.admin.listUsers();
    if (error) {
      return Response.json({ error: error.message }, { status: 500 });
    }
    return Response.json({ users });
  }
);

// 3. Composable context resolution for custom routing
export async function authenticateApiRequest(req: Request) {
  const { data: ctx, error } = await createSupabaseContext(req, {
    auth: ["user", "secret"],
  });

  if (error) {
    return {
      success: false,
      response: Response.json(
        { error: error.message, code: error.code },
        { status: error.status }
      ),
    };
  }

  return { success: true, ctx };
}

