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


class FilterBase:
    name = ''
    settings = {}

    def __init__(self, **kwargs):
        self.settings.update(kwargs)

    def __str__(self):
        # generate filter argument string
        return self._make_filter(self.name, self.settings)

    @staticmethod
    def _make_filter(command: str, settings: dict) -> str:
        params = [f'{k}={v}' for k, v in settings.items()]
        return f'{command}={":".join(params)}'


class Compressor(FilterBase):
    name = 'acompressor'
    settings = dict(
        threshold=0.1,
        ratio=2,
        attack=5
    )


class FadeOut(FilterBase):
    name = 'afade'
    settings = dict(
        type='out',
        start_time=1.98,
        duration=0.02
    )


class FilterInstanceError(Exception):
    pass


class FilterGraph:
    def __init__(self, *filters):
        for f in filters:
            if not isinstance(f, FilterBase):
                raise FilterInstanceError('Filter must be subclass instance of FilterBase.')
        self._filters = filters

    def __str__(self):
        # generate filtergraph argument string
        return ','.join([str(f) for f in self._filters])


def create_preview(path):
    """Process audio file with ffmpeg - max duration, add a compressor, and a fade-out."""

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
