class VMWriter:
    def __init__(self, file_name):
        self.file_name = file_name
        self.file = open(file_name, "w")

    def writePush(self, segment, index):
        self.file.write("push " + segment + " " + str(index) + "\n")

    def writePop(self, segment, index):
        self.file.write("pop " + segment + " " + str(index) + "\n")

    def writeArithmetic(self, command):
        if command == "+":
            self.file.write("add\n")
        elif command == "-":
            self.file.write("sub\n")
        elif command == "-":
            self.file.write("neg\n")
        elif command == "=":
            self.file.write("eq\n")
        elif command == "<":
            self.file.write("lt\n")
        elif command == ">":
            self.file.write("gt\n")
        elif command == "&":
            self.file.write("and\n")
        elif command == "|":
            self.file.write("or\n")
        elif command == "~":
            self.file.write("not\n")
        elif command == "*":
            self.file.write("call Math.multiply 2\n")

    def writeLabel(self, label):
        self.file.write("label " + label + "\n")

    def writeGoto(self, label):
        self.file.write("goto " + label + "\n")

    def writeIf(self, label):
        self.file.write("if-goto " + label + "\n")

    def writeCall(self, name, n_args):
        self.file.write("call " + name + " " + str(n_args) + "\n")

    def writeFunction(self, name, n_locals):
        self.file.write("function " + name + " " + str(n_locals) + "\n")

    def writeReturn(self):
        self.file.write("return\n")

    def close(self):
        self.file.close()
