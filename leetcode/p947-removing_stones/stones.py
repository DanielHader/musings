
class DisjointForest:
    def __init__(self, n):
        self.elements = [i for i in range(n)]
        self.parents = [i for i in range(n)]
        self.sizes = [1 for _ in range(n)]

    def find(self, x):
        if x != self.parents[x]:
            self.parents[x] = self.find(self.parents[x])
            return self.parents[x]
        else:
            return x

    def union(self, x, y):
        x = self.find(x)
        y = self.find(y)

        if x == y:
            return

        if self.sizes[x] < self.sizes[y]:
            (x, y) = (y, x)

        self.parents[y] = x
        self.sizes[x] += self.sizes[y]

def remove_stones(stones):

    x_coords = set()
    y_coords = set()

    for stone in stones:
        x = stone[0]
        y = stone[1]

        x_coords.add(x)
        y_coords.add(y)
        
    x_coords = sorted(list(x_coords))
    y_coords = sorted(list(y_coords))

    x_indices = {}
    y_indices = {}

    for i,x in enumerate(x_coords):
        x_indices[x] = i

    for i,y in enumerate(y_coords):
        y_indices[y] = i
    
    df = DisjointForest(len(x_coords) + len(y_coords))

    for stone in stones:
        x = stone[0]
        y = stone[1]
        
        df.union(x_indices[x], len(x_coords) + y_indices[y])

    unique_parents = set()
    for i in range(len(df.elements)):
        unique_parents.add(df.find(i))
    
    return len(stones) - len(unique_parents)

def main():

    test_cases = [
        [[0,0],[0,1],[1,0],[1,2],[2,1],[2,2]],
        [[0,0],[0,2],[1,1],[2,0],[2,2]],
        [[0,0]],
        [[0,1],[1,0],[1,1]],
    ]
    
    for test_case in test_cases:
        print(test_case)
        print(remove_stones(test_case))
        print()

if __name__ == "__main__":
    main()
