"""Helpers/utilities to parse ID3 tags from audio files with ffmpeg."""
from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any, Dict, Optional, Tuple, Union

from requests import JSONDecodeError

from music_assistant.constants import UNKNOWN_ARTIST
from music_assistant.helpers.process import AsyncProcess
from music_assistant.helpers.util import try_parse_int
from music_assistant.models.errors import InvalidDataError

# the only multi-item splitter we accept is the semicolon,
# which is also the default in Musicbrainz Picard.
# the slash is also a common splitter but causes colissions with
# artists actually containing a slash in the name, such as ACDC
TAG_SPLITTER = ";"


def split_items(org_str: str) -> Tuple[str]:
    """Split up a tags string by common splitter."""
    if not org_str:
        return tuple()
    if isinstance(org_str, list):
        return org_str
    return tuple(x.strip() for x in org_str.split(TAG_SPLITTER))


def split_artists(org_artists: Union[str, Tuple[str]]) -> Tuple[str]:
    """Parse all artists from a string."""
    final_artists = set()
    # when not using the multi artist tag, the artist string may contain
    # multiple artistsin freeform, even featuring artists may be included in this
    # string. Try to parse the featuring artists and seperate them.
    splitters = ("featuring", " feat. ", " feat ", "feat.")
    for item in split_items(org_artists):
        for splitter in splitters:
            for subitem in item.split(splitter):
                final_artists.add(subitem.strip())
    return tuple(final_artists)


@dataclass
class AudioTags:
    """Audio metadata parsed from an audio file."""

    raw: Dict[str, Any]
    sample_rate: int
    channels: int
    bits_per_sample: int
    format: str
    bit_rate: int
    duration: Optional[int]
    tags: Dict[str, str]
    has_cover_image: bool
    filename: str

    @property
    def title(self) -> str:
        """Return title tag (as-is)."""
        if tag := self.tags.get("title"):
            return tag
        # fallback to parsing from filename
        title = self.filename.rsplit(os.sep, 1)[-1].split(".")[0]
        if " - " in title:
            title_parts = title.split(" - ")
            if len(title_parts) >= 2:
                return title_parts[1].strip()
        return title

    @property
    def album(self) -> str:
        """Return album tag (as-is) if present."""
        return self.tags.get("album")

    @property
    def artists(self) -> Tuple[str]:
        """Return track artists."""
        # prefer multi-artist tag
        if tag := self.tags.get("artists"):
            return split_items(tag)
        # fallback to regular artist string
        if tag := self.tags.get("artist"):
            if ";" in tag:
                return split_items(tag)
            return split_artists(tag)
        # fallback to parsing from filename
        title = self.filename.rsplit(os.sep, 1)[-1].split(".")[0]
        if " - " in title:
            title_parts = title.split(" - ")
            if len(title_parts) >= 2:
                return split_artists(title_parts[0])
        return (UNKNOWN_ARTIST,)

    @property
    def album_artists(self) -> Tuple[str]:
        """Return (all) album artists (if any)."""
        # prefer multi-artist tag
        if tag := self.tags.get("albumartists"):
            return split_items(tag)
        # fallback to regular artist string
        if tag := self.tags.get("albumartist"):
            if ";" in tag:
                return split_items(tag)
            return split_artists(tag)
        return tuple()

    @property
    def genres(self) -> Tuple[str]:
        """Return (all) genres, if any."""
        return split_items(self.tags.get("genre"))

    @property
    def disc(self) -> int | None:
        """Return disc tag if present."""
        if tag := self.tags.get("disc"):
            return try_parse_int(tag.split("/")[0], None)
        return None

    @property
    def track(self) -> int | None:
        """Return track tag if present."""
        if tag := self.tags.get("track"):
            return try_parse_int(tag.split("/")[0], None)
        return None

    @property
    def year(self) -> int | None:
        """Return album's year if present, parsed from date."""
        if tag := self.tags.get("originalyear"):
            return try_parse_int(tag.split("-")[0], None)
        if tag := self.tags.get("originaldate"):
            return try_parse_int(tag.split("-")[0], None)
        if tag := self.tags.get("date"):
            return try_parse_int(tag.split("-")[0], None)
        return None

    @property
    def musicbrainz_artistids(self) -> Tuple[str]:
        """Return musicbrainz_artistid tag(s) if present."""
        return split_items(self.tags.get("musicbrainzartistid"))

    @property
    def musicbrainz_albumartistids(self) -> Tuple[str]:
        """Return musicbrainz_albumartistid tag if present."""
        return split_items(self.tags.get("musicbrainzalbumartistid"))

    @property
    def musicbrainz_releasegroupid(self) -> str | None:
        """Return musicbrainz_releasegroupid tag if present."""
        return self.tags.get("musicbrainzreleasegroupid")

    @property
    def musicbrainz_trackid(self) -> str | None:
        """Return musicbrainz_trackid tag if present."""
        if tag := self.tags.get("musicbrainztrackid"):
            return tag
        return self.tags.get("musicbrainzreleasetrackid")

    @property
    def album_type(self) -> str | None:
        """Return albumtype tag if present."""
        if tag := self.tags.get("musicbrainzalbumtype"):
            return tag
        return self.tags.get("releasetype")

    @classmethod
    def parse(cls, raw: dict) -> "AudioTags":
        """Parse instance from raw ffmpeg info output."""
        audio_stream = next(x for x in raw["streams"] if x["codec_type"] == "audio")
        has_cover_image = any(
            x for x in raw["streams"] if x["codec_name"] in ("mjpeg", "png")
        )
        # convert all tag-keys (gathered from all streams) to lowercase without spaces
        tags = {}
        for stream in raw["streams"] + [raw["format"]]:
            for key, value in stream.get("tags", {}).items():
                key = key.lower().replace(" ", "").replace("_", "")
                tags[key] = value

        return AudioTags(
            raw=raw,
            sample_rate=int(audio_stream.get("sample_rate", 44100)),
            channels=audio_stream.get("channels", 2),
            bits_per_sample=int(
                audio_stream.get(
                    "bits_per_raw_sample", audio_stream.get("bits_per_sample")
                )
                or 16
            ),
            format=raw["format"]["format_name"],
            bit_rate=int(raw["format"].get("bit_rate", 320)),
            duration=int(float(raw["format"].get("duration", 0))) or None,
            tags=tags,
            has_cover_image=has_cover_image,
            filename=raw["format"]["filename"],
        )

    def get(self, key: str, default=None) -> Any:
        """Get tag by key."""
        return self.tags.get(key, default)


async def parse_tags(file_path: str) -> AudioTags:
    """Parse tags from a media file."""

    args = (
        "ffprobe",
        "-hide_banner",
        "-loglevel",
        "fatal",
        "-show_error",
        "-show_format",
        "-show_streams",
        "-print_format",
        "json",
        "-i",
        file_path,
    )

    async with AsyncProcess(
        args, enable_stdin=False, enable_stdout=True, enable_stderr=False
    ) as proc:

        try:
            res, _ = await proc.communicate()
            data = json.loads(res)
            if error := data.get("error"):
                raise InvalidDataError(error["string"])
            return AudioTags.parse(data)
        except (KeyError, ValueError, JSONDecodeError, InvalidDataError) as err:
            raise InvalidDataError(
                f"Unable to retrieve info for {file_path}: {str(err)}"
            ) from err


async def get_embedded_image(file_path: str) -> bytes | None:
    """Return embedded image data."""
    args = (
        "ffmpeg",
        "-hide_banner",
        "-loglevel",
        "fatal",
        "-i",
        file_path,
        "-map",
        "0:v",
        "-c",
        "copy",
        "-f",
        "mjpeg",
        "-",
    )

    async with AsyncProcess(
        args, enable_stdin=False, enable_stdout=True, enable_stderr=False
    ) as proc:

        res, _ = await proc.communicate()
        return res
