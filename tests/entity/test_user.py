"""Tests for the User entity."""

import pytest

from entity.models.user import User


def test_user_creation_with_valid_values() -> None:
    """Create a valid user entity."""
    # Arrange
    user_id = 1
    username = "alice"
    email = "alice@example.com"

    # Act
    user = User(user_id=user_id, username=username, email=email)

    # Assert
    assert user.user_id == user_id
    assert user.username == username
    assert user.email == email
    assert user.is_active is True


def test_user_creation_raises_when_user_id_is_not_positive() -> None:
    """Reject non-positive user id."""
    # Arrange
    invalid_user_id = 0

    # Act / Assert
    with pytest.raises(ValueError, match="user_id must be a positive integer."):
        User(user_id=invalid_user_id, username="alice", email="alice@example.com")


def test_user_creation_raises_when_username_is_blank() -> None:
    """Reject blank username."""
    # Arrange
    blank_username = "   "

    # Act / Assert
    with pytest.raises(ValueError, match="username must not be blank."):
        User(user_id=1, username=blank_username, email="alice@example.com")


def test_user_creation_raises_when_email_is_invalid() -> None:
    """Reject invalid email."""
    # Arrange
    invalid_email = "alice.example.com"

    # Act / Assert
    with pytest.raises(ValueError, match="email must be a valid email format."):
        User(user_id=1, username="alice", email=invalid_email)


def test_deactivate_returns_new_inactive_user() -> None:
    """Deactivate user without mutating original instance."""
    # Arrange
    active_user = User(user_id=1, username="alice", email="alice@example.com")

    # Act
    deactivated_user = active_user.deactivate()

    # Assert
    assert active_user.is_active is True
    assert deactivated_user.is_active is False
    assert deactivated_user.user_id == active_user.user_id
    assert deactivated_user.username == active_user.username
    assert deactivated_user.email == active_user.email
