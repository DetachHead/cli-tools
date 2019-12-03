from __future__ import annotations

import enum
from dataclasses import dataclass
from datetime import datetime

from .bundle_id import BundleIdPlatform
from .resource import Resource


class DeviceClass(enum.Enum):
    APPLE_TV = 'APPLE_TV'
    APPLE_WATCH = 'APPLE_WATCH'
    IPAD = 'IPAD'
    IPHONE = 'IPHONE'
    IPOD = 'IPOD'
    MAC = 'MAC'


class DeviceStatus(enum.Enum):
    DISABLED = 'DISABLED'
    ENABLED = 'ENABLED'


class Device(Resource):
    """
    https://developer.apple.com/documentation/appstoreconnectapi/device
    """

    @dataclass
    class Attributes(Resource.Attributes):
        deviceClass: DeviceClass
        model: str
        name: str
        platform: BundleIdPlatform
        status: DeviceStatus
        udid: str
        addedDate: datetime

        def __post_init__(self):
            if isinstance(self.deviceClass, str):
                self.deviceClass = DeviceClass(self.deviceClass)
            if isinstance(self.platform, str):
                self.platform = BundleIdPlatform(self.platform)
            if isinstance(self.status, str):
                self.status = DeviceStatus(self.status)
            if isinstance(self.addedDate, str):
                self.addedDate = Resource.from_iso_8601(self.addedDate)