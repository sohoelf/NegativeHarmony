import configparser
#import numpy as np
#from matplotlib import pyplot as plt
#from numpy.core.machar import MachAr
import click
import os
from NegativeModeling import MusicPiece
from MDictionaryLoader import MDictionaryLoader
#defaule config file path
CONFIG_FILE_PATH = 'config_files/setting.conf'

@click.command()
@click.option('--recursive', '-r', '-R', is_flag=True, help='Option to apply each listed directory.')
@click.argument('file_name_path', type=click.Path(exists=True))
@click.option('--mode', '-m', '-M', default='N', help='N | N+ | N+part1 | N+part2 | prepare')
#@click.option('--seed', '-s', '-S', default=0, type=int, help='Integer seed for N+random mode.')
@click.option('--config_section_name', '-c', '-C', default='DEFAULT', help='Config section name.')
def main(recursive, file_name_path, mode, config_section_name):

    #load section in config file and makedir for save_path
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE_PATH)
    config_section = config[config_section_name]
    dirname, filename = os.path.split(file_name_path)
    SAVE_PATH = dirname + config_section['save_path']
    if not os.path.isabs(dirname):
        SAVE_PATH = './'+SAVE_PATH
    os.makedirs(SAVE_PATH, exist_ok=True)

    #organize the PATH of the target file into a list [['~/example/filename.xml','filename']...]
    target_file_path_array = []
    #if it was a directory
    if recursive:
        if os.path.isfile(file_name_path):
            print('Error: file_name_path is not a directory')
            return
        for file in os.listdir(file_name_path):
            if os.path.isfile(os.path.join(file_name_path, file)):
                #file filter from config file like 'xml|mxl|midi'
                if config_section['file_filter'].find(os.path.splitext(file)[-1][1:]) > -1:
                    target_file_path_array.append(
                        [file_name_path+'/'+file, os.path.splitext(file)[0]])
    #if it was only one file
    else:
        if os.path.isdir(file_name_path):
            print(
                'Error: file_name_path is a directory, maybe you should use the -r option')
            return
        target_file_path_array.append([file_name_path, filename])

    #generate musical dictionary through config file and csv files
    mDictionary = MDictionaryLoader(config_section)

    #Loop through all of the target music pieces files
    for item in target_file_path_array:
        music_piece = MusicPiece(item[0])

        if mode == 'N':
            music_piece.NegativePieceByMode_N(mDictionary)
        elif mode == 'N+':
            music_piece.NegativePieceByMode_N_PLUS(mDictionary)
        elif mode == 'N+part1':
            music_piece.NegativePieceByMode_N_PLUS_PART(mDictionary, 'V')
        elif mode == 'N+part2':
            music_piece.NegativePieceByMode_N_PLUS_PART(mDictionary, 'I')
        elif mode == 'prepare':
            music_piece.NegativePreparation(mDictionary)

        music_piece.saveNegativeAsXML(SAVE_PATH + '/' + item[1])

if __name__ == '__main__':
    main()
