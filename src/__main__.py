# third-party
from loguru import logger

# built in
from time import time, sleep

# local
from syncronizer.utils import read_conf, parse_args
from syncronizer.sync import sync


if __name__ == "__main__":
    start_time = time()
    logger.info(f"Start syncronization -- {start_time}")

    config, active = parse_args() or ""  # можно задать по умолчанию
    dirs = read_conf(config)

    if active:
        try:
            while True:
                sync(dirs)
                sleep(1)
        except KeyboardInterrupt:
            pass
    else:
        sync(dirs)

    logger.info(f"End syncronization -- spent time {time() - start_time}")
