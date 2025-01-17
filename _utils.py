# source: https://github.com/bzm10/ColorKit/blob/main/ColorKit/colorkit.py
def cmyk_to_rgb(c, m, y, k):
    c, m, y, k = c / 100.0, m / 100.0, y / 100.0, k / 100.0

    # CMYK -> CMY -> RGB
    r = (1 - c) * (1 - k)
    g = (1 - m) * (1 - k)
    b = (1 - y) * (1 - k)

    return (r, g, b)