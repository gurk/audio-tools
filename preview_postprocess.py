#!/usr/bin/env python3
import argparse
import glob
import os
import subprocess

__author__      = "Graeme Urquhart"
__version__     = "0.1.0"
__description__ = "Audio file preview generator (ffmpeg)"


def main(cli_args):
    # process specified files
    for path in cli_args.paths:
        create_preview(path)

    # if no files specified, recursively find aif files and process them
    if not cli_args.paths:
        for path in glob.iglob('./**/*.aif', recursive=True):
            create_preview(path)


# compressor - filter settings (ffmpeg)
def compressor(threshold=0.1, ratio=2, attack=5):
    return f'acompressor=threshold={threshold}:ratio={ratio}:attack={attack}'


# fade out - filter settings (ffmpeg)
def fade_out(start=1.98, duration=0.02):
    return f'afade=out:st={start}:d={duration}'


def create_preview(path):
    """Process audio file with ffmpeg - max duration, add a compressor, and a fade-out."""

    # build .ogg output file path
    input_path, _ = os.path.splitext(path)
    output_path   = f'{input_path}.ogg'

    # ffmpeg command + args
    command = ['/usr/local/bin/ffmpeg',                # ffmpeg executable
               '-i', path,                             # input file
               '-ss', '0', '-t', '2',                  # max duration 2s
               '-af', f'{compressor()},{fade_out()}',  # filtergraph - [compressor -> fade_out]
               '-c:a', 'libvorbis',                    # convert to ogg, with libvorbis codec
               output_path]

    subprocess.run(args=command)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__description__)

    # Specify argument for input file paths
    parser.add_argument("paths", nargs="*", help="Audio files to be processed")

    # Specify output of "--version"
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s (version {__version__})"
    )

    main(cli_args=parser.parse_args())
