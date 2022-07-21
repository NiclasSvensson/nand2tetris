import os
import re

class JackTokenizer:
    def __init__(self, input_dir):
        self.keywords = ("class", "constructor", "function", "method", "field", "static", "var",
                         "int", "char", "boolean", "void", "true", "false", "null", "this", "let",
                         "do", "if", "else", "while", "return")
        self.symbols = ("{", "}", "(", ")", "[", "]", ".", ",", ";", "+", "-", "*", "*", "/", "&",
                        "|", "<", ">", "=", "~")
        self.input_dir = input_dir
        self.file_names = []
        for file in os.listdir(input_dir):
            if file.split(".")[-1] == "jack":
                self.file_names.append(file.split("/")[-1].split(".")[0])
        self.file_index = -1

    def advanceFile(self):
        self.tokens = []
        self.file_index += 1
        if self.file_index + 1 > len(self.file_names):
            return False
        else:
            self.file = open(os.path.join(self.input_dir, self.file_names[self.file_index] + ".jack"), "r")
            string = ""
            lines = self.file.readlines()
            # Remove comments
            for line in lines:
                code = line.split("//", 1)[0].strip()
                if code == "":
                    continue
                else:
                    string += code
            string = re.sub(re.compile("/\*.*?\*/", re.DOTALL), "", string)
            self.string = string
            # Target file
            self.write_file = open(os.path.join(self.input_dir, self.file_names[self.file_index] + "T_my.xml"), "w")
            self.write_file.write("<tokens>\n")
            return True

    def getFileName(self):
        return self.file_names[self.file_index]

    def hasMoreTokens(self):
        if len(self.string) == 0:
            return False
        else:
            return True

    def tokenType(self):
        self.string = self.string.strip()
        if self.string.startswith(self.keywords):
            return "KEYWORD"
        elif self.string.startswith(self.symbols):
            return "SYMBOL"
        elif self.string.startswith("\""):
            return "STRING_CONST"
        elif self.string[0].isdigit():
            return "INT_CONST"
        else:
            return "IDENTIFIER"

    def keyWord(self):
        for keyword in self.keywords:
            if self.string.startswith(keyword):
                self.string = self.string.replace(keyword, "", 1)
                self.writeToXML(keyword, "keyword")
                return keyword

    def symbol(self):
        for symbol in self.symbols:
            if self.string.startswith(symbol):
                self.string = self.string.replace(symbol, "", 1)
                self.writeToXML(symbol, "symbol")
                return symbol

    def identifier(self):
        for char in self.string:
            if (char in self.symbols) or (char == " "):
                identifier = self.string.split(char)[0]
                self.string = self.string.replace(identifier, "", 1)
                self.writeToXML(identifier, "identifier")
                return identifier

    def intVal(self):
        for char in self.string:
            if not char.isdigit():
                val = self.string.split(char)[0]
                self.string = self.string.replace(val, "", 1)
                self.writeToXML(val, "integerConstant")
                return val

    def stringVal(self):
        val = self.string.split("\"")[1]
        self.string = self.string.replace("\"" + val + "\"", "", 1)
        self.writeToXML(val, "stringConstant")
        return val

    def writeToXML(self, symbol, type):
        symbol = "&lt;" if symbol == "<" else symbol
        symbol = "&gt;" if symbol == ">" else symbol
        symbol = "&amp;" if symbol == "&" else symbol
        self.write_file.write("<" + type + "> " + symbol + " </" + type + ">\n")

    def close(self):
        self.write_file.write("</tokens>")
        self.write_file.close()
