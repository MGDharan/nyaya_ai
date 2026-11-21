# NyayaAI – Production Database Schema Specification

## 1. Relational & Vector Storage Architecture

NyayaAI uses an enterprise relational schema designed with SQLAlchemy and PostgreSQL with the `pgvector` extension. For local zero-dependency testing and environments without Docker or PostgreSQL services, an embedded SQLite persistence layer (`backend/data/vectors.db`) is seamlessly supported.

The complete SQLAlchemy schema model is implemented in `backend/app/services/db_models.py`.

---

## 2. Table Specifications & Relationships

### A. `users`
Stores citizen profiles, preferred language, state jurisdiction, and role.
- `id` (UUID, Primary Key)
- `email` (VARCHAR(255), Unique, Indexed)
- `hashed_password` (VARCHAR(255))
- `full_name` (VARCHAR(255))
- `preferred_language` (VARCHAR(32), Default: "English")
- `state_jurisdiction` (VARCHAR(128), Default: "India")
- `role` (VARCHAR(32), Default: "citizen")
- `created_at` (TIMESTAMP WITH TIME ZONE)

### B. `statute_acts`
Authoritative register of Central and State Acts, Gazette references, and legislative status.
- `id` (UUID, Primary Key)
- `act_title` (VARCHAR(512), Indexed)
- `act_number` (VARCHAR(128))
- `enactment_year` (INTEGER, Indexed)
- `jurisdiction` (VARCHAR(128), Indexed)
- `commencement_date` (DATE)
- `is_in_force` (BOOLEAN, Default: TRUE)
- `repealed_by_act_id` (UUID, Foreign Key -> `statute_acts.id`, Nullable)
- `repeal_date` (DATE, Nullable)
- `official_source_url` (TEXT)
- `sha256_hash` (VARCHAR(64))

### C. `statute_sections`
Granular section-level provisions preserving hierarchical legal metadata.
- `id` (UUID, Primary Key)
- `act_id` (UUID, Foreign Key -> `statute_acts.id`, On Delete CASCADE)
- `chapter_number` (VARCHAR(64))
- `chapter_title` (VARCHAR(255))
- `section_number` (VARCHAR(32), Indexed)
- `section_title` (VARCHAR(512))
- `full_text` (TEXT)
- `subsections_json` (JSONB)
- `provisos_json` (JSONB)
- `explanations_json` (JSONB)
- `is_repealed` (BOOLEAN, Default: FALSE)
- `embedding` (VECTOR(768)) -- Dense 768-d Gemini representation

### D. `judicial_judgments`
Authoritative judgments from the Supreme Court of India, High Courts, and NCDRC.
- `id` (UUID, Primary Key)
- `case_title` (VARCHAR(512), Indexed)
- `citation` (VARCHAR(255), Indexed)
- `court_name` (VARCHAR(255))
- `judgment_date` (DATE)
- `bench_coram` (VARCHAR(512))
- `ratio_decidendi` (TEXT)
- `overruled_by_id` (UUID, Foreign Key -> `judicial_judgments.id`, Nullable)
- `is_binding_precedent` (BOOLEAN, Default: TRUE)
- `official_pdf_url` (TEXT)

### E. `query_conversations` & `query_messages`
Full conversation history, user prompts, 10-agent logs, and structured outputs.
- `id` (UUID, Primary Key)
- `user_id` (UUID, Foreign Key -> `users.id`, Nullable)
- `title` (VARCHAR(255))
- `incident_date` (DATE, Nullable)
- `jurisdiction` (VARCHAR(128))
- `created_at` (TIMESTAMP WITH TIME ZONE)

### F. `citation_verification_audits`
Audit trail recording the exact verification result for every generated legal claim.
- `id` (UUID, Primary Key)
- `message_id` (UUID, Foreign Key -> `query_messages.id`)
- `act_name` (VARCHAR(512))
- `section_number` (VARCHAR(32))
- `exact_provision_text` (TEXT)
- `official_source` (TEXT)
- `effective_date` (DATE)
- `current_status` (VARCHAR(64))
- `jurisdiction` (VARCHAR(128))
- `confidence_level` (VARCHAR(32)) -- `verified`, `caution`, `unverified`, `refuted`
- `audit_verdict` (VARCHAR(32))
- `verified_at` (TIMESTAMP WITH TIME ZONE)

---

## 3. PostgreSQL DDL Script

```sql
-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS vector;

-- Statute Acts
CREATE TABLE IF NOT EXISTS statute_acts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    act_title VARCHAR(512) NOT NULL,
    act_number VARCHAR(128),
    enactment_year INTEGER NOT NULL,
    jurisdiction VARCHAR(128) NOT NULL DEFAULT 'India',
    commencement_date DATE,
    is_in_force BOOLEAN NOT NULL DEFAULT TRUE,
    repealed_by_act_id UUID REFERENCES statute_acts(id),
    repeal_date DATE,
    official_source_url TEXT,
    sha256_hash VARCHAR(64),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_acts_title ON statute_acts(act_title);
CREATE INDEX idx_acts_year ON statute_acts(enactment_year);
CREATE INDEX idx_acts_jurisdiction ON statute_acts(jurisdiction);

-- Statute Sections with 768-dimension Vector Index
CREATE TABLE IF NOT EXISTS statute_sections (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    act_id UUID NOT NULL REFERENCES statute_acts(id) ON DELETE CASCADE,
    chapter_number VARCHAR(64),
    chapter_title VARCHAR(255),
    section_number VARCHAR(32) NOT NULL,
    section_title VARCHAR(512),
    full_text TEXT NOT NULL,
    subsections_json JSONB,
    provisos_json JSONB,
    explanations_json JSONB,
    is_repealed BOOLEAN NOT NULL DEFAULT FALSE,
    embedding vector(768),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_sections_act_num ON statute_sections(act_id, section_number);
-- HNSW Vector Cosine Index for sub-millisecond retrieval
CREATE INDEX idx_sections_hnsw_embedding ON statute_sections 
USING hnsw (embedding vector_cosine_ops) WITH (m = 16, ef_construction = 64);
```

