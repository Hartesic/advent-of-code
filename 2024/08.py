my_input = """
.....................................O..V.........
..................................................
................................O.........Z.......
....W....................................V....v...
........................m................8........
.....................................n........Z..v
.............F.....3...n....5m....................
................................................V.
................3............iv....Z.............V
...........................O..n..i........p......H
......W..6..............................i.........
......................................b...........
..................................n........p......
........M.......c...........m..5......1...........
...M............................L..5..A...........
...w...........9.............F5..................q
.W.....................................q....p.....
.......W........r.......H.....LA......q...........
................4.F....................A..........
........3.......a.....F...................A..L....
....ME...............................Q..........q.
.E..................ih...................Z........
................E...H...........h.................
.........m.........X..............................
..................0......C.................h......
.M......l.................Q.h.....................
..........C..............0........................
.............lX............3.c....................
......8.X.........c....r..a......H.....9..........
.................QE.....C.........................
..R................a........Q...................7.
...........................a......................
l..........X.R............1..I..........9.........
.................0R..............b.....z......x...
.......l.....w....r..........................b....
.8..........0...................P1z...............
.............c.........................L..........
.................C..N............o............9...
...........e..f..N................................
8.............................B...................
...........4...............................x......
....w....RY..........4.......................P....
.........yw.....Y.............o2...............7..
..6y........4..............fo..............7......
.........Y..6............o......................x.
.....Y....e.....y..I.r...........2................
....e.............................P.......z.bB....
.............6.................B........7......x..
..y.N........f...........1....I....z....B.........
.....e....f.............I.................2.......
""".strip()


def get_frequencies_and_map_boundaries():
    all_antennas: dict[str, list[tuple[int, int]]] = {}
    for y, line in enumerate(my_input.split('\n')):
        for x, char in enumerate(line):
            if char == '.':
                continue
            if char not in all_antennas:
                all_antennas[char] = []
            all_antennas[char].append((y, x))
    return all_antennas, y + 1, x + 1


frequencies, lines_count, line_len = get_frequencies_and_map_boundaries()


def get_antinode(antenna: tuple[int, int], pos_diff: tuple[int, int]):
    y_diff, x_diff = pos_diff
    return (antenna[0] + y_diff, antenna[1] + x_diff)


def get_pos_diff(pos_1: tuple[int, int], pos_2: tuple[int, int]):
    return (pos_2[0] - pos_1[0], pos_2[1] - pos_1[1])


def get_reversed_pos_diff(pos_diff: tuple[int, int]):
    return (pos_diff[0] * -1, pos_diff[1] * -1)


def is_on_map(pos: tuple[int, int]):
    y, x = pos
    if y < 0 or y >= lines_count:
        return False
    if x < 0 or x >= line_len:
        return False
    return True


#
# --- Part One ---
#
def part_one():
    antinodes: set[tuple[int, int]] = set()
    for antennas in frequencies.values():
        for antenna_idx, antenna_pos in enumerate(antennas[:-1]):
            for next_antenna_pos in antennas[antenna_idx + 1:]:
                pos_diff = get_pos_diff(antenna_pos, next_antenna_pos)
                reversed_pos_diff = get_reversed_pos_diff(pos_diff)
                antinode_1 = get_antinode(next_antenna_pos, pos_diff)
                antinode_2 = get_antinode(antenna_pos, reversed_pos_diff)
                if is_on_map(antinode_1):
                    antinodes.add(antinode_1)
                if is_on_map(antinode_2):
                    antinodes.add(antinode_2)
    return len(antinodes)


print("Total unique antinodes count:", part_one())


#
# --- Part Two ---
#
def part_two():
    antinodes: set[tuple[int, int]] = set()
    for antennas in frequencies.values():
        for antenna_idx, antenna_pos in enumerate(antennas[:-1]):
            for next_antenna_pos in antennas[antenna_idx + 1:]:
                pos_diff = get_pos_diff(antenna_pos, next_antenna_pos)
                reversed_pos_diff = get_reversed_pos_diff(pos_diff)
                next_antinodes = [next_antenna_pos]
                while True:
                    next_antinode = get_antinode(next_antinodes[-1], pos_diff)
                    if not is_on_map(next_antinode):
                        break
                    next_antinodes.append(next_antinode)
                prev_antinodes = [antenna_pos]
                while True:
                    prev_antinode = get_antinode(prev_antinodes[-1],
                                                 reversed_pos_diff)
                    if not is_on_map(prev_antinode):
                        break
                    prev_antinodes.append(prev_antinode)
                antinodes.update(next_antinodes, prev_antinodes)
    return len(antinodes)


print("Total unique antinodes count with resonant harmonics:", part_two())
