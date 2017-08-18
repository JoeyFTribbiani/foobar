def distSq(xa, ya, xb, yb):
    return (xb - xa) ** 2 + (yb - ya) ** 2


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def extendXInMirrors(x, y, capX, capY, w, distance):
    margin = w - x
    curX = x + 2 * margin
    curY = y
    res = []
    while distSq(capX, capY, curX, curY) <= distance ** 2:
        res += (curX, curY),
        margin = w - margin
        curX = curX + 2 * margin

    margin = x
    curX = x - 2 * margin
    while distSq(capX, capY, curX, curY) <= distance ** 2:
        res += (curX, curY),
        margin = w - margin
        curX = curX - 2 * margin

    return res


def extendYInMirrors(x, y, capX, capY, h, distance):
    margin = h - y
    curX = x
    curY = y + 2 * margin
    res = []
    while distSq(capX, capY, curX, curY) <= distance ** 2:
        res += (curX, curY),
        margin = h - margin
        curY = curY + 2 * margin

    margin = y
    curY = y - 2 * margin
    while distSq(capX, capY, curX, curY) <= distance ** 2:
        res += (curX, curY),
        margin = h - margin
        curY = curY - 2 * margin

    return res


def answer(dimensions, captain_position, badguy_position, distance):
    bx, by = badguy_position
    w, h = dimensions
    x, y = captain_position

    # Judge if the minimal distance from captain to bad guy is shorter than required distance
    if distSq(x, y, bx, by) > distance ** 2:
        return 0

    # Copy captain in the mirrors(walls)
    capsX = extendXInMirrors(x, y, x, y, w, distance) + [(x, y)]
    caps = []
    for point in capsX:
        caps += extendYInMirrors(point[0], point[1], x, y, h, distance)
    caps += capsX

    # Shooting directions from captain self to the captain in the mirror
    dirs2cap = {}
    for point in caps:
        dx = point[0] - x
        dy = point[1] - y
        if dx == 0 and dy == 0:
            continue
        gcdV = abs(gcd(dx, dy))
        k = str(dx / gcdV) + "," + str(dy / gcdV)
        if gcdV and (k not in dirs2cap or gcdV < dirs2cap[k]):
            dirs2cap[k] = gcdV

    # Copy bad guy in the mirrors(walls)
    badguysX = extendXInMirrors(bx, by, x, y, w, distance) + [(bx, by)]
    badguys = []
    for point in badguysX:
        badguys += extendYInMirrors(point[0], point[1], x, y, h, distance)
    badguys += badguysX

    # Shooting directions from captain to the bad guy if not shooting the captain first
    dirs2bg = {}
    for point in badguys:
        dx = point[0] - x
        dy = point[1] - y
        gcdV = abs(gcd(dx, dy))
        k = str(dx / gcdV) + "," + str(dy / gcdV)
        if (k not in dirs2cap or gcdV < dirs2cap[k]) and (k not in dirs2bg or gcdV < dirs2bg[k]):
            dirs2bg[k] = gcdV

    return len(dirs2bg.items())