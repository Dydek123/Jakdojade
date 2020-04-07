import collections

queue = []
visited = []
previous = []

class Graph:
    # Constructor
    def __init__(self):

        # default dictionary to store graph
        self.graph = collections.defaultdict(dict)

    # function to add an edge to graph
    def addEdge(self, u, v):
        x = []
        elementy = self.graph.get(u)
        if elementy == None:
            x.append(v)
        else:
            for i in elementy:
                x.append(i)
            x.append(v)
        self.graph[u] = x
        # self.graph=collections.OrderedDict(sorted(self.graph.items()))
        # print(self.graph)

    # Function to print a BFS of graph
    def bfs(self, node):
        x = []
        s = 0
        visited.append(node)
        queue.append(node)
        while queue:
            z = s
            s = queue.pop(0)
            print(s, end=" ")
            x.append([s, z])
            z += 1
            for neighbour in self.graph[s]:
                if neighbour not in visited:
                    visited.append(neighbour)
                    queue.append(neighbour)
        return x

    def bfs2(self, node, queue, visited):
        x = []
        visited=[]
        s = 0
        visited.append(node)
        queue.append(node)
        ile = 1
        a = 0
        b = 0
        j = 0
        c = []
        while queue:
            for i in range(ile):
                s = queue.pop(0)
                print(s, end=" ")
                x.append([s, b])
                for neighbour in self.graph[s]:
                    if neighbour not in visited:
                        visited.append(neighbour)
                        queue.append(neighbour)
                        a += 1
                c.append(a)
                a = 0
            ile = c.pop(0)
            b = x[j][0]
            j += 1
            if queue == []:
                break
        return x

    def najkrotsza(self, droga, poczatek, koniec):
        droga.reverse()
        # print(droga)
        a=poczatek
        b=koniec
        x = []
        z = []
        for j in range (0,1):
            x=[]
            poczatek=a
            koniec=b
            while True:
                for i in droga:
                    if i[0] == koniec:
                        x.append(i[0])
                        break
                    elif i[1] == 0:
                        return [-1,0]
                koniec = i[1]
                if koniec == poczatek:
                    x.append(koniec)
                    break
            z.append(x)
        droga.reverse()
        return z

g = Graph()
g.addEdge(84, 90)
g.addEdge(90, 84)
g.addEdge(90, 67)
g.addEdge(90, 3069)
g.addEdge(3069, 90)
g.addEdge(67, 90)
g.addEdge(67, 68)
g.addEdge(68, 67)
g.addEdge(68, 71)
g.addEdge(71, 68)
g.addEdge(3069, 57)
g.addEdge(57, 3069)
g.addEdge(3069, 60)
g.addEdge(60, 3069)
g.addEdge(60, 2601)
g.addEdge(2601, 60)
g.addEdge(2601, 63)
g.addEdge(63, 2601)
g.addEdge(57, 56)
g.addEdge(56, 57)
g.addEdge(56, 55)
g.addEdge(56, 1)
g.addEdge(1, 56)
g.addEdge(1, 62)
g.addEdge(62, 1)
g.addEdge(62, 63)
g.addEdge(63, 62)
g.addEdge(55, 56)

aa = []
bb = []
z=[]
x = g.bfs2(84, aa, bb)
print("\n",x)
print(x)
naj = g.najkrotsza(x, 84, 999)
print(naj)
z=naj[0]
# z.reverse()
print(z)
