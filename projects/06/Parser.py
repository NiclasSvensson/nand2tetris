from Code import Code

class Parser:
    def __init__(self, input_file):
        self.file = open(input_file, "r")
        self.lines = self.file.readlines()
        self.commands = []
        for i in range(len(self.lines)):
            instruction = self.lines[i].split("//", 1)[0].strip()
            if instruction != "":
                self.commands.append(instruction.replace(" ", ""))
        self.line_index = 0
        self.code = Code()

    def hasMoreCommands(self):
        if self.line_index <= len(self.commands)-1:
            return True
        else:
            self.line_index = 0
            return False

    def advance(self):
        self.line_index += 1

    def commandType(self):
        if self.commands[self.line_index][0] == "@":
            return "A_COMMAND"
        elif self.commands[self.line_index][0] == "(" and self.commands[self.line_index][-1] == ")":
            return "L_COMMAND"
        else:
            return "C_COMMAND"

    def symbol(self):
        sym = self.commands[self.line_index]
        if self.commandType() == "A_COMMAND":
            return sym[1:]
        if self.commandType() == "L_COMMAND":
            return sym[sym.find("(")+1:sym.find(")")]

    def dest(self):
        command = self.commands[self.line_index]
        if "=" in command:
            components = command.split("=")
            return self.code.dest(components[0])
        else:
            return "000"

    def comp(self):
        command = self.commands[self.line_index]
        if "=" in command:
            operation = command.split("=")[1]
            return self.code.comp(operation)
        if ";" in command:
            operation = command.split(";")[0]
            return self.code.comp(operation)

    def jump(self):
        command = self.commands[self.line_index]
        if ";" in command:
            components = command.split(";")
            return self.code.jump(components[1])
        else:
            return "000"
