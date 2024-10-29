def rgb_val(colour: str, alpha_front: bool = True) -> tuple[int, int, int]:
    if colour.startswith("#"):
        colour = colour[1:]
    if len(colour) == 8:
        if alpha_front:
            colour = colour[2:]
        else:
            colour = colour[:6]
    if len(colour) == 6:
        return tuple(int(colour[i:i + 2], 16) for i in (0, 2, 4))
    raise ValueError(f"Invalid colour: {colour}")


def alpha_val(colour: str) -> int:
    if colour.startswith("#"):
        colour = colour[1:]
    if len(colour) == 8:
        return int(colour[:2], 16)
    return 255


def brightness(colour: str) -> float:
    r, g, b = rgb_val(colour)
    return 0.299 * r + 0.587 * g + 0.114 * b


def contrast(colour1: str, colour2: str) -> float:
    return abs(brightness(colour1) - brightness(colour2))


def is_dark(colour: str) -> bool:
    return brightness(colour) < 128


def is_light(colour: str) -> bool:
    return brightness(colour) >= 128


def is_contrast(colour1: str, colour2: str) -> bool:
    return contrast(colour1, colour2) >= 128


def is_similar(colour1: str, colour2: str) -> bool:
    return contrast(colour1, colour2) < 32


def contrast_bw(colour: str) -> str:
    return "#FFFFFF" if is_dark(colour) else "#000000"
