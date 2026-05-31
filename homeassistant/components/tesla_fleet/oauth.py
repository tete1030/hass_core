"""Provide oauth implementations for the Tesla Fleet integration."""

from typing import Any

from homeassistant.components.application_credentials import (
    AuthImplementation,
    AuthorizationServer,
    ClientCredential,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.config_entry_oauth2_flow import AUTH_CALLBACK_PATH

from .const import AUTHORIZE_URL, SCOPES, TOKEN_URL


class TeslaUserImplementation(AuthImplementation):
    """Tesla Fleet API user OAuth2 implementation."""

    def __init__(
        self, hass: HomeAssistant, auth_domain: str, credential: ClientCredential
    ) -> None:
        """Initialize the Tesla OAuth2 implementation."""
        super().__init__(
            hass,
            auth_domain,
            credential,
            AuthorizationServer(AUTHORIZE_URL, TOKEN_URL),
        )
        self.public_callback_base_url: str | None = None

    @property
    def redirect_uri(self) -> str:
        """Return the Tesla OAuth redirect URI."""
        if self.public_callback_base_url:
            return f"{self.public_callback_base_url}{AUTH_CALLBACK_PATH}"
        return super().redirect_uri

    @property
    def extra_authorize_data(self) -> dict[str, Any]:
        """Extra data that needs to be appended to the authorize URL."""
        return {
            "prompt": "login",
            "prompt_missing_scopes": "true",
            "scope": " ".join(SCOPES),
        }
