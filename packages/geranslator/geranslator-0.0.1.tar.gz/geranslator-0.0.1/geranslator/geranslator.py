from .config.config import Config

class Geranslator:
    lang_dir = Config.get('lang_dir')

    def translate(self):
        print(self.lang_dir)
        exit()
