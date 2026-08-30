CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE TABLE IF NOT EXISTS social_accounts (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(), tenant_id varchar(128) NOT NULL, platform varchar(32) NOT NULL,
  external_account_id varchar(160) NOT NULL, display_name varchar(200), runtime_account_id varchar(160), active boolean NOT NULL DEFAULT true,
  UNIQUE (tenant_id, platform, external_account_id)
);
CREATE TABLE IF NOT EXISTS social_posts (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(), tenant_id varchar(128) NOT NULL, account_id varchar(128) NOT NULL,
  body text NOT NULL, state varchar(32) NOT NULL DEFAULT 'draft', scheduled_for timestamptz, runtime_post_id varchar(160),
  last_reconciled_at timestamptz, created_at timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS ix_social_posts_tenant_state ON social_posts(tenant_id, state);
CREATE TABLE IF NOT EXISTS social_metric_snapshots (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(), tenant_id varchar(128) NOT NULL, post_id varchar(160) NOT NULL,
  metrics_json text NOT NULL, captured_at timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS ix_social_metrics_post_captured ON social_metric_snapshots(post_id, captured_at DESC);
