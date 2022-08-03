class SymbolTable:
    def __init__(self):
        self.static_i = 0
        self.field_i = 0
        self.arg_i = 0
        self.var_i = 0

        self.class_table = {}

    def __str__(self):
        return str(self.class_table) + "\n" + str(self.subroutine_table)

    def startSubroutine(self):
        self.arg_i = 0
        self.var_i = 0
        self.subroutine_table = {}

    def getNumFields(self):
        return self.field_i

    def define(self, name, type, kind):
        if kind == "static":
            self.class_table[name] = [type, kind, self.varCount(kind)]
            self.static_i += 1
        elif kind == "field":
            self.class_table[name] = [type, "this", self.varCount(kind)]
            self.field_i += 1
        elif kind == "argument":
            self.subroutine_table[name] = [type, kind, self.varCount(kind)]
            self.arg_i += 1
        elif kind == "local":
            self.subroutine_table[name] = [type, kind, self.varCount(kind)]
            self.var_i += 1

    def varCount(self, kind):
        if kind == "static":
            return self.static_i
        elif kind == "field":
            return self.field_i
        elif kind == "argument":
            return self.arg_i
        elif kind == "local":
            return self.var_i

    def typeOf(self, name):
        return self.class_table[name][0] if name in self.class_table else self.subroutine_table[name][0]

    def kindOf(self, name):
        return self.class_table[name][1] if name in self.class_table else self.subroutine_table[name][1]

    def indexOf(self, name):
        return self.class_table[name][2] if name in self.class_table else self.subroutine_table[name][2]

    def __contains__(self, name):
        return (name in self.class_table) or (name in self.subroutine_table)
