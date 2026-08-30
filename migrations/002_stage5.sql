CREATE TABLE IF NOT EXISTS social_sync_checkpoints (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id varchar(128) NOT NULL,
  platform varchar(32) NOT NULL,
  external_account_id varchar(160) NOT NULL,
  cursor_value text,
  last_success_at timestamptz,
  last_attempt_at timestamptz,
  last_error text,
  UNIQUE (tenant_id, platform, external_account_id)
);
CREATE UNIQUE INDEX IF NOT EXISTS uq_social_runtime_post
  ON social_posts(tenant_id, runtime_post_id)
  WHERE runtime_post_id IS NOT NULL;
CREATE INDEX IF NOT EXISTS ix_social_sync_checkpoint_tenant
  ON social_sync_checkpoints(tenant_id, platform);
