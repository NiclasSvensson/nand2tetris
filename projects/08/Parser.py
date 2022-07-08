import os

class Parser:
    def __init__(self, input):
        self.arithmetics = ["add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"]
        self.file_index = -1
        if input.split(".")[-1] == "vm":
            self.dir_path = os.path.dirname(input)
            self.file_names = [input.split("/")[-1].split(".")[0]]
        else:
            self.dir_path = input
            self.file_names = []
            for file in os.listdir(input):
                if file.split(".")[-1] == "vm":
                    self.file_names.append(file.split("/")[-1].split(".")[0])

    def hasMoreCommands(self):
        if self.line_index <= len(self.commands)-1:
            return True
        else:
            self.line_index = 0
            return False

    def advance(self):
        self.line_index += 1

    def advanceFile(self):
        self.file_index += 1
        if self.file_index + 1 > len(self.file_names):
            return False
        else:
            self.file = open(os.path.join(self.dir_path, self.file_names[self.file_index] + ".vm"), "r")
            self.lines = self.file.readlines()
            self.commands = []
            for i in range(len(self.lines)):
                instruction = self.lines[i].split("//", 1)[0].strip()
                if instruction != "":
                    self.commands.append(instruction)
            self.line_index = 0
            return True

    def getFileName(self):
        return self.file_names[self.file_index]

    def commandType(self):
        command = self.commands[self.line_index].split(" ")
        if command[0] == "pop":
            return "C_POP"
        elif command[0] == "push":
            return "C_PUSH"
        elif command[0] in self.arithmetics:
            return "C_ARITHMETIC"
        elif command[0] == "label":
            return "C_LABEL"
        elif command[0] == "goto":
            return "C_GOTO"
        elif command[0] == "if-goto":
            return "C_IF"
        elif command[0] == "function":
            return "C_FUNCTION"
        elif command[0] == "return":
            return "C_RETURN"
        elif command[0] == "call":
            return "C_CALL"

    def arg1(self):
        command = self.commands[self.line_index].split(" ")
        if len(command) == 1:
            return command[0]
        else:
            return command[1]

    def arg2(self):
        return self.commands[self.line_index].split(" ")[2]
