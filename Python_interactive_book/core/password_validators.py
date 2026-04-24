import re
import string

from django.core.exceptions import ValidationError


class ComplexPasswordValidator:
    """
    Пароль: ≥8 символов, латинские a–z и A–Z, цифра, спецсимвол (string.punctuation).
    """

    def validate(self, password, user=None):
        errors = []
        if len(password) < 8:
            errors.append("Пароль должен быть не короче 8 символов.")
        if not re.search(r"[a-z]", password):
            errors.append("Добавьте хотя бы одну строчную латинскую букву (a–z).")
        if not re.search(r"[A-Z]", password):
            errors.append("Добавьте хотя бы одну прописную латинскую букву (A–Z).")
        if not re.search(r"\d", password):
            errors.append("Добавьте хотя бы одну цифру (0–9).")
        if not any(ch in string.punctuation for ch in password):
            errors.append("Добавьте хотя бы один спецсимвол (!@#$%… и т.п.).")
        if errors:
            raise ValidationError(errors)

    def get_help_text(self):
        return (
            "Не менее 8 символов: латинские строчные и прописные буквы, "
            "цифра и спецсимвол из набора ASCII."
        )
