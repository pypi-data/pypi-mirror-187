from io import BytesIO, TextIOWrapper
from typing import Union, Optional

import aiohttp
import os
import re
import shutil
import zipfile
from pathlib import Path
from nonebot.log import logger

osufile = Path(__file__).parent / 'osufile'
map_path = Path() / "data" / "osu" / "map"
if not map_path.exists():
    map_path.mkdir(parents=True, exist_ok=True)


async def map_downloaded(setid: str) -> Optional[Path]:
    # 判断是否存在该文件
    path = map_path / setid
    if setid in os.listdir(map_path) and list(path.glob('*.osu')):
        return path
    url = f'https://txy1.sayobot.cn/beatmaps/download/novideo/{setid}'
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, allow_redirects=False) as req:
                sayo = req.headers['Location']
    except Exception as e:
        logger.error(f'Request Failed or Timeout\n{e}')
    filepath = await osz_file_dl(sayo, int(setid))
    # 解压下载的osz文件
    myzip = zipfile.ZipFile(filepath.absolute())
    myzip.extractall(myzip.filename[:-4])
    myzip.close()
    # 删除文件
    remove_file(Path(str(filepath)[:-4]))
    os.remove(filepath)
    return path


async def download_map(setid: int) -> Optional[Path]:
    url = f'https://txy1.sayobot.cn/beatmaps/download/novideo/{setid}'
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, allow_redirects=False) as req:
                sayo = req.headers['Location']
    except Exception as e:
        logger.error(f'Request Failed or Timeout\n{e}')
    filepath = await osz_file_dl(sayo, setid, True)
    return filepath


async def osz_file_dl(sayo: str, setid: int, dl: bool = False) -> Optional[Path]:
    async with aiohttp.ClientSession() as session:
        async with session.get(sayo) as req:
            if not req.content_disposition:
                return
            osufilename = req.content_disposition.filename
            logger.info(f'Start Downloading Map: {osufilename}')
            filename = f'{setid}.osz' if not dl else osufilename
            filepath = map_path / filename
            chunk = await req.read()
            open(filepath, 'wb').write(chunk)
    logger.info(f'Map: <{osufilename}> Download Complete')
    return filepath


async def get_projectimg(url: str):
    try:
        if 'avatar-guest.png' in url:
            url = 'https://osu.ppy.sh/images/layout/avatar-guest.png'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as req:
                if req.status == 403:
                    return osufile / 'work' / 'mapbg.png'
                data = await req.read()
                im = BytesIO(data)
        return im
    except Exception as e:
        logger.error(f'Image Failed: {e}')
        return e


def remove_file(path: Path) -> bool:
    bg_list = set()
    for file in os.listdir(path):
        if '.osu' in file:
            bg = re_map(path / file)
            bg_list.add(bg)
            bid = get_map_id(path / file)
            os.rename(path / file, path / f'{bid}.osu')

    for root, dir, files in os.walk(path, topdown=False):
        for name in files:
            if name not in bg_list and '.osu' not in name:
                os.remove(os.path.join(root, name))
        for dirname in dir:
            shutil.rmtree(os.path.join(root, dirname))
    return True


def re_map(file: Union[bytes, Path]) -> str:
    if isinstance(file, bytes):
        text = TextIOWrapper(BytesIO(file), 'utf-8').read()
    else:
        with open(file, 'r', encoding='utf-8') as f:
            text = f.read()
    res = re.search(r'\d,\d,\"(.+)\"', text)
    bg = 'mapbg.png' if not res else res.group(1).strip()
    return bg


def get_map_id(file: Path) -> str:
    with open(file, 'r', encoding='utf-8') as f:
        text = f.read()
    res = re.search(r'BeatmapID:(\d*)', text)
    return res.group(1).strip()
