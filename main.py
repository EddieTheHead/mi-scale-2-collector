import asyncio
import logging

from bleak import BleakClient, BleakScanner
from bleak.uuids import normalize_uuid_16
from bleak.backends.characteristic import BleakGATTCharacteristic

import google_sheets_connector
from weight_scale_measurement import ScaleMeasurement, parse_weight_measurement_message

WEIGHT_SCALE_SERVICE_UUID = normalize_uuid_16(0x181d)
WEIGHT_SCALE_FEATURE_CHAR_UUID = normalize_uuid_16(0x2a9e)
WEIGHT_MEASUREMENT_UUID = normalize_uuid_16(0x2a9d)

OUT_FILE_PATH = 'measurements.csv'

logger = logging.getLogger(__name__)

def append_to_csv(measurement : ScaleMeasurement, file_path = OUT_FILE_PATH):
    with open(file_path, 'a') as out_file:
        out_file.write(f'{measurement.time},{measurement.collection_time}, {measurement.weight}, {measurement.unit}, {measurement.stabilized}\n')

def notification_handler(characteristic: BleakGATTCharacteristic, data: bytearray):
    """Handler for weight measurement notification"""
    logger.debug('Notification: from %s, data: %s, len: %i', characteristic, data, len(data))

    message = parse_weight_measurement_message(data)
    logger.debug(message)

    if message.stabilized:
        logger.info(message)
        append_to_csv(message)
        google_sheets_connector.append_weight_measurement(message)


async def connect_and_measure():
    disconnected_event = asyncio.Event()

    def disconnected_callback(bleak_client: BleakClient):
        logger.info("disconnected callback")
        disconnected_event.set()

    device = await BleakScanner().find_device_by_name("MI SCALE2")

    if not device:
        logger.info("no device found")
        return
    else: 
        logger.info(f"found device: {device.name}")

    client = BleakClient(device, disconnected_callback=disconnected_callback)

    async with client:
        await client.start_notify(WEIGHT_MEASUREMENT_UUID, notification_handler)
        await disconnected_event.wait()

async def main():
    logger.info("starting scan")
    while True:
        await connect_and_measure()
        logger.info("restarting scan")

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)-15s %(name)-8s %(levelname)s: %(message)s",
    )

    asyncio.run(main())