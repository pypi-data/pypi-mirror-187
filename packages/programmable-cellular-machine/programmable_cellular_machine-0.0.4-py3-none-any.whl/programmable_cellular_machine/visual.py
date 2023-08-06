import abc
import multiprocessing
import threading
from copy import copy
from pathlib import Path

import cv2
import numpy as np
import pygame
from PIL import Image, ImageDraw

from programmable_cellular_machine.palette import Palette
from programmable_cellular_machine.places import BasePlace


class VisualProvider(abc.ABC):
    palette: Palette

    def __init__(self, palette: Palette) -> None:
        self.palette = palette
        pass

    def start(self, place: BasePlace):
        pass

    @abc.abstractmethod
    def render(self, place: BasePlace):
        pass

    def stop(self, place: BasePlace | None):
        pass


class DevNullProvider(VisualProvider):
    def __init__(self, *args, **kwargs) -> None:
        pass

    def render(self, place: BasePlace):
        pass


class ImageProviderMixin(VisualProvider):

    width: int | None
    height: int | None

    def make_image(self, place: BasePlace):
        image = Image.new('RGBA', (place.width, place.height), color=0)
        draw = ImageDraw.Draw(image)

        for pos_x, pos_y, value in place.cells:
            color = self.palette.get(value)
            draw.point((pos_x, pos_y), color)

        if self.width == place.width and self.height == place.height:
            return image

        return image.resize((self.width, self.height), Image.ANTIALIAS)


class ImageAsTextProviderMixin(VisualProvider):

    width: int | None
    height: int | None

    def make_image(self, place: BasePlace):
        text_palette = {}
        for pos_x, pos_y, value in place.cells:
            color = self.palette.get(value)
            text_palette[(pos_x, pos_y)] = color
        if self.width == place.width and self.height == place.height:
            return text_palette
        return text_palette


class ResultImageAsTextProvider(ImageAsTextProviderMixin, VisualProvider):
    width: int
    height: int

    file: Path

    def __init__(
        self,
        palette: Palette,
        width: int,
        height: int,
        filename: str
    ) -> None:
        super().__init__(palette)

        self.width = width
        self.height = height

        self.file = Path(filename).absolute()

    def render(self, place: BasePlace):
        pass

    def stop(self, place: BasePlace | None):
        if place is None:
            return

        image_as_text = str(self.make_image(place))
        print(f'imastext = {image_as_text[:10]}')
        with open(self.file, 'w') as f:
            f.write(image_as_text)


class ImageProvider(ImageProviderMixin, VisualProvider):

    width: int
    height: int

    # 'video_provider.avi'
    file: Path

    increment: int

    def __init__(self, palette: Palette, width: int, height: int, filename: str) -> None:
        super().__init__(palette)

        self.width = width
        self.height = height

        self.file = Path(filename).absolute()

        self.increment = 0

    def render(self, place: BasePlace):
        image = self.make_image(place)

        self.increment += 1

        path = copy(self.file)
        path = path.parent / f'{self.increment}-{path.name}'

        image.save(path)


class ResultImageProvider(ImageProviderMixin, VisualProvider):

    width: int
    height: int

    file: Path

    def __init__(
        self,
        palette: Palette,
        width: int,
        height: int,
        filename: str
    ) -> None:
        super().__init__(palette)

        self.width = width
        self.height = height

        self.file = Path(filename).absolute()

    def render(self, place: BasePlace):
        pass

    def stop(self, place: BasePlace | None):
        if place is None:
            return

        image = self.make_image(place)
        image.save(self.file)


class VideoProvider(ImageProviderMixin, VisualProvider):
    """Провайдер для сохранения работы машины как видео"""

    width: int
    height: int
    fps: int

    # 'video_provider.avi'
    filename: str

    video: cv2.VideoWriter

    def __init__(self, palette: Palette, width: int, height: int, fps: int, filename: str) -> None:
        super().__init__(palette)

        self.width = width
        self.height = height
        self.fps = fps
        self.filename = filename

    def start(self, *args):
        self.video = cv2.VideoWriter(
            self.filename,
            cv2.VideoWriter_fourcc(*'DIVX'),
            self.fps,
            (self.width, self.height),
        )

    def render(self, place: BasePlace):
        image = self.make_image(place)

        image_data = np.array(image)
        image_data = cv2.cvtColor(image_data, cv2.COLOR_RGB2BGR)

        self.video.write(image_data)

    def stop(self, *args):
        self.video.release()


class PygameProvider(VisualProvider):
    """Визуальный провайдер pygame"""

    fps: int

    screen: pygame.Surface

    def __init__(self, palette: Palette, fps: int | None = None) -> None:
        super().__init__(palette)
        self.fps = fps or 0

    def start(self, place: BasePlace):
        pygame.init()

        self.screen = pygame.display.set_mode([place.width, place.height])
        self.clock = pygame.time.Clock()

    def render(self, place: BasePlace):
        for pos_x, pos_y, value in place.cells:
            color = self.palette.get(value)
            self.screen.set_at((pos_x, pos_y), color)

        pygame.display.flip()

        pygame.display.set_caption(f'FPS: {int(self.clock.get_fps())}')
        self.clock.tick(self.fps)

    def stop(self, *args):
        pygame.quit()


class MultiVisualProvider(VisualProvider):
    providers: list[VideoProvider]
    threads: list[threading.Thread]

    def __init__(self, providers: list[VideoProvider]) -> None:
        self.providers = providers
        self.threads = []

    def start_thread(self, thread: threading.Thread):
        thread.start()

        self.threads.append(thread)

    def join(self):
        for thread in self.threads:
            thread.join()

    def start(self, place: BasePlace):
        for provider in self.providers:
            thread = threading.Thread(target=provider.start, args=(place,))
            self.start_thread(thread)

        self.join()

    def render(self, place: BasePlace):
        for provider in self.providers:
            thread = threading.Thread(target=provider.render, args=(place,))
            self.start_thread(thread)
        self.join()

    def stop(self, place: BasePlace | None):
        for provider in self.providers:
            thread = threading.Thread(target=provider.stop, args=(place,))
            self.start_thread(thread)
        self.join()

    # def start(self, place: BasePlace):
    #     for provider in self.providers:
    #         provider.start(place)

    # def render(self, place: BasePlace):
    #     for provider in self.providers:
    #         provider.render(place)

    # def stop(self, place: BasePlace | None):
    #     for provider in self.providers:
    #         provider.stop(place)


class QueueVisualProvider(VisualProvider):

    provider: VideoProvider

    def __init__(self, provider: VideoProvider) -> None:
        self.provider = provider

    def worker(self, queue: multiprocessing.Queue):
        while True:
            item = queue.get()

            if item is None:
                break

            if item[0] == 'render':
                self.provider.render(item[1])
                continue

            if item[0] == 'start':
                self.provider.start(item[1])
                continue

            if item[0] == 'stop':
                self.provider.stop(item[1])
                continue

    def start(self, place: BasePlace):
        self.queue = multiprocessing.Queue()

        self.process = multiprocessing.Process(target=self.worker, args=(self.queue,))
        self.process.start()

        self.queue.put(('start', place))

    def render(self, place: BasePlace):
        self.queue.put(('render', place))

    def stop(self, place: BasePlace | None):
        self.queue.put(('stop', place))
        self.queue.put(None)

        # self.queue.join()

        self.process.join()
        self.process.terminate()


def queue(provider: VideoProvider):
    return QueueVisualProvider(provider)


def multi(*providers: VideoProvider):
    return MultiVisualProvider(providers)


def gen_queue_from_all_provider(palette: Palette, width: int, height: int, fps: int) -> VisualProvider:
    return queue(
        multi(
            [
                VideoProvider(palette, width, height, fps, 'export/cells.avi'),
                PygameProvider(palette, fps),
                ResultImageProvider(palette, width, height, 'export/cells.png'),
            ]
        )
    )
