from dataclasses import dataclass
from typing import Union, Tuple

from PIL import Image, ImageDraw, ImageFont


@dataclass
class Rect:
    x: int
    y: int
    w: int
    h: int


class ImageFactory:
    """画像に文字を書き込むクラス"""

    def __init__(
            self,
            image: Union[Image.Image, str],
            font: Union[ImageFont.FreeTypeFont, Tuple[str, int]],
            rect: Rect
    ):
        """
        :param image: ベースになる画像 (実体 or パス)
        :param font: 書き込むフォント (実体 or (パス, フォントサイズ)のtuple)
        :param rect: 文字を書き込む領域
        """
        self.image = self._load_image(image)
        self.font = self._load_font(font)
        self.rect = rect

    @staticmethod
    def _load_image(x: Union[Image.Image, str]) -> Image.Image:
        if isinstance(x, Image.Image):
            return x
        elif isinstance(x, str):
            return Image.open(x)

    @staticmethod
    def _load_font(x: Union[ImageFont.FreeTypeFont, Tuple[str, int]]) -> ImageFont.FreeTypeFont:
        if isinstance(x, ImageFont.FreeTypeFont):
            return x
        elif isinstance(x, tuple):
            path, size = x
            return ImageFont.truetype(path, size=size)

    def __call__(self, char: str, fill='black') -> Image.Image:
        """
        画像に文字を書き込む

        :param char: 書き込む文字
        :param fill: 文字の色
        :return: 作成した画像
        """
        image = self.image.copy()
        draw = ImageDraw.Draw(image)

        # 中央の座標
        cx = self.rect.x + (self.rect.w // 2)
        cy = self.rect.y + (self.rect.h // 2)

        # 文字が入力される領域
        sw, sh = self.font.getsize(char)

        # 実際に文字が表示される領域
        x1, y1, x2, y2 = self.font.getbbox(char)
        bw = x2 - x1
        bh = y2 - y1

        # 文字を中央に表示する
        dx = sw - bw // 2
        dy = sh - bh // 2
        x = cx - dx
        y = cy - dy
        draw.text((x, y), char, fill, self.font)

        return image
