from knox.settings import knox_settings

RENEW_EXPIRY_MAPPING = {
    "mobile": knox_settings.MOBILE_TOKEN_TTL,
    "restricted": knox_settings.RESTRICTED_TOKEN_TTL,
    "trusted_web": knox_settings.TRUSTED_WEB_TOKEN_TTL,
    "web": knox_settings.WEB_TOKEN_TTL
}