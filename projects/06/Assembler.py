import os
import argparse

from SymbolTable import SymbolTable

from Parser import Parser

def main(args):
    symbol_table = SymbolTable()
    output_file = open(os.path.join(args.target_path, "Prog.hack"), "w")
    parser = Parser(args.asm_path)
    # First pass
    ROM_address = 0
    while parser.hasMoreCommands():
        command_type = parser.commandType()
        if command_type == "A_COMMAND":
            ROM_address +=1
            symbol = parser.symbol()
        if command_type == "C_COMMAND":
            ROM_address +=1
        if command_type == "L_COMMAND":
            symbol = parser.symbol()
            symbol_table.addEntry(symbol, ROM_address)
        parser.advance()
    # Second pass
    RAM_address = 16
    while parser.hasMoreCommands():
        command_type = parser.commandType()
        if command_type == "A_COMMAND":
            symbol = parser.symbol()
            if symbol.isdigit():
                code = symbol
            else:
                if symbol_table.contains(symbol):
                    code = symbol_table.getAdress(symbol)
                else:
                    symbol_table.addEntry(symbol, RAM_address)
                    RAM_address += 1
                    code = symbol_table.getAdress(symbol)
            code = bin(int(code)).split("0b")[-1].zfill(16)
        if command_type == "C_COMMAND":
            code = "111" + parser.comp() + parser.dest() + parser.jump()
        if command_type == "L_COMMAND":
            parser.advance()
            continue
        output_file.write(code + "\n")
        parser.advance()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Assembler for the Hack platform')
    parser.add_argument('asm_path', help='Path to *.asm file')
    parser.add_argument('--target_path', default="", help='Path to the generated *.hack file')
    args = parser.parse_args()
    main(args)
