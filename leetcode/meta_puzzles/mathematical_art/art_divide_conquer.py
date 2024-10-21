from typing import List, Union, Optional
from dataclasses import dataclass

@dataclass()
class BoundingBox:
    x_min: int = 0
    x_max: int = 0
    y_min: int = 0
    y_max: int = 0

    def width(self) -> int:
        return self.x_max - self.x_min + 1

    def height(self) -> int:
        return self.y_max - self.y_min + 1
    
    def contains(self, x: int, y: int) -> bool:
        return x >= self.x_min and x <= self.x_max and y >= self.y_min and y <= self.y_max

@dataclass(frozen=True)
class Point:
    x: int
    y: int
    
Line = Union['HorizontalLine','VerticalLine']

@dataclass(frozen=True)
class HorizontalLine:
    x_min: int
    x_max: int
    y: int

    def length(self) -> int:
        return self.x_max - self.x_min + 1
    
@dataclass(frozen=True)
class VerticalLine:
    y_min: int
    y_max: int
    x: int

    def length(self) -> int:
        return self.y_max - self.y_min + 1

def plusSignCountDivideAndConquer(bbox: BoundingBox, h_lines: List[HorizontalLine], v_lines: List[VerticalLine]) -> int:
    NORTH = 0
    EAST  = 1
    SOUTH = 2
    WEST  = 3
    DIVIDE_AND_CONQUER_THRESHOLD = 1
    if bbox.width() < DIVIDE_AND_CONQUER_THRESHOLD and bbox.height() < DIVIDE_AND_CONQUER_THRESHOLD:
        
        plus_directions = {}
        for x in range(bbox.x_min, bbox.x_max + 1):
            for y in range(bbox.y_min, bbox.y_max + 1):
                plus_directions[x,y] = { NORTH: False, EAST: False, SOUTH: False, WEST: False }

        for h_line in h_lines:
            y = h_line.y
            for i, x in enumerate(range(h_line.x_min, h_line.x_max + 1)):
                if not bbox.contains(x,y):
                    continue
                if i > 0:
                    plus_directions[x,y][WEST] = True
                if i < h_line.length() - 1:
                    plus_directions[x,y][EAST] = True

        for v_line in v_lines:
            x = v_line.x
            for i, y in enumerate(range(v_line.y_min, v_line.y_max + 1)):
                if not bbox.contains(x,y):
                    continue
                if i > 0:
                    plus_directions[x,y][SOUTH] = True
                if i < v_line.length() - 1:
                    plus_directions[x,y][NORTH] = True

        pluses = 0
        for x in range(bbox.x_min, bbox.x_max + 1):
            for y in range(bbox.y_min, bbox.y_max + 1):
                found_plus = True
                for d in [NORTH, EAST, SOUTH, WEST]:
                    if plus_directions[x,y][d] is False:
                        found_plus = False
                        break
                if found_plus:
                    pluses += 1
                    
        return pluses

    # split lines into resepctive bounding boxes
    h_linesA = []
    v_linesA = []

    h_linesB = []
    v_linesB = []

    split_axis_pluses = 0
    
    # keeps track of which points along the split axis contain lines in which directions
    # used for finding pluses on the split axis
    split_axis_line_dirs: Dict[int, Dict[int, bool]] = {}
    
    # for wide bboxes, split vertically along the middle
    # create bounding boxes for each side, not including the split axis
    if bbox.width() > bbox.height():
        # vertical split axis
        x_half = (bbox.x_max + bbox.x_min) // 2
        bboxA = BoundingBox(x_min=bbox.x_min, x_max=x_half-1, y_min=bbox.y_min, y_max=bbox.y_max)
        bboxB = BoundingBox(x_min=x_half+1, x_max=bbox.x_max, y_min=bbox.y_min, y_max=bbox.y_max)

        for h_line in h_lines:
            if h_line.x_min < x_half and h_line.x_max > x_half:
                # split the horizontal line in 2
                h_lineA = HorizontalLine(x_min=h_line.x_min, x_max=x_half, y=h_line.y)
                h_lineB = HorizontalLine(x_min=x_half, x_max=h_line.x_max, y=h_line.y)
                h_linesA.append(h_lineA)
                h_linesB.append(h_lineB)

                if h_line.y not in split_axis_line_dirs:
                    split_axis_line_dirs[h_line.y] = { NORTH: False, EAST: False, SOUTH: False, WEST: False }
                    
                split_axis_line_dirs[h_line.y][EAST] = True
                split_axis_line_dirs[h_line.y][WEST] = True
                
            elif h_line.x_max <= x_half:
                # h_line before the split axis
                h_lineA = HorizontalLine(x_min=h_line.x_min, x_max=h_line.x_max, y=h_line.y)
                h_linesA.append(h_lineA)

                if h_line.x_max == x_half:
                    if h_line.y not in split_axis_line_dirs:
                        split_axis_line_dirs[h_line.y] = { NORTH: False, EAST: False, SOUTH: False, WEST: False }
                    split_axis_line_dirs[h_line.y][WEST] = True
                
            elif h_line.x_min >= x_half:
                # h_line after the split axis
                h_lineB = HorizontalLine(x_min=h_line.x_min, x_max=h_line.x_max, y=h_line.y)
                h_linesB.append(h_lineB)

                if h_line.x_min == x_half:
                    if h_line.y not in split_axis_line_dirs:
                        split_axis_line_dirs[h_line.y] = { NORTH: False, EAST: False, SOUTH: False, WEST: False }
                    split_axis_line_dirs[h_line.y][EAST] = True

        for v_line in v_lines:
            if v_line.x < x_half:
                v_linesA.append(v_line)
            elif v_line.x > x_half:
                v_linesB.append(v_line)
            else:
                for y in split_axis_line_dirs:
                    if v_line.y_min <= y and v_line.y_max > y: 
                        split_axis_line_dirs[y][NORTH] = True
                    if v_line.y_max >= y and v_line.y_min < y:
                        split_axis_line_dirs[y][SOUTH] = True
    else:
        # horizontal split axis
        y_half = (bbox.y_max + bbox.y_min) // 2
        bboxA = BoundingBox(x_min=bbox.x_min, x_max=bbox.x_max, y_min=bbox.y_min, y_max=y_half-1)
        bboxB = BoundingBox(x_min=bbox.x_min, x_max=bbox.x_max, y_min=y_half+1, y_max=bbox.y_max)

        for v_line in v_lines:
            if v_line.y_min < y_half and v_line.y_max > y_half:
                v_lineA = VerticalLine(y_min=v_line.y_min, y_max=y_half, x=v_line.x)
                v_lineB = VerticalLine(y_min=y_half, y_max=v_line.y_max, x=v_line.x)
                v_linesA.append(v_lineA)
                v_linesB.append(v_lineB)

                if v_line.x not in split_axis_line_dirs:
                    split_axis_line_dirs[v_line.x] = { NORTH: False, EAST: False, SOUTH: False, WEST: False }
                    
                split_axis_line_dirs[v_line.x][NORTH] = True
                split_axis_line_dirs[v_line.x][SOUTH] = True
                
            elif v_line.y_max <= y_half:
                v_lineA = VerticalLine(y_min=v_line.y_min, y_max=v_line.y_max, x=v_line.x)
                v_linesA.append(v_lineA)

                if v_line.y_max == y_half:
                    if v_line.x not in split_axis_line_dirs:
                        split_axis_line_dirs[v_line.x] = { NORTH: False, EAST: False, SOUTH: False, WEST: False }
                    split_axis_line_dirs[v_line.x][SOUTH] = True
                
            elif v_line.y_min >= y_half:
                v_lineB = VerticalLine(y_min=v_line.y_min, y_max=v_line.y_max, x=v_line.x)
                v_linesB.append(v_lineB)

                if v_line.y_min == y_half:
                    if v_line.x not in split_axis_line_dirs:
                        split_axis_line_dirs[v_line.x] = { NORTH: False, EAST: False, SOUTH: False, WEST: False }
                    split_axis_line_dirs[v_line.x][NORTH] = True

        for h_line in h_lines:
            if h_line.y < y_half:
                h_linesA.append(h_line)
            elif h_line.y > y_half:
                h_linesB.append(h_line)
            else:
                for x in split_axis_line_dirs:
                    if h_line.x_min <= x and h_line.x_max > x: 
                        split_axis_line_dirs[x][EAST] = True
                    if h_line.x_max >= x and h_line.x_min < x:
                        split_axis_line_dirs[x][WEST] = True

    # reconstruct pluses on the split axis
    for xy in split_axis_line_dirs:
        found_plus = True
        for d in [NORTH, EAST, SOUTH, WEST]:
            if split_axis_line_dirs[xy][d] is False:
                found_plus = False
                break
        if found_plus:
            split_axis_pluses += 1

    plusesA = plusSignCountDivideAndConquer(bboxA, h_linesA, v_linesA)
    plusesB = plusSignCountDivideAndConquer(bboxB, h_linesB, v_linesB)
    return split_axis_pluses + plusesA + plusesB

def getPlusSignCount(N: int, L: List[int], D: str) -> int:
    # pre-process path into separate lines and calculate bounding box

    bbox = BoundingBox()
    
    h_lines = []
    v_lines = []
    
    x, y = 0, 0
    for length, direction in zip(L, D):
        if direction == 'U':
            ny = y + length
            v_lines.append(VerticalLine(y_min=y, y_max=ny, x=x))
            y = ny
        elif direction == 'D':
            ny = y - length
            v_lines.append(VerticalLine(y_min=ny, y_max=y, x=x))
            y = ny
        elif direction == 'L':
            nx = x - length
            h_lines.append(HorizontalLine(x_min=nx, x_max=x, y=y))
            x = nx
        elif direction == 'R':
            nx = x + length
            h_lines.append(HorizontalLine(x_min=x, x_max=nx, y=y))
            x = nx
        else:
            raise RuntimeError(f'invalid direction "{direction}"')
        
        if x < bbox.x_min:
            bbox.x_min = x
        if x > bbox.x_max:
            bbox.x_max = x

        if y < bbox.y_min:
            bbox.y_min = y
        if y > bbox.y_max:
            bbox.y_max = y

    return plusSignCountDivideAndConquer(bbox, h_lines, v_lines)

def main():
    test_cases = [
        (9, [6, 3, 4, 5, 1, 6, 3, 3, 4], 'ULDRULURD'),
        (8, [1, 1, 1, 1, 1, 1, 1, 1], 'RDLUULDR'),
        (8, [1, 2, 2, 1, 1, 2, 2, 1], 'UDUDLRLR'),
    ]

    answers = [ 4, 1, 1 ]

    for i, (tc, ans) in enumerate(zip(test_cases, answers)):
        res = getPlusSignCount(*tc)
        if res == ans:
            print(f'TEST CASE {i} PASSED')
        else:
            print(f'TEST CASE {i} FAILED (GOT {res}, EXPECTED {ans})')

if __name__ == "__main__":
    main()
