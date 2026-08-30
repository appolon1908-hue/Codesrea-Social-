from app.models import SocialAccount, SocialPost


def test_account_tenant_boundary():
    assert SocialAccount.__table__.columns["tenant_id"].nullable is False


def test_post_tenant_boundary():
    assert SocialPost.__table__.columns["tenant_id"].nullable is False
