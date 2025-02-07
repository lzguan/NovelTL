from typing import List
import json

class Node:

    def __init__(self, char='', parent=None, terminal=False):
        self.char = char
        self.children = []
        self.parent = parent
        self.terminal = False

    def findChild(self, char):
        for child in self.children:
            if child.char == char:
                return child
        return False

class Trie:

    def __init__(self):
        self.root = Node()
    
    def contains(self, str):
        curNode = self.root
        for char in str:
            ex = False
            for child in curNode.children:
                if char == child.char:
                    curNode = child
                    ex = True
                    break
            if not ex:
                return False
        if curNode.terminal:
            return True
        return False
    
    def insert(self, str):
        curNode = self.root
        for char in str:
            ex = False
            for child in curNode.children:
                if char == child.char:
                    curNode = child
                    ex = True
                    break
            if not ex:
                newChild = Node(char=char, parent=curNode)
                curNode.children.append(newChild)
                curNode = newChild
        curNode.terminal = True

with open('glossary_unprocessed.json', 'r') as f:
    glossary = json.load(f)

trie = Trie()
for word in glossary:
    trie.insert(word)

def search(trie : Trie, node : Node, ridlist : set, possibilities : list[Node], path):
    path = path + node.char
    npossibilites = []
    addterm = False
    for p in possibilities:
        np = p.findChild(node.char)
        if np:
            npossibilites.append(np)
            if np.terminal:
                addterm = True
    if addterm:
        npossibilites.append(trie.root)
    if node.terminal:
        for i in range(1, len(npossibilites)):
            if npossibilites[i].terminal:
                ridlist.add(path)
                break
    for child in node.children:
        search(trie, child, ridlist, npossibilites, path)
    if len(path) >= 1:
        path = path[:-1]

def rootsearch(trie : Trie, ridlist : set):
    for child in trie.root.children:
        search(trie, child, ridlist, [trie.root], "")

ridlist = set()
rootsearch(trie, ridlist)
print(ridlist)
print(len(ridlist))
print(len(glossary))


# t = Trie()
# t.insert("fjfj")
# t.insert("fjfjfjfjf")
# t.insert("fttwe")
# t.insert("uuufeiw")
# t.insert("uewafa")
# print(t.contains("fjfj"))
# print(t.contains("fjfjfjfjf"))
# print(t.contains("fttwe"))
# print(t.contains("uuufeiw"))
# print(t.contains("uewafa"))
# print(t.contains("fjfjfj"))
# print(t.contains("iiiewaf"))
# print(t.contains("i"))
# print(t.contains("uu"))
# print([x.char for x in t.root.children])