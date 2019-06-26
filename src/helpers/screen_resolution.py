from win32api import GetSystemMetrics


def screen_resolution():
    screen_w = GetSystemMetrics(0)
    screen_h = GetSystemMetrics(1)

    return "{}x{}".format(screen_w, screen_h)


if __name__ == '__main__':
    print("{}".format(screen_resolution()))
