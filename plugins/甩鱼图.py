import base64
import io

from mirai import GroupMessage, At, Image as Img
from PIL import Image

from Bot import bot
from tools import conforms, get_avatar, mark

gif1 = Image.open("file/甩鱼1.png")
gif2 = Image.open("file/甩鱼2.png")


@bot.on(GroupMessage)
@mark
@conforms((["看！是", "看!是"], At), (["看！是", "看!是"], At, ""))
async def run(event: GroupMessage, _, at: At, _2=None):
    avatar = await get_avatar(at.target)
    avatar = avatar.resize((36, 36))
    frames = []
    for i in [gif1, gif2]:
        img = Image.new("RGBA", (49, 49))
        img.paste(avatar, (1, 3))
        img.paste(i, (0, 0), gif1)
        frames.append(img)
    img1 = Image.new("RGBA", (49, 49))
    img2 = Image.new("RGBA", (49, 49))

    img1.paste(avatar, (1, 3))
    img1.paste(gif1, (0, 0), gif1)

    img2.paste(avatar, (1, 3))
    img2.paste(gif2, (0, 0), gif2)

    gif_cache = io.BytesIO()
    frames[0].save(gif_cache, format="gif", save_all=True, append_images=frames, duration=1 / 60 * 1000, loop=0)
    b = base64.b64encode(gif_cache.getvalue())
    s = b.decode("utf-8")
    return bot.send(event, Img(base64=s))
