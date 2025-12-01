# Django modules
from django.core.exceptions import ValidationError


def validate_indentation(value: int) -> None:
    """
    Validate that the indentation level is between 0 and 5.
    """
    if not value in range(0, 6):
        raise ValidationError(
            message="Indentation level must be between 0 and 5.",
            code="invalid_indentation",
        )
