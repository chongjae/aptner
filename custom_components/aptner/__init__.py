import logging
from datetime import timedelta
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from homeassistant.components import persistent_notification

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_USERNAME, CONF_PASSWORD
from homeassistant.core import (
    HomeAssistant,
    ServiceResponse,
    ServiceCall,
    SupportsResponse,
)
from .aptner import Aptner
from .const import DOMAIN, CAR_RESERVATION_SERVICE_NAME

_LOGGER = logging.getLogger(__name__)

MIN_TIME_BETWEEN_UPDATES = timedelta(minutes=1)


async def async_setup(hass, config):
    """Set up the integration."""
    hass.data[DOMAIN] = {}
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up the integration from a config entry."""
    username = entry.data[CONF_USERNAME]
    password = entry.data[CONF_PASSWORD]
    aptner = Aptner(hass, username, password)  # Modify this line

    hass.data[DOMAIN][entry.entry_id] = aptner

    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "sensor")
    )

    await _async_setup_service(hass, entry)

    return True


CAR_RESERVATION_SCHEMA = vol.Schema(
    {
        vol.Required("car_no"): cv.string
    }
)


async def _async_setup_service(hass: HomeAssistant, entry: ConfigEntry):
    """서비스를 설정합니다."""

    async def _async_car_reservation(call: ServiceCall) -> ServiceResponse:
        """주차 등록을 수행합니다."""
        try:
            car_no = call.data["car_no"]
            aptner = hass.data[DOMAIN][entry.entry_id]
            await aptner.reservation_car(car_no)
            message = await aptner.get_current_reservation_list()
            persistent_notification.async_create(
                hass, message, "예약 리스트", call.context.id
            )
            return {
                "result": "success",
                "value": message,
            }
        except Exception as e:
            persistent_notification.async_create(
                hass, str(e), "주차 예약 실패", call.context.id
            )
            return {
                "result": "fail",
                "message": str(e),
            }

    hass.services.async_register(
        DOMAIN,
        CAR_RESERVATION_SERVICE_NAME,
        _async_car_reservation,
        schema=CAR_RESERVATION_SCHEMA,
        supports_response=SupportsResponse.ONLY,
    )
