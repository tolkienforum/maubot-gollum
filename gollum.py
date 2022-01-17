from maubot import Plugin, MessageEvent
from maubot.handlers import command
from mautrix.types import RoomID
from datetime import datetime


class GollumBot(Plugin):

    @command.new(name="beleidige", aliases=["b"])
    @command.argument("names", pass_raw=True, required=False)
    async def beleidige(self, evt: MessageEvent, names: str) -> None:
        await evt.mark_read()
        await evt.reply("jezz goots ab!")
        self.log.info("Wär: " + names)
        if not names:
            namen = ""
        else:
            namen = names

        async with self.http.get(
                "https://swiss-wowbagger-ultgi7by3q-oa.a.run.app/?format=json&v=undefined&names={}&voice=".format(namen)
        ) as response:
            data = await response.json()

        self.log.info(data)
        await self.client.send_text(evt.room_id, data["text"])

    @command.new(name="mäh")
    async def maeh(self, evt: MessageEvent) -> None:
        await self.client.send_markdown(evt.room_id, "__Mas Tequila!!__")

    @command.new(name="wm")
    async def wm(self, evt: MessageEvent) -> None:
        if evt.sender.startswith("@wm:"):
            await evt.reply("Neeee lassma!")
        else:
            await self.client.kick_user(evt.room_id, evt.sender, "hat wm gesagt!")
            await self.client.send_text(evt.room_id, "Fizzzzzz " + evt.sender + " ist weg!")

    @command.new(name="lion")
    async def lion(self, evt: MessageEvent) -> None:
        await evt.reply("Löwe kommt!")
        await self.send_image(evt.room_id, "https://www.tolkienforum.de/stuff/botme/lions.php", "lion")

    @command.new(name="milooo")
    async def milooo(self, evt: MessageEvent) -> None:
        await evt.reply("Milooo kommt sofort!")
        await self.send_image(evt.room_id, "https://www.tolkienforum.de/stuff/botme/milooos.php", "milooo")

    @command.new(name="rooofy")
    async def rooofy(self, evt: MessageEvent) -> None:
        await evt.reply("Rooofy! Yeah! Sofort!")
        await self.send_image(evt.room_id, "https://www.tolkienforum.de/stuff/botme/roofys.php", "rooofy")

    @command.new(name="geist")
    async def geist(self, evt: MessageEvent) -> None:
        await self.send_image(evt.room_id, "https://www.tolkienforum.de/uploads/default_pf_hsmilie_5.gif", "geist")

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
