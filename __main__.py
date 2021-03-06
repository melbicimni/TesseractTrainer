#!/usr/bin/env python

import argparse
import sys
from os.path import exists

import lib.defaults as df
from lib.tesseract_training import TesseractTrainer


def perform_security_checks(args):
    """ Perform several checks on the tesseract training arguments:
        * the {tessdata_path} directorty must exist
        * the {font_path} file must exist
        * the font name must not contain any spaces
        * the font defined by {font_name} must be described in the {font_properties} file
    If any of those tests fail, the execution will stop.
    """
    if not exists(args.tessdata_path):
        print("The %s directory does not exist. Aborting." % (args.tessdata_path))
        sys.exit(1)

    if not exists(args.font_path):
        print("The %s file does not exist. Aborting." % (args.font_path))
        sys.exit(1)

    if " " in args.font_name:
        print("The --font-name / -F argument must not contain any spaces. Aborting.")
        sys.exit(1)

    if args.font_name not in open(args.font_properties, 'r').read().split():
        print("The font properties of %s have not been defined in %s. Aborting." % (args.font_name, args.font_properties))
        sys.exit(1)

if __name__ == '__main__':

    # Parse training arguments
    parser = argparse.ArgumentParser(description='Tesseract training arguments.')
    # Required arguments
    parser.add_argument('--tesseract-lang', '-l', type=str, action='store', required=True,
        help="Set the tesseract language traineddata to create.")
    parser.add_argument('--training-text', '-t', type=str, action='store', required=True,
        help="The path of the training text.")
    parser.add_argument('--font-path', '-F', type=str, action='store', required=True,
        help="The path of TrueType/OpenType file of the used training font.")
    parser.add_argument('--font-name', '-n', type=str, action='store', required=True,
        help="The name of the used training font. No spaces.")
    # Optional arguments
    parser.add_argument('--experience_number', '-e', type=int, action='store', default=df.EXP_NUMBER,
        help="The number of the training experience.")
    parser.add_argument('--font-properties', '-f', type=str, action='store', default=df.FONT_PROPERTIES,
        help="The path of a file containing font properties for a list of training fonts.")
    parser.add_argument('--font-size', '-s', type=int, action='store', default=df.FONT_SIZE,
        help="The font size of the training font, in px.")
    parser.add_argument('--tessdata-path', '-p', type=str, action='store', default=df.TESSDATA_PATH,
        help="The path of the tessdata/ directory on your filesystem.")
    parser.add_argument('--word_list', '-w', type=str, action='store', default=df.WORD_LIST,
        help="The path of a file containing a list of frequent words.")
    parser.add_argument('--verbose', '-v', action='store_true',
        help="Use this argument if you want to display the training output.")
    args = parser.parse_args()

    perform_security_checks(args)  # Check validity of args

    # Training process
    trainer = TesseractTrainer(dictionary_name=args.tesseract_lang,
                                text=args.training_text,
                                font_name=args.font_name,
                                font_path=args.font_path,
                                font_size=args.font_size,
                                exp_number=args.experience_number,
                                font_properties=args.font_properties,
                                tessdata_path=args.tessdata_path,
                                word_list=args.word_list,
                                verbose=args.verbose)
    trainer.training()  # generate a multipage tif from args.training_text, train on it and generate a traineddata file
    trainer.clean()  # remove all files generated in the training process (except the traineddata file)
    trainer.add_trained_data()  # copy the traineddata file to the tessdata/ directory
