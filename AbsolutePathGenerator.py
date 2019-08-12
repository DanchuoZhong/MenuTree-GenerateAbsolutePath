import os
import sys
import codecs
import chardet


class pathGenerator:
    def __init__(self, path):
        self.path = ""
        self.fileName,self.fileExt = os.path.splitext(path)
        # self.fileExt = os.path.splitext(path)[1]
        self.depthPos = []
        self.absoluteFile = None  # initialize as None
        self.originFile = None

    def convert_file_to_utf8(self):
        # !!! does not backup the origin file
        content = codecs.open(self.fileName+self.fileExt, 'rb').read()
        source_encoding = chardet.detect(content)['encoding']
        if source_encoding == None:
            print("Detect Failed", self.fileName)
            return False
        else:
            print("  ", source_encoding, self.fileName)
            if source_encoding != 'utf-8':
                # .encode(source_encoding)
                content = content.decode(source_encoding, 'ignore')
                codecs.open(self.fileName+self.fileExt, 'w',
                            encoding='utf-8').write(content)
            return True

    def openFile(self):
        self.absoluteFile = open(
            self.fileName+"-absolutePath.txt", mode='w', encoding="utf-8")
        self.originFile = open(self.fileName+self.fileExt,
                               mode='r', encoding="utf-8")

    # following functions may fail if there are special characters  in the file name

    def getFolderDepth(self, line):
        return max(line.find('├'), line.find('└'))

    def getPureStr(self, line):
        index = 0
        skipChar = [' ', '─', '├', '│', '└']
        while(index < len(line) and line[index] in skipChar):
            index += 1
        return line[index:len(line)-1]

    def pathBacktrace(self):
        self.path = self.path[0:self.path.rfind('/')]

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
        if self.convert_file_to_utf8() == False:
            return False
        self.openFile()
        lines = self.originFile.readlines()
        count = 1
        purStr = 0
        curDepth = 0
        for line in lines:
            count += 1
            purStr = self.getPureStr(line)
            curDepth = self.getFolderDepth(line)
            if curDepth == -1:  # 非文件夹
                if(self.getPureStr(line) == ""):
                    self.absoluteFile.write(line)
                else:
                    self.wrtieAbsoluteRoute(line)
                    # print(line, end='')
            else:  # 文件夹
                while(len(self.depthPos) >= 1 and curDepth <= self.depthPos[-1]):
                    # 同级文件夹或上级文件夹
                    self.depthPos.pop()
                    self.pathBacktrace()
                self.depthPos.append(curDepth)
                self.path += ('/'+purStr)
                self.wrtieAbsoluteRoute(line)
        self.absoluteFile.close()
        self.originFile.close()
        return True


if __name__ == "__main__":
    pf = pathGenerator(sys.argv[1])
    pf.run()
