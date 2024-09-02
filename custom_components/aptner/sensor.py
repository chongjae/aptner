import logging
from datetime import timedelta

from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class CarSensor(CoordinatorEntity):
    """Representation of a Sensor."""

    def __init__(self, coordinator, username, password):
        """Initialize the sensor."""
        super().__init__(coordinator, f"{username}_car_sensor")
        self._username = username
        self._password = password
        self._state = coordinator.data

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self._username}_car_sensor"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def icon(self):
        return "mdi:car"

    async def async_update(self):
        """Fetch new state data for the sensor."""
        self._state = await self.coordinator.data.update()


class CostSensor(CoordinatorEntity):
    """Representation of a Sensor."""

    def __init__(self, coordinator, username, password):
        """Initialize the sensor."""
        super().__init__(coordinator, f"{username}_cost_sensor")
        self._username = username
        self._password = password
        self._state = coordinator.data

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self._username}_cost_sensor"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def icon(self):
        return "mdi:cash-clock"

    async def async_update(self):
        """Fetch new state data for the sensor."""
        self._state = await self.coordinator.data.update()


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the sensor platform."""
    aptner = hass.data[DOMAIN][config_entry.entry_id]
    car_coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="sensor",
        update_method=aptner.find_car,
        update_interval=timedelta(minutes=1),
    )
    cost_coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="sensor",
        update_method=aptner.get_cost,
        update_interval=timedelta(hours=24),
    )
    await car_coordinator.async_config_entry_first_refresh()
    await cost_coordinator.async_config_entry_first_refresh()

    async_add_entities([CarSensor(car_coordinator, aptner.id, aptner.password)], False)
    async_add_entities([CostSensor(cost_coordinator, aptner.id, aptner.password)], False)
