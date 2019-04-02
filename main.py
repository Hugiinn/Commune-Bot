import asyncio
from bot import CommuneBot

loop = asyncio.get_event_loop()

def main():

    Bot = CommuneBot()

    asyncio.ensure_future(Bot.start())
    loop.run_forever()

    loop.close()

main()



