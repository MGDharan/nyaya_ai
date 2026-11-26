-- NyayaAI Enterprise PostgreSQL / Supabase Migration (with RLS)
-- Safe to run on Supabase SQL Editor; creates tables if they do not exist.

CREATE TABLE IF NOT EXISTS public.user_profiles (
    user_id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    email TEXT NOT NULL UNIQUE,
    full_name TEXT NOT NULL DEFAULT 'User',
    role TEXT NOT NULL DEFAULT 'citizen' CHECK (role IN ('citizen', 'advocate', 'admin')),
    bar_council_no TEXT,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS public.user_sessions (
    session_id TEXT PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES public.user_profiles(user_id) ON DELETE CASCADE,
    login_timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    logout_timestamp TIMESTAMPTZ,
    last_active_timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    session_duration_sec DOUBLE PRECISION DEFAULT 0.0,
    device_info TEXT,
    browser_info TEXT,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    expires_at TIMESTAMPTZ NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS public.user_chat_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES public.user_profiles(user_id) ON DELETE CASCADE,
    request_id TEXT NOT NULL,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    legal_domain TEXT,
    jurisdiction TEXT DEFAULT 'India',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Enable Row Level Security (RLS)
ALTER TABLE public.user_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.user_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.user_chat_history ENABLE ROW LEVEL SECURITY;

-- Policies: Users can only read/manage their own profile, sessions, and chat history
CREATE POLICY "Users read own profile" ON public.user_profiles
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users update own profile" ON public.user_profiles
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users read own sessions" ON public.user_sessions
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users read own chat history" ON public.user_chat_history
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users delete own chat history" ON public.user_chat_history
    FOR DELETE USING (auth.uid() = user_id);

