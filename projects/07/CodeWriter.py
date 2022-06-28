import os

class CodeWriter:
    def __init__(self, output):
        self.asm_file = open(output.replace("vm", "asm"), "w")
        self.memory_segments = {"local": "LCL", "argument": "ARG", "this": "THIS", "that": "THAT", "pointer": "3", "temp": "5"}
        self.number_of_comp = 0

    def setFileName(self, file_name):
        self.file_name = str(file_name)

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
                self.asm_file.write("A=M\n")
                self.asm_file.write("M=D\n")
                self.asm_file.write("@SP\n")
                self.asm_file.write("M=M+1\n")
            elif segment == "static":
                self.asm_file.write("@" + self.file_name + "." + str(index) + "\n")
                self.asm_file.write("D=M\n")
                self.asm_file.write("@SP\n")
                self.asm_file.write("A=M\n")
                self.asm_file.write("M=D\n")
                self.asm_file.write("@SP\n")
                self.asm_file.write("M=M+1\n")
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


"""
self.asm_file.write("@SP\n")
self.asm_file.write("M=M-1\n")
self.asm_file.write("A=M\n")
self.asm_file.write("D=M\n")
self.asm_file.write("@SP\n")
self.asm_file.write("M=M-1\n")
self.asm_file.write("A=M\n")
self.asm_file.write("D=D+M\n")
self.asm_file.write("@SP\n")
self.asm_file.write("A=M\n")
self.asm_file.write("M=D\n")
self.asm_file.write("@SP\n")
self.asm_file.write("M=M+1\n")
"""

"""
self.asm_file.write("@" + str(index) + "\n")
self.asm_file.write("D=A\n")
self.asm_file.write("@SP\n")
self.asm_file.write("A=M\n")
self.asm_file.write("M=D\n")
self.asm_file.write("@SP\n")
self.asm_file.write("M=M+1\n")
"""
