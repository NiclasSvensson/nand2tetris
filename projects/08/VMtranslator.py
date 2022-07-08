import os
import argparse

from Parser import Parser
from CodeWriter import CodeWriter

def main(args):
    parser = Parser(args.vm_path)
    code_writer = CodeWriter(args.vm_path)
    code_writer.writeInit()
    while parser.advanceFile():
        file_name = parser.getFileName()
        code_writer.setFileName(file_name)
        while parser.hasMoreCommands():
            command_type = parser.commandType()
            if command_type == "C_POP" or command_type == "C_PUSH":
                code_writer.writePushPop(command_type, parser.arg1(), parser.arg2())
            elif command_type == "C_ARITHMETIC":
                code_writer.writeArithmetic(parser.arg1())
            elif command_type == "C_LABEL":
                code_writer.writeLabel(parser.arg1())
            elif command_type == "C_GOTO":
                code_writer.writeGoto(parser.arg1())
            elif command_type == "C_IF":
                code_writer.writeIf(parser.arg1())
            elif command_type == "C_FUNCTION":
                code_writer.writeFunction(parser.arg1(), int(parser.arg2()))
            elif command_type == "C_RETURN":
                code_writer.writeReturn()
            elif command_type == "C_CALL":
                code_writer.writeCall(parser.arg1(), int(parser.arg2()))
            parser.advance()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='VM for the Hack platform')
    parser.add_argument('vm_path', help='Path to *.vm file')
    args = parser.parse_args()
    main(args)
