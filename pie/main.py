import pie.launcher.launcher
import sys


def entry_point(argv):
    if len(argv) < 2:
        print 'No input file provided'
        return 1

    return pie.launcher.launcher.run(argv[1])


if __name__ == '__main__':
    entry_point(sys.argv)
