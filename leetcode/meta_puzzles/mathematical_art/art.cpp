#include <bits/stdc++.h>
using namespace std;

struct BoundingBox {
    int x_min, x_max, y_min, y_max;

    BoundingBox(int x_min=0, int x_max=0, int y_min=0, int y_max=0)
        : x_min(x_min), x_max(x_max), y_min(y_min), y_max(y_max) {}

    int width() const { return this->x_max - this->x_min + 1; }
    int height() const { return this->y_max - this->y_min + 1; }
    bool contains(int x, int y) const { return x <= x_max and x >= x_min and y <= y_max and y >= y_min; }
};

struct Line {
    int x_min, x_max, y_min, y_max;
    
    bool is_vertical() const { return x_min == x_max; }
    bool is_horizontal() const { return y_min == y_max; }
};

struct DirArr {
    array<bool, 4> data;
    DirArr() : data{0} {}

    bool &operator[] (int d) { return data[d]; }
};

int plusSignCountDivideAndConquer(const BoundingBox bbox, const vector<Line> &h_lines, const vector<Line> &v_lines) {
    const int NORTH = 0;
    const int EAST  = 1;
    const int SOUTH = 2;
    const int WEST  = 3;
    
    const int THRESHOLD = 10;

    //std::cout << bbox.width() << " " << bbox.height() << std::endl;
    if (bbox.width() < THRESHOLD and bbox.height() < THRESHOLD) {
        // explicit search
        //std::cout << "beginning explicit search" << std::endl;
        
        bool plus_directions[bbox.width()][bbox.height()][4];
        memset(plus_directions, 0, sizeof(plus_directions));

        //std::cout << "iterating over lines" << std::endl;

        for (auto line : h_lines) {
            int y = line.y_min;
            int y_idx = y - bbox.y_min;
                
            for (int x=line.x_min; x <= line.x_max; x++) {
                int x_idx = x - bbox.x_min;
                    
                if (!bbox.contains(x, y)) continue;
                if (x > line.x_min)
                    plus_directions[x_idx][y_idx][WEST] = true;
                if (x < line.x_max)
                    plus_directions[x_idx][y_idx][EAST] = true;
            }
        }
        for (auto line : v_lines) {
            int x = line.x_min;
            int x_idx = x - bbox.x_min;
                
            for (int y=line.y_min; y <= line.y_max; y++) {
                int y_idx = y - bbox.y_min;
                    
                if (!bbox.contains(x, y)) continue;
                if (y > line.y_min)
                    plus_directions[x_idx][y_idx][SOUTH] = true;
                if (y < line.y_max)
                    plus_directions[x_idx][y_idx][NORTH] = true;
            }

        }

        int pluses = 0;
        for (int y = bbox.y_min; y <= bbox.y_max; y++) {
            int y_idx = y - bbox.y_min;
            
            for (int x = bbox.x_min; x <= bbox.x_max; x++) {
                int x_idx = x - bbox.x_min;
                
                bool found_plus = true;
                for (int d = 0; d < 4; d++) {
                    if (!plus_directions[x_idx][y_idx][d]) {
                        found_plus = false;
                        break;
                    }
                }
                if (found_plus) pluses++;
            }
        }

        return pluses;
        
    } else {
        //std::cout << "beginning divide and conquer" << std::endl;
        
        // divide and conquer
        bool split_horizontally = bbox.width() > bbox.height();
        
        BoundingBox bboxA, bboxB;
        vector<Line> h_linesA, v_linesA, h_linesB, v_linesB;
        unordered_map<int, DirArr> split_axis_plus_directions;

        //cout << "DIVIDE AND CONQUER" << std::endl;
        //cout << "  BBOX " << bbox.x_min << " - " << bbox.x_max << " : " << bbox.y_min << " - " << bbox.y_max << std::endl;
        
        if (split_horizontally) {
            int x_half = (bbox.x_max + bbox.x_min) / 2;
            bboxA = BoundingBox(bbox.x_min, x_half-1, bbox.y_min, bbox.y_max);
            bboxB = BoundingBox(x_half+1, bbox.x_max, bbox.y_min, bbox.y_max);

            //std::cout << "  splitting horizontally at x=" << x_half << std::endl;
            
            for (auto line : h_lines) {
                if (line.x_min < x_half and line.x_max > x_half) {
                    // split line in 2
                    h_linesA.insert(h_linesA.end(), { line.x_min, x_half, line.y_min, line.y_min });
                    h_linesB.insert(h_linesB.end(), { x_half, line.x_max, line.y_min, line.y_min });
                        
                    split_axis_plus_directions[line.y_min][EAST] = true;
                    split_axis_plus_directions[line.y_min][WEST] = true;
                        
                } else if (line.x_max <= x_half) {

                    h_linesA.insert(h_linesA.end(), {line.x_min, line.x_max, line.y_min, line.y_min});
                    if (line.x_max == x_half) split_axis_plus_directions[line.y_min][WEST] = true;
                            
                } else if (line.x_min >= x_half) {

                    h_linesB.insert(h_linesB.end(), {line.x_min, line.x_max, line.y_min, line.y_min});
                    if (line.x_min == x_half) split_axis_plus_directions[line.y_min][EAST] = true;
                }
            }
            for (auto line : v_lines) {
                if (line.x_min < x_half) v_linesA.push_back(line);
                else if (line.x_min > x_half) v_linesB.push_back(line);
                else {
                    for (auto it = split_axis_plus_directions.begin(); it != split_axis_plus_directions.end(); ++it) {
                        auto y = it->first;
                        auto &dirs = it->second;
                        if (line.y_min <= y and line.y_max > y) dirs[NORTH] = true;
                        if (line.y_max >= y and line.y_min < y) dirs[SOUTH] = true;
                    }
                }
            }
            
        } else {

            int y_half = (bbox.y_max + bbox.y_min) / 2;
            bboxA = BoundingBox(bbox.x_min, bbox.x_max, bbox.y_min, y_half-1);
            bboxB = BoundingBox(bbox.x_min, bbox.x_max, y_half+1, bbox.y_max);

            for (auto line : v_lines) {
                if (line.y_min < y_half and line.y_max > y_half) {
                    // split line in 2
                    v_linesA.insert(v_linesA.end(), { line.x_min, line.x_min, line.y_min, y_half });
                    v_linesB.insert(v_linesB.end(), { line.x_min, line.x_min, y_half, line.y_max });

                    split_axis_plus_directions[line.x_min][NORTH] = true;
                    split_axis_plus_directions[line.x_min][SOUTH] = true;
                        
                } else if (line.y_max <= y_half) {

                    v_linesA.insert(v_linesA.end(), {line.x_min, line.x_min, line.y_min, line.y_max});
                    if (line.y_max == y_half) split_axis_plus_directions[line.x_min][SOUTH] = true;
                            
                } else if (line.y_min >= y_half) {

                    v_linesB.insert(v_linesB.end(), {line.x_min, line.x_min, line.y_min, line.y_max});
                    if (line.y_min == y_half) split_axis_plus_directions[line.x_min][NORTH] = true;
                }
            }
            for (auto line : h_lines) {
                if (line.y_min < y_half) h_linesA.push_back(line);
                else if (line.y_min > y_half) h_linesB.push_back(line);
                else {
                    for (auto it = split_axis_plus_directions.begin(); it != split_axis_plus_directions.end(); ++it) {
                        auto x = it->first;
                        auto &dirs = it->second;
                        if (line.x_min <= x and line.x_max > x) dirs[EAST] = true;
                        if (line.x_max >= x and line.x_min < x) dirs[WEST] = true;
                    }
                }
            }
        }

        int pluses = 0;
        for (auto it = split_axis_plus_directions.begin(); it != split_axis_plus_directions.end(); ++it) {
            auto xy = it->first;
            auto &dirs = it->second;

            //std::cout << " ! xy = " << xy << " dirs = " << dirs[0] << dirs[1] << dirs[2] << dirs[3] << std::endl;
            
            bool found_plus = true;
            for (int d = 0; d < 4; d++) {
                if (!dirs[d]) {
                    found_plus = false;
                    break;
                }
            }
            if (found_plus) pluses++;
        }

        //std::cout << "FOUND " << pluses << " PLUSES" << std::endl;

        int plusesA = plusSignCountDivideAndConquer(bboxA, h_linesA, v_linesA);
        int plusesB = plusSignCountDivideAndConquer(bboxB, h_linesB, v_linesB);

        return pluses + plusesA + plusesB;
    }
}

int getPlusSignCount(int N, vector<int> L, string D) {
    
    BoundingBox bbox;
    vector<Line> h_lines, v_lines;

    int x = 0, y = 0;
    for (int i = 0; i < L.size(); i++) {
        int len = L[i];
        char dir = D[i];

        switch (dir) {
        case 'U':
            v_lines.insert(v_lines.end(), { x, x, y, y+len });
            y += len;
            break;
        case 'D':
            v_lines.insert(v_lines.end(), { x, x, y-len, y });
            y -= len;
            break;
        case 'L':
            h_lines.insert(h_lines.end(), { x-len, x, y, y});
            x -= len;
            break;
        case 'R':
            h_lines.insert(h_lines.end(), { x, x+len, y, y});
            x += len;
            break;
        default:
            throw runtime_error("invalid direction");
        };

        if (x < bbox.x_min) { bbox.x_min = x; }
        if (x > bbox.x_max) { bbox.x_max = x; }
        if (y < bbox.y_min) { bbox.y_min = y; }
        if (y > bbox.y_max) { bbox.y_max = y; }
    }

    return plusSignCountDivideAndConquer(bbox, h_lines, v_lines);
}

struct TestCase {
    int N;
    vector<int> L;
    string D;
    int ans;
};

int main(int argc, char** argv) {
    vector<TestCase> cases = {
        { 9, {6, 3, 4, 5, 1, 6, 3, 3, 4}, "ULDRULURD", 4 },
        { 8, {1, 1, 1, 1, 1, 1, 1, 1}, "RDLUULDR", 1 },
        { 8, {1, 2, 2, 1, 1, 2, 2, 1}, "UDUDLRLR", 1 },
    };

    for (int i = 0; i < cases.size(); i++) {
        TestCase tc = cases[i];
        int res = getPlusSignCount(tc.N, tc.L, tc.D);
        if (res == tc.ans) {
            cout << "TEST CASE " << i << " PASSED" << endl;
        } else {
            cout << "TEST CASE " << i << " FAILED (GOT " << res << " EXPECTED " << tc.ans << ")" << endl;
        }
    }
}
