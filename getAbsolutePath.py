import os


class pathFinder:
    def __init__(self, path=""):
        self.path = ""
        self.fileName = os.path.splitext(path)[0]
        self.depthPos = []
        self.absoluteFile = open(
            self.fileName+"-absolutePath.txt", mode='w', encoding="utf-8")
        self.originFile = open(self.fileName+os.path.splitext(path)[1],
                               mode='r', encoding="utf-8")

    # following functions may fail if there are special characters  in the file name
    def getFolderDepth(self, line):
        # return max([line.find('├─')//3+1, line.find('└─')//3+1])
        index = max(line.find('├'), line.find('└'))
        return index
    
    def getPureStr(self, line):
        index = 0
        length = len(line)
        curDepth = 0
        skipChar = [' ', '─', '├', '│', '└']
        while(index < length and line[index] in skipChar):
            index += 1
        return line[index:len(line)-1]

    def pathBacktrace(self, n):
        i = len(self.path)-1
        while(n > 0):
            i = self.path.rfind('/', 0, i)
            n -= 1
        self.path = self.path[0:i]

    def wrtieAbsoluteRoute(self, line):
        self.absoluteFile.write(line[0:-1])
        self.absoluteFile.write("  [")
        self.absoluteFile.write(self.path)
        self.absoluteFile.write("]\n")
        # print(line[0:-1], end='')
        # print("  [", end='')
        # print(self.path, end='')
        # print("]\n", end='')

    def run(self):
        lines = self.originFile.readlines()
        count = 1
        purStr = 0
        curDepth = 0
        for line in lines:
            count += 1
            purStr = self.getPureStr(line)
            curDepth = self.getFolderDepth(line)
            if curDepth == -1:  # 非文件夹
                if(self.getPureStr(line)==""):
                    self.absoluteFile.write(line)
                else:
                    self.wrtieAbsoluteRoute(line)
                # print(line, end='')
            else:  # 文件夹
                while(len(self.depthPos) >= 1 and curDepth <= self.depthPos[-1]):
                    # 同级文件夹或上级文件夹
                    self.depthPos.pop()
                    self.pathBacktrace(1)
                self.depthPos.append(curDepth)
                self.path += ('/'+purStr)
                self.wrtieAbsoluteRoute(line)
        self.absoluteFile.close()
        self.originFile.close()

    def test(self):
        self.run()

if __name__ == "__main__":
    pf = pathFinder("本站所有资源一览（一直在更新）.txt")
    # pf = pathFinder("test.txt")
    pf.test()