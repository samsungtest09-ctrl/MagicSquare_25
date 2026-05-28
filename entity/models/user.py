"""User domain entity for MagicSquare."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class User:
    """Represents a user in the domain layer.

    This class belongs to the ECB `entity` layer and contains only domain data
    and domain rules.

    Attributes:
        user_id: Unique identifier for the user.
        username: Public display name of the user.
        email: Email address used for contact and login.
        is_active: Whether the user account is active.
    """

    user_id: int
    username: str
    email: str
    is_active: bool = True

    def __post_init__(self) -> None:
        """Validate invariants for user entity fields.

        Raises:
            ValueError: If one of the required invariants is violated.
        """
        if self.user_id <= 0:
            raise ValueError("user_id must be a positive integer.")
        if not self.username.strip():
            raise ValueError("username must not be blank.")
        if "@" not in self.email or self.email.startswith("@") or self.email.endswith("@"):
            raise ValueError("email must be a valid email format.")

    def deactivate(self) -> User:
        """Return a new inactive user instance.

        Returns:
            User: New user instance with `is_active` set to False.
        """
        return User(
            user_id=self.user_id,
            username=self.username,
            email=self.email,
            is_active=False,
        )
