import asyncio
import logging

from bleak import BleakClient, BleakScanner
from bleak.uuids import normalize_uuid_16

import time_update_message

WEIGHT_SCALE_SERVICE_UUID = normalize_uuid_16(0x181d)
CURRENT_TIME_UUID = normalize_uuid_16(0x2a2b)

logger = logging.getLogger(__name__)

async def update_time_on_scale():
    device = await BleakScanner().find_device_by_name("MI SCALE2")
    if not device:
        logger.info("no device found")
        return
    else: 
        logger.info(f"found device: {device.name}")

    client = BleakClient(device)
    await client.connect()
    service = client.services.get_service(WEIGHT_SCALE_SERVICE_UUID)

    characteristic = service.get_characteristic(CURRENT_TIME_UUID)
    payload = time_update_message.get_time_update_cmd()

    await client.write_gatt_char(
        characteristic, payload
    )

async def list_mi_devices():
    scanner = BleakScanner()
    print(await scanner.discover())


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)-15s %(name)-8s %(levelname)s: %(message)s",
    )

    asyncio.run(update_time_on_scale())
