from app.models import SocialAccountModel, SocialPostModel


def test_account_tenant_boundary():
    assert SocialAccountModel.__table__.columns["tenant_id"].nullable is False


def test_post_tenant_boundary():
    assert SocialPostModel.__table__.columns["tenant_id"].nullable is False
