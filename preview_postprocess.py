#!/usr/bin/env python3
import argparse
import glob
import os
import subprocess

from ffmpeg_py import FilterGraph, Compressor, FadeOut


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


def create_preview(path):
    """Create 2 second preview from input audio file, add compressor, fade-out, and convert to ogg format."""

    # build .ogg output file path
    path_no_ext, _ = os.path.splitext(path)
    output_path    = f'{path_no_ext}.ogg'

    filters = FilterGraph(
        Compressor(ratio=8),
        FadeOut()
    )

    # [ffmpeg binary, *arguments, output path]
    command = ['/usr/local/bin/ffmpeg',                # ffmpeg executable
               '-i', path,                             # input file
               '-ss', '0', '-t', '2',                  # max duration 2s
               '-af', f'{filters}',                    # audio filtergraph
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
