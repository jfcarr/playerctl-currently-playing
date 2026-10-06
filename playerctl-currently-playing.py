#!/usr/bin/env -S uv run -q -s

# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "argparse>=1.4.0",
# ]
# ///

import argparse
import subprocess
from datetime import datetime


def get_value(full_array, position):
    """
    Get value from array.
    """
    return full_array[position].rstrip("\n").strip()


def microseconds_to_mm_ss(microseconds):
    """
    Convert microseconds to formatted string mm:ss
    """
    seconds = microseconds / 1000000
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)

    return (
        f"{int(minutes):02d}:{int(seconds):02d}"
        if hours == 0
        else f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"
    )


def display_info(args):
    """
    Get metadata from playerctl and display results
    """
    try:
        metadata_fields = [
            "{{playerName}}",
            "{{mpris:length}}",
            "{{position}}",
            "{{status}}",
            "{{album}}",
            "{{artist}}",
            "{{xesam:albumArtist}}",
            "{{title}}",
            "{{xesam:title}}",
            "{{rhythmbox:streamTitle}}",
            "{{xesam:contentCreated}}",
            "{{date}}",
        ]

        result = subprocess.run(
            f"playerctl metadata --format '{'~'.join(metadata_fields)}'",
            check=False,
            shell=True,
            capture_output=True,
        )
        standard_output = result.stdout.decode("utf-8").strip()
        standard_error = result.stderr.decode("utf-8").strip()

        if standard_error == "":
            result_items = standard_output.split("~")

            player_name = get_value(result_items, 0)
            length = get_value(result_items, 1)
            position = get_value(result_items, 2)
            status = get_value(result_items, 3)
            album = get_value(result_items, 4)
            artist = get_value(result_items, 5)
            album_artist = get_value(result_items, 6)
            title = get_value(result_items, 7)
            alternate_title = get_value(result_items, 8)
            stream_title = get_value(result_items, 9)
            content_created = get_value(result_items, 10)
            date_info = get_value(result_items, 11)

            # time left
            if (
                length != ""
                and position != ""
                and stream_title == ""
                and args.remaining
            ):
                time_left = int(length) - int(position)
                formatted_time_left = microseconds_to_mm_ss(time_left)
            else:
                formatted_time_left = ""

            # year
            if content_created == "":
                year = "" if date_info == "" else date_info
            else:
                year = datetime.fromisoformat(content_created).year

            message_elements = []
            if title != "":
                message_elements.append(title)
            if stream_title != "":
                message_elements.append(stream_title)
            # if album != '' and album != 'Unknown':
            # message_elements.append(album)

            artist_and_album = ""
            if artist != "" and artist != "Unknown":
                artist_and_album = artist
            else:
                if album_artist != "":
                    artist_and_album = artist
            if artist_and_album != "":
                if album != "" and album != "Unknown" and args.album:
                    artist_and_album = f"{artist_and_album} - {album}"
                message_elements.append(artist_and_album)
            if year != "":
                message_elements.append(str(year))
            if formatted_time_left != "":
                message_elements.append(formatted_time_left)

            output_value = f"{' | '.join(message_elements)}"

            print(output_value)
        else:
            print("Nothing playing")
    except:
        print("Nothing playing (ERR)")


def main():
    parser = argparse.ArgumentParser(
        prog="playerctl-currently-playing",
        description="Display information about the currently playing media",
    )

    parser.add_argument(
        "--album",
        action="store_true",
        default=False,
        help="Show current album name (if available)",
    )

    parser.add_argument(
        "--remaining",
        action="store_true",
        default=False,
        help="Show time remaining for current track",
    )

    args = parser.parse_args()

    display_info(args)


if __name__ == "__main__":
    main()
