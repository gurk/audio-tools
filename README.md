# audio-tools
Library and scripts for processing audio files, based on FFmpeg.

Requires Python 3.6+, no dependencies.

Initial sketch provisions for ease of filter and filtergraph creation.

```
from ffmpeg_py import FilterGraph, Compressor, FadeOut

# filtergraph [compressor -> fade out]

filters = FilterGraph(
    Compressor(ratio=8),
    FadeOut()
)
```
