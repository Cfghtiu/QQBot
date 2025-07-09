import io

from PIL import Image
from mirai import At, GroupMessage

from Bot import bot
from tools import conforms, get_avatar, to_img, mark

img = Image.open("file/丢.png")


@bot.on(GroupMessage)
@mark
@conforms(["我丢"], ["我丢", At], ["我丢", At, ""])
async def run(event: GroupMessage, _, at=None, __=None):
    if at is None:
        at = At(event.sender.id)
    avatar: Image.Image = await get_avatar(at.target)
    avatar = avatar.resize((137, 137)).rotate(-160)
    img_copy = img.copy()
    r = 68
    for i in range(136):
        for j in range(136):
            lx = abs(i - r)
            ly = abs(j - r)
            e = (pow(lx, 2) + pow(ly, 2)) ** 0.5
            if e < r:
                img_copy.putpixel((19 + i, 180 + j), avatar.getpixel((i, j)))
    cache = io.BytesIO()
    img_copy.save(cache, format="png")
    return bot.send(event, to_img(cache))
