import os
from datetime import datetime
import asyncio
import aiofiles
import logging
import websockets
from dotenv import load_dotenv

load_dotenv("settings.txt")
HISTORY_PATH = os.path.join(os.getcwd(), "data_history")
WSS_URL = "wss://api.bitkub.com/websocket-api/"
DATA_STR = ""

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s :%(levelname)s: %(message)s"
)


def prepare_data_dir():
    logging.info(f"checking history path ({HISTORY_PATH})")
    if not os.path.exists(HISTORY_PATH):
        os.mkdir(HISTORY_PATH)
        logging.info(f"history path is created")
        return
    logging.info(f"history path already exists")


def create_wss_url():
    global WSS_URL
    symbols = [s for s in list(os.environ.get("CAPTURE_COIN", "").split(","))]
    stream_name = ",".join(
        [f"market.ticker.thb_{s.lower()},market.trade.thb_{s.lower()}" for s in symbols])
    # print(stream_name)
    WSS_URL = f"{WSS_URL}{stream_name}"


def get_file_name():
    return os.path.join(HISTORY_PATH, f"{datetime.now().strftime('%Y-%m-%dT%H')}.txt")


async def parse_socket_data(data):
    global DATA_STR
    lines = f"{DATA_STR}{data}".split("\n")
    async with aiofiles.open(get_file_name(), mode="a") as f:
        await f.writelines([f"{line}\n" for line in lines])
        f.close()


async def collect_bitkub_history():
    # logging.info(WSS_URL)
    try:
        async for websocket in websockets.connect(WSS_URL):
            logging.info('Connecting to websocket')
            try:
                async for message in websocket:
                    await parse_socket_data(message)
            except:
                logging.error('Websocket reading error')
    except:
        logging.error('Cannot connect to websocket')


if __name__ == "__main__":
    prepare_data_dir()
    create_wss_url()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(collect_bitkub_history())
    logging.info("END")
