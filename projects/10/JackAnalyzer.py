import os
import argparse

from JackTokenizer import JackTokenizer
from CompilationEngine import CompilationEngine

def main(args):
    tokenizer = JackTokenizer(args.jack_path)
    while tokenizer.advanceFile():
        input_stream = []
        while tokenizer.hasMoreTokens():
            token_type = tokenizer.tokenType()
            if token_type == "KEYWORD":
                input_stream.append((tokenizer.keyWord(), "keyword"))
            elif token_type == "SYMBOL":
                input_stream.append((tokenizer.symbol(), "symbol"))
            elif token_type == "IDENTIFIER":
                input_stream.append((tokenizer.identifier(), "identifier"))
            elif token_type == "INT_CONST":
                input_stream.append((tokenizer.intVal(), "integerConstant"))
            elif token_type == "STRING_CONST":
                input_stream.append((tokenizer.stringVal(), "stringConstant"))
        compilation_engine = CompilationEngine(input_stream, os.path.join(args.jack_path, tokenizer.getFileName() + "_my.xml"))
        #print(input_stream)
        compilation_engine.compileClass()
        tokenizer.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Compiler for the jack language')
    parser.add_argument('jack_path', help='Path to *.jack file(s)')
    args = parser.parse_args()
    main(args)
