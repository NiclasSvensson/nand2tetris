class Parser:
    def __init__(self, input_file):
        self.arithmetics = ["add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"]
        if input_file.split(".")[-1] == "vm":
            self.file = open(input_file, "r")
            self.file_names = [input_file.split("/")[-1].split(".")[0]]
        else:
            self.file_names = []
            for file in os.listdir(input):
                if file.split(".")[-1] == "vm":
                    self.file_names.append(file.split("/")[-1].split(".")[0])
        self.lines = self.file.readlines()
        self.commands = []
        for i in range(len(self.lines)):
            instruction = self.lines[i].split("//", 1)[0].strip()
            if instruction != "":
                self.commands.append(instruction)
        self.line_index = 0

    def hasMoreCommands(self):
        if self.line_index <= len(self.commands)-1:
            return True
        else:
            self.line_index = 0
            return False

    def advance(self):
        self.line_index += 1

    def commandType(self):
        command = self.commands[self.line_index].split(" ")
        if command[0] == "pop":
            return "C_POP"
        elif command[0] == "push":
            return "C_PUSH"
        elif command[0] in self.arithmetics:
            return "C_ARITHMETIC"

    def arg1(self):
        command = self.commands[self.line_index].split(" ")
        if len(command) == 1:
            return command[0]
        else:
            return command[1]

    def arg2(self):
        return self.commands[self.line_index].split(" ")[2]
