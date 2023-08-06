from __future__ import annotations

import json
import os
import sys
from fractions import Fraction
from typing import Any

from auto_editor.ffwrapper import FFmpeg, FileInfo
from auto_editor.objs.export import ExJson, ExTimeline
from auto_editor.objs.util import ParserError, parse_dataclass
from auto_editor.timeline import Visual, audio_objects, v3, visual_objects
from auto_editor.utils.log import Log

"""
Make a pre-edited file reference that can be inputted back into auto-editor.
"""


def check_attrs(data: object, log: Log, *attrs: str) -> None:
    if not isinstance(data, dict):
        log.error("Data is in wrong shape!")
    for attr in attrs:
        if attr not in data:
            log.error(f"'{attr}' attribute not found!")


def check_file(path: str, log: Log) -> None:
    if not os.path.isfile(path):
        log.error(f"Could not locate media file: '{path}'")


class Version:
    __slots__ = ("major", "minor", "micro")

    def __init__(self, val: str, log: Log) -> None:
        if val.startswith("unstable:"):
            val = val[9:]

        ver_str = val.split(".")
        if len(ver_str) > 3:
            log.error("Version string: Too many separators!")
        while len(ver_str) < 3:
            ver_str.append("0")

        try:
            self.major, self.minor, self.micro = map(int, ver_str)
        except ValueError:
            log.error("Version string: Could not convert to int.")

    def __eq__(self, other: object) -> bool:
        if isinstance(other, tuple) and len(other) == 2:
            return (self.major, self.minor) == other
        return (self.major, self.minor, self.micro) == other

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.micro}"


def read_json(path: str, ffmpeg: FFmpeg, log: Log) -> v3:
    with open(path) as f:
        data = json.load(f)

    check_attrs(data, log, "version")
    version = Version(data["version"], log)

    if version == (3, 0):
        check_attrs(data, log, "timeline")
        tl = data["timeline"]
        check_attrs(
            tl,
            log,
            "sources",
            "background",
            "v",
            "a",
            "timebase",
            "resolution",
            "samplerate",
        )

        sources: dict[str, FileInfo] = {}
        for _id, path in tl["sources"].items():
            check_file(path, log)
            sources[_id] = FileInfo(path, ffmpeg, log)

        bg = tl["background"]
        sr = tl["samplerate"]
        res = (tl["resolution"][0], tl["resolution"][1])
        tb = Fraction(tl["timebase"])

        v: Any = []
        a: Any = []

        def dict_to_args(d: dict) -> str:
            attrs = []
            for k, v in d.items():
                if k != "name":
                    attrs.append(f"{k}={v}")
            return ",".join(attrs)

        for vlayers in tl["v"]:
            if vlayers:
                v_out: list[Visual] = []
                for vdict in vlayers:
                    if "name" not in vdict:
                        log.error("Invalid video object: name not specified")
                    if vdict["name"] not in visual_objects:
                        log.error(f"Unknown video object: {vdict['name']}")
                    my_obj = visual_objects[vdict["name"]]
                    text = dict_to_args(vdict)
                    try:
                        v_out.append(parse_dataclass(text, my_obj, coerce_default=True))
                    except ParserError as e:
                        log.error(e)

                v.append(v_out)

        for alayers in tl["a"]:
            if alayers:
                a_out = []
                for adict in alayers:
                    if "name" not in adict:
                        log.error("Invalid audio object: name not specified")
                    if adict["name"] not in audio_objects:
                        log.error(f"Unknown audio object: {adict['name']}")
                    my_obj = audio_objects[adict["name"]]
                    text = dict_to_args(adict)
                    try:
                        a_out.append(parse_dataclass(text, my_obj, coerce_default=True))
                    except ParserError as e:
                        log.error(e)

                a.append(a_out)

        return v3(sources, tb, sr, res, bg, v, a, None)

    log.error(f"Importing version {version} timelines is not supported.")


def make_json_timeline(
    obj: ExJson | ExTimeline,
    out: str | int,
    tl: object,
    log: Log,
) -> None:

    if (version := Version(obj.api, log)) != (3, 0):
        log.error(f"Version {version} is not supported!")

    if not isinstance(tl, v3):
        raise ValueError("Wrong tl object!")

    if isinstance(out, str):
        if not out.endswith(".json"):
            log.error("Output extension must be .json")
        outfile: Any = open(out, "w")
    else:
        outfile = sys.stdout

    json.dump(tl.as_dict(), outfile, indent=2, default=lambda o: o.__dict__)

    if isinstance(out, str):
        outfile.close()
    else:
        print("")  # Flush stdout
