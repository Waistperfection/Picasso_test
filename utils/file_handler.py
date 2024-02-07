from typing import Callable

from api.models import File


class FormatHandlerAlreadyExists(Exception):
    ...


class FileHandler:

    def __init__(self):
        self.__handlers: dict[str, Callable] = {}

    @staticmethod
    def default_handler(file: File):
        print("default_handler")

    def get_handler(self, file: File) -> Callable:
        file_format = file.file.name.split(".")[-1]
        return self.__handlers.get(file_format, self.default_handler)

    def __call__(self, file):
        handler = self.get_handler(file)
        handler(file)

    def register(self, file_format: str, func: Callable):
        if file_format.startswith("."):
            raise ValueError(
                "The valid file format should be written without a dot : {file_format} => {file_format[1:]}"
            )
        if not callable(func):
            raise TypeError(
                "Please check that you are not trying to register not callable object."
            )
        if h := self.__handlers.get(file_format.lower(), None):
            raise FormatHandlerAlreadyExists(
                f"Handler function for '{file_format.lower()}' already exists {h.__name__}"
            )
        self.__handlers[file_format.lower()] = func


handler = FileHandler()

def process_png(file: File):
    print("png file")


def process_jpg(file: File):
    print("jpg file")


def process_txt(file: File):
    print("txt file")


handler.register("png", process_png)
handler.register("jpg", process_jpg)
handler.register("txt", process_txt)
