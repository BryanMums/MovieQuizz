"""Sample Slack ping bot using asyncio and websockets."""
import asyncio
import json
import signal

import aiohttp

import websockets


DEBUG = True
TOKEN = "xoxb-38180923028-EZx5sMipo0PLytXzVEtrU90D"
RUNNING = True
CHANNEL = ""
USER = ""
MESSAGES = []

async def producer():
    """Produce a ping message every 10 seconds."""
    await asyncio.sleep(10)
    return json.dumps({"type": "ping"})


async def consumer(message, ws):
    """Consume the message by printing them."""
    data = json.loads(message)
    if data["type"] == "message":
        CHANNEL = data["channel"]
        USER = data["user"]
        MESSAGES.append(message)




async def bot(token):
    """Create a bot that joins Slack."""
    loop = asyncio.get_event_loop()
    with aiohttp.ClientSession(loop=loop) as client:
        async with client.post("https://slack.com/api/rtm.start",
                               data={"token": TOKEN}) as response:
            assert 200 == response.status, "Error connecting to RTM."
            rtm = await response.json()

    async with websockets.connect(rtm["url"]) as ws:
        while RUNNING:
            listener_task = asyncio.ensure_future(ws.recv())
            producer_task = asyncio.ensure_future(producer())

            done, pending = await asyncio.wait(
                [listener_task, producer_task],
                return_when=asyncio.FIRST_COMPLETED
            )

            for task in pending:
                task.cancel()

            if listener_task in done:
                message = listener_task.result()
                await consumer(message, ws)

            if producer_task in done:
                message = producer_task.result()
                await ws.send(message)


def stop():
    """Gracefully stop the bot."""
    global RUNNING
    RUNNING = False
    print("Stopping... closing connections.")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    loop.set_debug(DEBUG)
    #loop.add_signal_handler(signal.SIGINT, stop)
    loop.run_until_complete(bot(TOKEN))
    loop.close()