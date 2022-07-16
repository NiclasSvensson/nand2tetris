import os
import argparse

from JackTokenizer import JackTokenizer
from CompilationEngine import CompilationEngine

def main(args):
    tokenizer = JackTokenizer(args.jack_path)
    compilation_engine = CompilationEngine()
    while tokenizer.advanceFile():
        input_stream = []
        tokenizer.write_file.write("<tokens>\n")
        while tokenizer.hasMoreTokens():
            token_type = tokenizer.tokenType()
            if token_type == "KEYWORD":
                #nput_stream.append(tokenizer.keyWord())
                tokenizer.writeToXML(tokenizer.keyWord(), "keyword")
            elif token_type == "SYMBOL":
                #input_stream.append(tokenizer.symbol())
                tokenizer.writeToXML(tokenizer.symbol(), "symbol")
            elif token_type == "IDENTIFIER":
                #input_stream.append(tokenizer.identifier())
                tokenizer.writeToXML(tokenizer.identifier(), "identifier")
            elif token_type == "INT_CONST":
                #input_stream.append(tokenizer.intVal())
                tokenizer.writeToXML(tokenizer.intVal(), "integerConstant")
            elif token_type == "STRING_CONST":
                #input_stream.append(tokenizer.stringVal())
                tokenizer.writeToXML(tokenizer.stringVal(), "stringConstant")
        tokenizer.write_file.write("</tokens>")
        #print(input_stream)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Compiler for the jack language')
    parser.add_argument('jack_path', help='Path to *.jack file(s)')
    args = parser.parse_args()
    main(args)
