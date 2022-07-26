class VMWriter:
    def __init__(self, file_name):
        self.file_name = file_name
        self.file = open(file_name, "w")

    def writePush(self):
        pass

    def writePop(self):
        pass

    def writeArithmetic(self):
        pass

    def writeLabel(self):
        pass

    def writeGoto(self):
        pass

    def writeIf(self):
        pass

    def writeCall(self):
        pass

    def writeFunction(self):
        pass

    def writeReturn(self):
        pass

    def close(self):
        self.file.close()
