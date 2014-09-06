#! /usr/bin/python3


# Functions

def Call(command, display = False):
    '''Function for executing console command'''
    from os import system
    if display:
        print(command)
    system(command)
    return

def RandomFileName():
    '''Generate random file name'''
    from random import randrange as RandomRange
    from os import getcwd as GetCurrentWorkingDirectory,\
                   listdir as ListDirectoryContents

    fileNames = ListDirectoryContents(GetCurrentWorkingDirectory())
    while True:
        fileName = '{}'.format(RandomRange(1000))

        if fileName not in fileNames:
            break

    return fileName

def ReadFile(fileName):
    '''Read ascii file'''
    with open(fileName, 'r') as f:
        print('{} >>'.format(fileName))
        return f.read()

def WriteFile(fileName, raw):
    '''Write ascii file'''
    with open(fileName, 'w') as f:
        print('{} <<'.format(fileName))
        f.write(raw)

def WriteMathTex2Png(mathLatexFileName):
    '''Convert math LaTeX to a transparent png file'''
    temporaryFileName = RandomFileName()
    dviFileName, texFileName = ('{}.{}'.format(temporaryFileName, suffix) for suffix in ('dvi', 'tex'))
    pngFileName  = mathLatexFileName.replace('tex', 'png')

    # Write math LaTeX file

    mathLatexRaw = ReadFile(mathLatexFileName)
    mathLatexRaw = r'\documentclass[fleqn]{{article}} \usepackage{{amssymb,amsmath,bm,color}} \usepackage[latin1]{{inputenc}} \begin{{document}} \thispagestyle{{empty}} \mathindent0cm \parindent0cm \begin{{displaymath}} {} \end{{displaymath}} \end{{document}}'.format(mathLatexRaw.strip())
    WriteFile(texFileName, mathLatexRaw)

    # Convert LaTeX to dvi

    Call('latex {} 1> /dev/null'.format(texFileName))

    # Convert dvi to transparent png

    arguments = {\
        'bg' : 'Transparent',\
        'D' : 400,\
        'o' : pngFileName,\
        'q' : None,\
        'Q' : 12,\
        'T' : 'tight',\
        'z' : 5,\
        }
    Call('dvipng {} {}'.format(dviFileName, ' '.join('-{}{}'.format(key, ['', ' {}'.format(value)][bool(value)]) for (key, value) in sorted(arguments.items()))))

    # Remove temporary files

    Call('rm -f {}'.format(' '.join('{}.{}'.format(temporaryFileName, suffix) for suffix in ('aux', 'dvi', 'log', 'tex'))))

    return

# Script

def InterpretArguments():
    '''Initiate argument parser and add custom arguments'''
    from argparse import ArgumentParser
    parser = ArgumentParser(description = 'Script for converting math LaTeX to a transparent png', epilog = 'Version 1.0 | Jeffrey Seifried 2011')
    parser.add_argument('--version', action = 'version', version = '%(prog)s 1.0 | Jeffrey Seifried 2011')

    # LaTeX filename argument

    parser.add_argument('mathLatexFileName', help = 'Math LaTeX input file name')

    return parser.parse_args()

if __name__ == '__main__':

    # Interpret arguments

    args = InterpretArguments()

    # Convert math LaTex to transparent png

    WriteMathTex2Png(args.mathLatexFileName)
