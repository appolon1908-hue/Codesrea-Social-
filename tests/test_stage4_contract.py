from app.main import SOCIAL_PUBLISHING_ENABLED, SOCIAL_READ_SYNC_ENABLED


def test_social_publishing_defaults_off():
    assert SOCIAL_PUBLISHING_ENABLED is False


def test_social_read_sync_defaults_off():
    assert SOCIAL_READ_SYNC_ENABLED is False
