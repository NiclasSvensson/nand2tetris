import os

class CodeWriter:
    def __init__(self, output_dir):
        path = output_dir[:-1] if os.path.isdir(output_dir) else os.path.dirname(output_dir)
        self.asm_file = open(os.path.join(path, os.path.basename(path) + ".asm"), "w")
        self.memory_segments = {"local": "LCL", "argument": "ARG", "this": "THIS", "that": "THAT", "pointer": "3", "temp": "5"}
        self.number_of_comp = 0
        self.number_of_call = 0

    def setFileName(self, file_name):
        self.file_name = str(file_name)

    def writeInit(self):
        self.asm_file.write("@256\n")
        self.asm_file.write("D=A\n")
        self.asm_file.write("@SP\n")
        self.asm_file.write("M=D\n")
        self.writeCall("Sys.init", 0)

    def writeArithmetic(self, command):
        self.asm_file.write("@SP\n")
        self.asm_file.write("M=M-1\n")
        self.asm_file.write("A=M\n")
        if command == "neg":
            self.asm_file.write("D=-M\n")
        elif command == "not":
            self.asm_file.write("D=!M\n")
        else:
            self.asm_file.write("D=M\n")
            self.asm_file.write("@SP\n")
            self.asm_file.write("M=M-1\n")
            self.asm_file.write("A=M\n")
            if command == "add":
                self.asm_file.write("D=D+M\n")
            elif command == "and":
                self.asm_file.write("D=D&M\n")
            elif command == "or":
                self.asm_file.write("D=D|M\n")
            else:
                self.asm_file.write("D=M-D\n")
                if command == "sub":
                    pass
                else:
                    label1 = "COMP_" + str(self.number_of_comp)
                    self.number_of_comp += 1
                    self.asm_file.write("@" + label1 + "\n")
                    if command == "eq":
                        self.asm_file.write("D;JEQ\n")
                    elif command == "gt":
                        self.asm_file.write("D;JGT\n")
                    elif command == "lt":
                        self.asm_file.write("D;JLT\n")
                    self.asm_file.write("D=0\n")
                    label2 = "COMP_" + str(self.number_of_comp)
                    self.number_of_comp += 1
                    self.asm_file.write("@" + label2 + "\n")
                    self.asm_file.write("0;JMP\n")
                    self.asm_file.write("(" + label1 + ")\n")
                    self.asm_file.write("D=-1\n")
                    self.asm_file.write("(" + label2 + ")\n")
        self.asm_file.write("@SP\n")
        self.asm_file.write("A=M\n")
        self.asm_file.write("M=D\n")
        self.asm_file.write("@SP\n")
        self.asm_file.write("M=M+1\n")

    def writePushPop(self, command, segment, index):
        if command == "C_POP":
            if segment == "static":
                self.asm_file.write("@SP\n")
                self.asm_file.write("M=M-1\n")
                self.asm_file.write("A=M\n")
                self.asm_file.write("D=M\n")
                self.asm_file.write("@" + self.file_name + "." + str(index) + "\n")
                self.asm_file.write("M=D\n")
            else:
                self.asm_file.write("@" + self.memory_segments[segment] + "\n")
                if segment == "temp" or segment == "pointer":
                    self.asm_file.write("D=A\n")
                else:
                    self.asm_file.write("D=M\n")
                self.asm_file.write("@" + str(index) + "\n")
                self.asm_file.write("D=D+A\n")
                self.asm_file.write("@R15\n")
                self.asm_file.write("M=D\n")
                self.asm_file.write("@SP\n")
                self.asm_file.write("AM=M-1\n")
                self.asm_file.write("D=M\n")
                self.asm_file.write("@R15\n")
                self.asm_file.write("A=M\n")
                self.asm_file.write("M=D\n")
        elif command == "C_PUSH":
            if segment == "constant":
                self.asm_file.write("@" + str(index) + "\n")
                self.asm_file.write("D=A\n")
                self.asm_file.write("@SP\n")
            elif segment == "static":
                self.asm_file.write("@" + self.file_name + "." + str(index) + "\n")
                self.asm_file.write("D=M\n")
                self.asm_file.write("@SP\n")
            else:
                self.asm_file.write("@" + str(index) + "\n")
                self.asm_file.write("D=A\n")
                self.asm_file.write("@" + self.memory_segments[segment] + "\n")
                if segment == "temp" or segment == "pointer":
                    self.asm_file.write("D=D+A\n")
                else:
                    self.asm_file.write("D=D+M\n")
                self.asm_file.write("A=D\n")
                self.asm_file.write("D=M\n")
                self.asm_file.write("@SP\n")
            self.asm_file.write("A=M\n")
            self.asm_file.write("M=D\n")
            self.asm_file.write("@SP\n")
            self.asm_file.write("M=M+1\n")

    def writeLabel(self, label):
        self.asm_file.write("(" + label + ")\n")

    def writeGoto(self, label):
        self.asm_file.write("@" + label + "\n")
        self.asm_file.write("0;JMP\n")

    def writeIf(self, label):
        self.asm_file.write("@SP\n")
        self.asm_file.write("M=M-1\n")
        self.asm_file.write("A=M\n")
        self.asm_file.write("D=M\n")
        self.asm_file.write("@" + label + "\n")
        self.asm_file.write("D;JNE\n")

    def writeCall(self, function_name, num_args):
        label = "RETURN_" + str(self.number_of_call)
        self.asm_file.write("@" + label + "\n")
        self.asm_file.write("D=A\n")
        self.asm_file.write("@SP\n")
        self.asm_file.write("A=M\n")
        self.asm_file.write("M=D\n")
        self.asm_file.write("@SP\n")
        self.asm_file.write("M=M+1\n")

        for seg in ["LCL", "ARG", "THIS", "THAT"]:
            self.asm_file.write("@" + seg + "\n")
            self.asm_file.write("D=M\n")
            self.asm_file.write("@SP\n")
            self.asm_file.write("A=M\n")
            self.asm_file.write("M=D\n")
            self.asm_file.write("@SP\n")
            self.asm_file.write("M=M+1\n")

        self.asm_file.write("@SP\n")
        self.asm_file.write("D=M\n")
        self.asm_file.write("@5\n")
        self.asm_file.write("D=D-A\n")
        self.asm_file.write("@" + str(num_args) + "\n")
        self.asm_file.write("D=D-A\n")
        self.asm_file.write("@ARG\n")
        self.asm_file.write("M=D\n")
        self.asm_file.write("@SP\n")
        self.asm_file.write("D=M\n")
        self.asm_file.write("@LCL\n")
        self.asm_file.write("M=D\n")
        self.writeGoto(function_name)
        self.asm_file.write("(" + label + ")\n")

        self.number_of_call += 1

    def writeReturn(self):
        self.asm_file.write("@LCL\n")
        self.asm_file.write("D=M\n")
        self.asm_file.write("@FRAME\n") #FRAME
        self.asm_file.write("M=D\n")
        self.asm_file.write("@5\n")
        self.asm_file.write("A=D-A\n")
        self.asm_file.write("D=M\n")
        self.asm_file.write("@RET\n") #RET
        self.asm_file.write("M=D\n")

        self.writePushPop("C_POP", "argument", 0)

        self.asm_file.write("@ARG\n")
        self.asm_file.write("D=M\n")
        self.asm_file.write("@SP\n")
        self.asm_file.write("M=D+1\n")

        for seg in ["THAT", "THIS", "ARG", "LCL"]:
            self.asm_file.write("@FRAME\n")
            self.asm_file.write("M=M-1\n")
            self.asm_file.write("A=M\n")
            self.asm_file.write("D=M\n")
            self.asm_file.write("@" + seg + "\n")
            self.asm_file.write("M=D\n")

        self.asm_file.write("@RET\n")
        self.asm_file.write("A=M\n")
        self.asm_file.write("0;JMP\n")

    def writeFunction(self, function_name, num_locals):
        self.asm_file.write("(" + function_name + ")\n")
        for local in range(num_locals):
            self.writePushPop("C_PUSH", "constant", 0)
