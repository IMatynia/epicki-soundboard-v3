import logging as log
import sys

log.basicConfig(
    format="[%(asctime)s->%(levelname)s->%(module)s" +
    "->%(funcName)s]: %(message)s\n",
    datefmt="%H:%M:%S",
    level=log.INFO
)


def main(args):
    pass


if __name__ == "__main__":
    main(sys.argv)
