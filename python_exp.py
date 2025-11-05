#!/usr/bin/env python3
"""
Pairwise video quality comparison with Psychtoolbox (Python).

Each trial presents two videos: one REFERENCE and one TEST.
- The order of Video 1 and Video 2 is randomized per trial.
- Participant must watch BOTH videos fully once (in that randomized order) before they can make a choice.
- After the initial full viewing, they can switch between the two videos (restarting playback) to compare.
- They then select which video has BETTER quality.
- Results are appended to a CSV log.

Controls (after initial full viewing):
  [SPACE]  -> switch between the two videos (restarts the newly-selected video from the beginning)
  [1]      -> choose Video 1 (the first in the randomized order for THIS TRIAL)
  [2]      -> choose Video 2
  [ESC]    -> abort experiment

Dependencies:
  pip install psychtoolbox numpy

Important notes:
- This script uses Psychtoolbox's Screen movie API via the Python wrapper.
- On some platforms you may need codecs (e.g., install ffmpeg) and to use common formats (H.264 MP4).
- For consistent timing, run with a discrete GPU and disable desktop compositing/aero if possible.

Edit the TRIALS list below to point to your video files.
"""

import csv
import os
import random
from datetime import datetime

import numpy as np

from psychtoolbox import Screen, GetSecs, WaitSecs
from psychtoolbox import KbCheck, KbName

# -----------------------------
# User configuration
# -----------------------------
# Set your trials here. Each entry must have 'reference' and 'test' absolute paths.
TRIALS = [
    {"reference": r"/path/to/ref_scene1.mp4", "test": r"/path/to/test_scene1.mp4"},
    {"reference": r"/path/to/ref_scene2.mp4", "test": r"/path/to/test_scene2.mp4"},
]

RESULTS_CSV = "pairwise_results.csv"
FULLSCREEN = True
BACKGROUND_GREY = 128  # 0..255
TEXT_COLOUR = [255, 255, 255]
TEXT_SIZE = 28

# -----------------------------
# Helper functions
# -----------------------------

def draw_centered_text(win, text, y_offset=0):
    Screen('TextSize', win, TEXT_SIZE)
    Screen('TextFont', win, 'Arial')
    bounds = Screen('TextBounds', win, text)
    w = Screen('Rect', win)[2]
    h = Screen('Rect', win)[3]
    x = (w - bounds[2]) / 2
    y = (h - bounds[3]) / 2 + y_offset
    Screen('DrawText', win, text, x, y, TEXT_COLOUR)


def wait_for_keypress(valid_keys=None):
    """Block until any key is pressed. If valid_keys provided, block until one of them is pressed.
    Returns the pressed key name (lowercase).
    """
    if valid_keys is not None:
        valid_keys = [k.lower() for k in valid_keys]
    while True:
        pressed, _secs, key_codes = KbCheck()
        if pressed:
            key_idx = np.where(key_codes)[0]
            if len(key_idx) > 0:
                key_name = KbName(key_idx[0]).lower()
                if valid_keys is None or key_name in valid_keys:
                    return key_name


def play_movie_full(win, movie_handle):
    """Play a movie from the beginning to the end, blocking until finished.
    Returns the total duration played in seconds.
    """
    # Start playback at normal speed
    Screen('PlayMovie', movie_handle, 1.0)

    t_start = GetSecs()
    frame_count = 0

    while True:
        tex = Screen('GetMovieImage', win, movie_handle)
        if tex <= 0:
            # 0 or -1 indicates no new frame or end-of-movie depending on backend;
            # we treat <=0 as finished.
            break
        Screen('DrawTexture', win, tex)
        Screen('Flip', win)
        Screen('Close', tex)  # release texture
        frame_count += 1

    # Stop playback and rewind to start for potential replays
    Screen('PlayMovie', movie_handle, 0)
    Screen('SetMovieTimeIndex', movie_handle, 0.0)

    t_end = GetSecs()
    return t_end - t_start


def play_movie_with_escape(win, movie_handle, allow_escape=False):
    """Play a movie, but allow an early break if allow_escape and ESC is pressed.
    Returns (finished_normally: bool, seconds_played: float)
    """
    Screen('PlayMovie', movie_handle, 1.0)
    t_start = GetSecs()
    finished = True

    while True:
        tex = Screen('GetMovieImage', win, movie_handle)
        if tex <= 0:
            break
        Screen('DrawTexture', win, tex)
        Screen('Flip', win)
        Screen('Close', tex)

        if allow_escape:
            pressed, _secs, key_codes = KbCheck()
            if pressed:
                if key_codes[KbName('ESCAPE')]:
                    finished = False
                    break

    Screen('PlayMovie', movie_handle, 0)
    t_end = GetSecs()
    return finished, (t_end - t_start)


# -----------------------------
# Main experiment
# -----------------------------

def main():
    # Prepare CSV
    write_header = not os.path.exists(RESULTS_CSV)
    csv_file = open(RESULTS_CSV, 'a', newline='', encoding='utf-8')
    writer = csv.writer(csv_file)
    if write_header:
        writer.writerow([
            'timestamp', 'trial_index',
            'video1_path', 'video2_path', 'video1_label', 'video2_label',  # labels: REF/TEST
            'initial_order',  # e.g., "[video1, video2]"
            'watched1_seconds', 'watched2_seconds',
            'selection',  # 'video1' or 'video2'
            'selection_label',  # 'REFERENCE' or 'TEST'
            'rt_seconds'
        ])

    # Open screen
    if FULLSCREEN:
        win = Screen('OpenWindow', 0, BACKGROUND_GREY)
    else:
        # Small window for debugging: width=1280, height=720
        win = Screen('OpenWindow', 0, BACKGROUND_GREY, [100, 100, 1380, 820])

    Screen('TextSize', win, TEXT_SIZE)

    try:
        # Instruction screen
        draw_centered_text(win, "Pairwise video comparison", y_offset=-40)
        draw_centered_text(win, "You will first watch both videos fully in random order.", y_offset=0)
        draw_centered_text(win, "Then you can switch [SPACE] and choose [1]/[2].", y_offset=40)
        draw_centered_text(win, "Press any key to start.", y_offset=100)
        Screen('Flip', win)
        wait_for_keypress()

        # Trial loop
        for ti, trial in enumerate(TRIALS, start=1):
            ref_path = trial['reference']
            test_path = trial['test']
            if not os.path.exists(ref_path) or not os.path.exists(test_path):
                # Show error and skip
                Screen('FillRect', win, BACKGROUND_GREY)
                draw_centered_text(win, f"Missing file in trial {ti}")
                draw_centered_text(win, os.path.basename(ref_path), y_offset=40)
                draw_centered_text(win, os.path.basename(test_path), y_offset=80)
                draw_centered_text(win, "Press any key to continue.", y_offset=140)
                Screen('Flip', win)
                wait_for_keypress()
                continue

            # Randomize order: make a list of (label, path)
            pair = [('REFERENCE', ref_path), ('TEST', test_path)]
            random.shuffle(pair)
            (lab1, path1), (lab2, path2) = pair

            # Open movies
            movie1 = Screen('OpenMovie', win, path1)
            movie2 = Screen('OpenMovie', win, path2)

            # Show a trial start screen
            Screen('FillRect', win, BACKGROUND_GREY)
            draw_centered_text(win, f"Trial {ti}")
            draw_centered_text(win, "You must watch both videos fully once.", y_offset=40)
            draw_centered_text(win, "(Playback will start automatically)", y_offset=80)
            Screen('Flip', win)
            WaitSecs(0.7)

            # Initial full viewing in randomized order
            watched1 = play_movie_full(win, movie1)
            WaitSecs(0.3)
            watched2 = play_movie_full(win, movie2)

            # Comparison phase: allow switching and choice
            instructions = [
                f"Trial {ti}: Comparison",
                f"Video 1 = {lab1}    Video 2 = {lab2}",
                "SPACE: switch  |  1/2: choose  |  ESC: abort",
            ]

            current = 1  # start by showing video 1 again
            t_choice_start = GetSecs()

            while True:
                # Draw instruction overlay
                Screen('FillRect', win, BACKGROUND_GREY)
                for idx, line in enumerate(instructions):
                    draw_centered_text(win, line, y_offset=-140 + idx * 36)
                draw_centered_text(win, f"Currently: Video {current}", y_offset=-40)
                draw_centered_text(win, "(Playing...)", y_offset=0)
                Screen('Flip', win)

                # Play selected movie once (can be interrupted by SPACE/1/2/ESC)
                sel_movie = movie1 if current == 1 else movie2
                Screen('PlayMovie', sel_movie, 1.0)

                chosen = None
                interrupted_switch = False

                while True:
                    tex = Screen('GetMovieImage', win, sel_movie)
                    if tex <= 0:
                        break
                    Screen('DrawTexture', win, tex)
                    # Re-draw a small overlay label
                    draw_centered_text(win, f"Video {current}", y_offset=-Screen('Rect', win)[3] // 2 + 30)
                    Screen('Flip', win)
                    Screen('Close', tex)

                    pressed, _secs, key_codes = KbCheck()
                    if pressed:
                        if key_codes[KbName('ESCAPE')]:
                            raise KeyboardInterrupt
                        if key_codes[KbName('space')]:
                            interrupted_switch = True
                            break
                        if key_codes[KbName('1')] or key_codes[KbName('2')]:
                            chosen = 'video1' if key_codes[KbName('1')] else 'video2'
                            break

                Screen('PlayMovie', sel_movie, 0)
                Screen('SetMovieTimeIndex', sel_movie, 0.0)

                if chosen is not None:
                    rt = GetSecs() - t_choice_start
                    selection_label = lab1 if chosen == 'video1' else lab2
                    # Log and move on
                    writer.writerow([
                        datetime.now().isoformat(timespec='seconds'),
                        ti,
                        path1, path2, lab1, lab2,
                        f"[video1={lab1}, video2={lab2}]",
                        f"{watched1:.3f}", f"{watched2:.3f}",
                        chosen, selection_label,
                        f"{rt:.3f}",
                    ])
                    csv_file.flush()

                    # Feedback
                    Screen('FillRect', win, BACKGROUND_GREY)
                    draw_centered_text(win, f"You chose: {chosen.upper()} ({selection_label})")
                    draw_centered_text(win, "Press any key for next trial.", y_offset=50)
                    Screen('Flip', win)
                    wait_for_keypress()
                    break

                if interrupted_switch:
                    current = 2 if current == 1 else 1
                    continue

            # Close movies
            Screen('CloseMovie', movie1)
            Screen('CloseMovie', movie2)

        # End screen
        Screen('FillRect', win, BACKGROUND_GREY)
        draw_centered_text(win, "All trials completed. Thank you!")
        draw_centered_text(win, f"Results saved to: {RESULTS_CSV}", y_offset=40)
        Screen('Flip', win)
        WaitSecs(1.5)
        draw_centered_text(win, "Press any key to exit.", y_offset=100)
        Screen('Flip', win)
        wait_for_keypress()

    except KeyboardInterrupt:
        Screen('FillRect', win, BACKGROUND_GREY)
        draw_centered_text(win, "Experiment aborted (ESC pressed).")
        Screen('Flip', win)
        WaitSecs(1.0)

    finally:
        Screen('CloseAll')
        csv_file.close()


if __name__ == '__main__':
    main()
