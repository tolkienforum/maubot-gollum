from maubot import Plugin, MessageEvent
from maubot.handlers import command
from mautrix.types import RoomID
from datetime import datetime


class GollumBot(Plugin):

    @command.new(name="lion")
    async def lion(self, evt: MessageEvent) -> None:
        await evt.reply("Löwe kommt! ")
        await self.send_image(evt.room_id, "https://www.tolkienforum.de/stuff/botme/lions.php", "lion")

    @command.new(name="milooo")
    async def milooo(self, evt: MessageEvent) -> None:
        await evt.reply("Milooo kommt sofort!")
        await self.send_image(evt.room_id, "https://www.tolkienforum.de/stuff/botme/milooos.php", "milooo")

    @command.new(name="rooofy")
    async def rooofy(self, evt: MessageEvent) -> None:
        await evt.reply("Rooofy! Yeah! Sofort!")
        await self.send_image(evt.room_id, "https://www.tolkienforum.de/stuff/botme/roofys.php", "rooofy")

    async def send_image(self, room_id: RoomID, url: str, file_name_prefix: str) -> None:
        current_time = str(datetime.now().microsecond)
        resp = await self.http.get(url + "?t=" + current_time)
        if resp.status != 200:
            self.log.warning(f"Unexpected status fetching image {url}: {resp.status}")
            return None

        data = await resp.read()
        uri = await self.client.upload_media(data)
        self.log.info(f"read image from {url} and uploaded it to {uri}")

        await self.client.send_image(room_id, url=uri, file_name=file_name_prefix + "-" + current_time)
