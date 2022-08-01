from SymbolTable import SymbolTable
from VMWriter import VMWriter

class CompilationEngine:
    def __init__(self, input_stream, file_name):
        self.stream = input_stream
        self.index = 0
        self.file = open(file_name  + "_my.xml", "w")
        self.indent = "  "
        self.subroutines = ["constructor", "function", "method"]
        self.types = ["int", "char", "boolean"]
        self.statements = ["let", "do", "return", "if", "while"]
        self.terms = ["integerConstant", "stringConstant"]
        self.operations = ["+", "-", "*", "*", "/", "&", "|", "<", ">", "="]
        self.unary_operations = ["~", "-"]
        self.keyword_constants = ["true", "false", "null", "this"]
        self.symbol_table = SymbolTable()
        self.vm_writer = VMWriter(file_name  + "_my.vm")

    def compileClass(self):
        indent = 0
        self.writeTag("class", False, indent)
        self.class_name = self.stream[self.index+1][0]
        self.advance(3, indent)
        while self.stream[self.index][0] == "static" or self.stream[self.index][0] == "field":
            self.compileClassVarDec(indent+1)
        while self.stream[self.index][0] in self.subroutines:
            self.compileSubroutine(indent+1)
        self.advance(1, indent)
        self.writeTag("class", True, indent)

    def compileClassVarDec(self, indent):
        self.writeTag("classVarDec", False, indent)
        kind = self.stream[self.index][0]
        type = self.stream[self.index+1][0]
        self.advance(2, indent)
        while self.stream[self.index][1] == "identifier":
            self.symbol_table.define(self.stream[self.index][0], type, kind)
            self.advance(2, indent)
        self.writeTag("classVarDec", True, indent)

    def compileSubroutine(self, indent):
        self.writeTag("subroutineDec", False, indent)
        self.symbol_table.startSubroutine()
        self.return_type = self.stream[self.index+1][0]
        function_name = self.stream[self.index+2][0]
        self.advance(4, indent)
        self.compileParameterList(indent+1)
        self.advance(1, indent)
        self.writeTag("subroutineBody", False, indent+1)
        self.advance(1, indent+1)
        while self.stream[self.index][0] == "var":
            self.compileVarDec(indent+1)
        self.vm_writer.writeFunction(self.class_name + "." + function_name, self.symbol_table.varCount("var"))
        self.compileStatements(indent+1)
        self.advance(1, indent+1)
        #print(self.symbol_table)
        self.writeTag("subroutineBody", True, indent+1)
        self.writeTag("subroutineDec", True, indent)

    def compileParameterList(self, indent):
        self.writeTag("parameterList", False, indent)
        while self.stream[self.index][0] in self.types or self.stream[self.index][1] == "identifier":
            self.symbol_table.define(self.stream[self.index + 1][0], self.stream[self.index][0], "arg")
            self.advance(2, indent)
            if self.stream[self.index][0] == ",":
                self.advance(1, indent)
        self.writeTag("parameterList", True, indent)

    def compileVarDec(self, indent):
        self.writeTag("varDec", False, indent+1)
        kind = self.stream[self.index][0]
        type = self.stream[self.index+1][0]
        self.advance(2, indent+1)
        while self.stream[self.index][1] == "identifier":
            self.symbol_table.define(self.stream[self.index][0], type, kind)
            self.advance(2, indent+1)
        self.writeTag("varDec", True, indent+1)

    def compileStatements(self, indent):
        self.writeTag("statements", False, indent+1)
        while self.stream[self.index][0] in self.statements:
            if self.stream[self.index][0] == "let":
                self.compileLet(indent+1)
            elif self.stream[self.index][0] == "do":
                self.compileDo(indent+1)
            elif self.stream[self.index][0] == "return":
                self.compileReturn(indent+1)
            elif self.stream[self.index][0] == "if":
                self.compileIf(indent+1)
            elif self.stream[self.index][0] == "while":
                self.compileWhile(indent+1)
        self.writeTag("statements", True, indent+1)

    def compileDo(self, indent):
        self.writeTag("doStatement", False, indent+1)
        if self.stream[self.index+2][0] == ".":
            name = self.stream[self.index+1][0]+"."+self.stream[self.index+3][0]
            self.advance(5, indent+1)
        else:
            name = self.class_name+"."+self.stream[self.index+1][0]
            self.advance(3, indent+1)
        args = self.compileExpressionList(indent+1);
        self.vm_writer.writeCall(name, args)
        if self.return_type == "void":
            self.vm_writer.writePop("temp", 0)
        self.advance(2, indent+1)
        self.writeTag("doStatement", True, indent+1)

    def compileLet(self, indent):
        self.writeTag("letStatement", False, indent+1)
        self.advance(2, indent+1)
        if self.stream[self.index][0] == "[":
            self.advance(1, indent+1)
            self.compileExpression(indent+1)
            self.advance(1, indent+1)
        self.advance(1, indent+1)
        self.compileExpression(indent+1)
        self.advance(1, indent+1)
        self.writeTag("letStatement", True, indent+1)

    def compileWhile(self, indent):
        self.writeTag("whileStatement", False, indent+1)
        self.advance(2, indent+1)
        self.compileExpression(indent+1)
        self.advance(2, indent+1)
        self.compileStatements(indent+1)
        self.advance(1, indent+1)
        self.writeTag("whileStatement", True, indent+1)

    def compileReturn(self, indent):
        self.writeTag("returnStatement", False, indent+1)
        self.advance(1, indent+1)
        if self.stream[self.index][0] != ";":
            self.compileExpression(indent+1)
        self.advance(1, indent+1)
        if self.return_type == "void":
            self.vm_writer.writePush("constant", 0)
        self.vm_writer.writeReturn()
        self.writeTag("returnStatement", True, indent+1)

    def compileIf(self, indent):
        self.writeTag("ifStatement", False, indent+1)
        self.advance(2, indent+1)
        self.compileExpression(indent+1)
        self.advance(2, indent+1)
        self.compileStatements(indent+1)
        self.advance(1, indent+1)
        if self.stream[self.index][0] == "else":
            self.advance(2, indent+1)
            self.compileStatements(indent+1)
            self.advance(1, indent+1)
        self.writeTag("ifStatement", True, indent+1)

    def compileExpression(self, indent):
        self.writeTag("expression", False, indent+1)
        cnt = 0
        op = None
        while True:
            self.compileTerm(indent+1)
            if op is not None:
                self.vm_writer.writeArithmetic(op)
            if self.stream[self.index][0] in self.operations:
                op = self.stream[self.index][0]
                self.advance(1, indent+1)
            else:
                break
            cnt += 1
        self.writeTag("expression", True, indent+1)

    def compileTerm(self, indent):
        self.writeTag("term", False, indent+1)
        if (self.stream[self.index][1] in self.terms) or (self.stream[self.index][0] in self.keyword_constants):
            if self.stream[self.index][1] == "integerConstant":
                self.vm_writer.writePush("constant", self.stream[self.index][0])
            self.advance(1, indent+1)
        elif self.stream[self.index][1] == "identifier":
            self.advance(1, indent+1)
            if self.stream[self.index][0] == "[":
                self.advance(1, indent+1)
                self.compileExpression(indent+1)
                self.advance(1, indent+1)
            elif self.stream[self.index][0] == "(":
                self.advance(1, indent+1)
                self.compileExpressionList(indent+1)
                self.advance(1, indent+1)
            elif self.stream[self.index][0] == ".":
                self.advance(3, indent+1)
                self.compileExpressionList(indent+1)
                self.advance(1, indent+1)
        elif self.stream[self.index][0] in self.unary_operations:
            op = self.stream[self.index][0]
            self.advance(1, indent+1)
            self.compileTerm(indent+1)
            self.writeArithmetic(op)
        elif self.stream[self.index][0] == "(":
            self.advance(1, indent+1)
            self.compileExpression(indent+1)
            self.advance(1, indent+1)
        self.writeTag("term", True, indent+1)

    def compileExpressionList(self, indent):
        self.writeTag("expressionList", False, indent+1)
        cnt = 0
        if self.stream[self.index][0] != ")":
            cnt += 1
            while True:
                self.compileExpression(indent+1)
                if self.stream[self.index][0] == ",":
                    cnt += 1
                    self.advance(1, indent+1)
                else:
                    break
        self.writeTag("expressionList", True, indent+1)
        return cnt

    def advance(self, increment, indent):
        for i in range(increment):
            self.writeTerminal(self.stream[self.index][0], self.stream[self.index][1], indent + 1)
            self.index += 1

    def writeTerminal(self, symbol, type, indent):
        symbol = "&lt;" if symbol == "<" else symbol
        symbol = "&gt;" if symbol == ">" else symbol
        symbol = "&amp;" if symbol == "&" else symbol
        self.file.write(self.indent*indent + "<" + type + "> " + symbol + " </" + type + ">\n")

    def writeTag(self, word, end, indent):
        self.file.write(self.indent*indent + ("<" + word + ">\n" if not end else "</" + word + ">\n"))
