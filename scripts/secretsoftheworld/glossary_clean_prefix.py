from typing import List
import json

# Common Japanese Particles and Suffixes
particles_and_suffixes = [
    "の", "を", "に", "と", "へ", "で", "から", "まで", "も", "や", "だ", "です",
    "か", "けど", "けれど", "へん", "とき", "たち", "な", "ら", "ちゃん", "さ"
]

# Common Kanji Components
kanji_components = [
    "人", "大", "小", "生", "力", "日", "水", "火", "木", "金", "土", "天"
]


prefixes = [
    "大",  # Great, large (e.g., 大輔 - Daisuke)
    "小",  # Small (e.g., 小泉 - Koizumi)
    "佐",  # Used in many names (e.g., 佐藤 - Sato)
    "宮",  # Palace, temple (e.g., 宮本 - Miyamoto)
    "長",  # Long (e.g., 長谷川 - Hasegawa)
    "松",  # Pine tree (e.g., 松本 - Matsumoto)
    "藤",  # Wisteria (e.g., 藤原 - Fujiwara)
    "田",  # Rice field (e.g., 田中 - Tanaka)
    "山",  # Mountain (e.g., 山田 - Yamada)
    "川",  # River (e.g., 川口 - Kawaguchi)
    "石",  # Stone (e.g., 石田 - Ishida)
    "木",  # Tree (e.g., 木村 - Kimura)
    "野",  # Field (e.g., 野口 - Noguchi)
    "村",  # Village (e.g., 村上 - Murakami)
    "島",  # Island (e.g., 島田 - Shimada)
    "井",  # Well (e.g., 井上 - Inoue)
    "川",  # River (e.g., 川崎 - Kawasaki)
    "井",  # Well (e.g., 井口 - Iguchi)
]

suffixes = [
    "子",  # Child (common in female names, e.g., 美子 - Yoshiko)
    "郎",  # Son (common in male names, e.g., 太郎 - Taro)
    "さん",  # Honorific (e.g., 佐藤さん - Sato-san)
    "様",  # Honorific (e.g., 山田様 - Yamada-sama)
    "ちゃん",  # Informal diminutive (e.g., 花ちゃん - Hana-chan)
    "君",  # Used for males or in a respectful tone (e.g., 一郎君 - Ichiro-kun)
    "夫",  # Husband (e.g., 佐藤夫 - Sato-fu)
    "妻",  # Wife (e.g., 田中妻 - Tanaka-tsuma)
    "介",  # Used in male names (e.g., 俊介 - Shunsuke)
    "美",  # Beautiful (e.g., 美智子 - Michiko)
    "恵",  # Blessing, grace (e.g., 恵子 - Keiko)
    "貴",  # Noble, precious (e.g., 貴子 - Takako)
    "雄",  # Male, masculine (e.g., 雄太 - Yuta)
    "子",  # Child, used for females (e.g., 小川子 - Ogawako)
    "佳",  # Good, beautiful (e.g., 佳子 - Yoshiko)
]



class Node:

    def __init__(self, char='', parent=None, terminal=False):
        self.char = char
        self.children = []
        self.parent = parent
        self.terminal = terminal 
        self.ignore = False

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
    
    def insert(self, str, ignore=False):
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
        curNode.ignore = ignore

with open('glossary_unprocessed.json', 'r') as f:
    glossary = json.load(f)

trie = Trie()
for word in glossary:
    trie.insert(word)
for word in suffixes:
    trie.insert(word, ignore=True)
for word in prefixes:
    trie.insert(word, ignore=True)
for word in particles_and_suffixes:
    trie.insert(word, ignore=True)
for word in kanji_components:
    trie.insert(word, ignore=True)


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
                if not node.ignore:
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