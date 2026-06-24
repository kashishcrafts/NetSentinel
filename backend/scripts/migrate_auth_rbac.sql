-- Enterprise Auth, RBAC & Audit migration
-- Run against existing NetSentinel PostgreSQL database

ALTER TABLE users ADD COLUMN IF NOT EXISTS refresh_token_jti VARCHAR(255);
ALTER TABLE users ADD COLUMN IF NOT EXISTS refresh_token_expires_at TIMESTAMP;

ALTER TABLE audit_logs ALTER COLUMN user_id DROP NOT NULL;
ALTER TABLE audit_logs ADD COLUMN IF NOT EXISTS username VARCHAR(255);
ALTER TABLE audit_logs ADD COLUMN IF NOT EXISTS role VARCHAR(50);
ALTER TABLE audit_logs ADD COLUMN IF NOT EXISTS status VARCHAR(20) DEFAULT 'success';
ALTER TABLE audit_logs ALTER COLUMN entity_type DROP NOT NULL;
ALTER TABLE audit_logs ALTER COLUMN entity_id DROP NOT NULL;

CREATE INDEX IF NOT EXISTS idx_audit_status ON audit_logs(status);

CREATE TABLE IF NOT EXISTS system_settings (
    id SERIAL PRIMARY KEY,
    key VARCHAR(100) UNIQUE NOT NULL,
    value JSON NOT NULL,
    description VARCHAR(500),
    updated_by INTEGER REFERENCES users(id),
    updated_at TIMESTAMP DEFAULT NOW()
);
