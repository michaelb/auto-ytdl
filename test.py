from autoytdl.config import Config
c = Config()
c.load()
print(c.youtube_dl_args)
