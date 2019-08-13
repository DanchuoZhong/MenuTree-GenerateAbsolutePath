import subprocess
import os
import sys
import codecs
import chardet


class pathGenerator:
    def __init__(self, directory=""):
        self.path = ""
        self.fileName = "MenuTree.txt"
        if(directory[-1] == "\\"):
            self.directory = directory[:-1]
        else:
            self.directory = directory
        self.menuTreePath = self.directory+'/'+self.fileName
        self.depthPos = []
        self.absoluteFile = None  # initialize as None
        self.originFile = None

    def convert_file_to_utf8(self):
        content = codecs.open(self.menuTreePath, 'rb').read()
        source_encoding = chardet.detect(content)['encoding']
        if source_encoding == None:
            print("Failed:Can't detect encoding")
            return False
        else:
            print("Encoding:",source_encoding, self.menuTreePath)
            if source_encoding != 'utf-8':
                # .encode(source_encoding)
                content = content.decode(source_encoding, 'ignore')
                codecs.open(self.menuTreePath, 'w',
                            encoding='utf-8').write(content)
                print("Converte encoding to UTF-8 succeeded")
            return True

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

    def writePaths(self):
        lines = self.originFile.readlines()
        lines.pop(0)
        lines.pop(0)
        purStr = 0
        curDepth = 0
        for line in lines:
            purStr = self.getPureStr(line)
            curDepth = self.getFolderDepth(line)
            if curDepth == -1:  # not a directory
                if(self.getPureStr(line) == ""):
                    self.absoluteFile.write(line)
                else:
                    self.wrtieAbsoluteRoute(line)
            else:  # 文件夹
                while(len(self.depthPos) >= 1 and curDepth <= self.depthPos[-1]):
                    # 同级文件夹或上级文件夹
                    self.depthPos.pop()
                    self.pathBacktrace()
                self.depthPos.append(curDepth)
                self.path += ('/'+purStr)
                self.wrtieAbsoluteRoute(line)

    def run(self):
        # import os
        if os.path.exists(self.directory) == False:
            print("Fail:Path don't exist")
            return -1
        print("Path exist:"+self.directory)
        cmd = ['tree', self.directory, "/f>", self.menuTreePath]
        subprocess.run(cmd, shell=True)
        if self.convert_file_to_utf8() == False:
            return -2
        self.absoluteFile = open(
            self.directory+"/AbsolutePath-"+self.fileName, mode='w', encoding="utf-8")
        self.originFile = open(self.menuTreePath, mode='r', encoding="utf-8")
        print("Generating the menu tree with absolute paths...")
        self.writePaths()
        print("Done")
        self.absoluteFile.close()
        self.originFile.close()
        return 1


if __name__ == "__main__":
    pf = pathGenerator(sys.argv[1])
    pf.run()
