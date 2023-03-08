from django.contrib.auth.tokens import PasswordResetTokenGenerator


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        email_field = user.get_email_field_name()
        email = getattr(user, email_field, "") or ""
        active_status = user.is_active
        return f"{user.pk}{timestamp}{email}{active_status}"


account_activation_token = AccountActivationTokenGenerator()


class CustomPasswordResetTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        login_timestamp = (
            ""
            if user.last_login is None
            else user.last_login.replace(microsecond=0, tzinfo=None)
        )
        email_field = user.get_email_field_name()
        email = getattr(user, email_field, "") or ""
        password_ = user.password
        return f"{user.pk}{login_timestamp}{timestamp}{email}{password_}"


password_reset_token = CustomPasswordResetTokenGenerator()
