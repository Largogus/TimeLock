def resizeWidget(h: int, min_h: int, max_h: int, min_space: int = 0, max_space: int = 100) -> int:
    space = min_space

    if h <= min_h:
        space = min_space
    elif h >= max_h:
        space = max_space
    else:
        k = (h - min_h) / (max_h - min_h)
        space = int(min_space + k * (max_space - min_space))

    return space