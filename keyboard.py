import curses
import math
from curses import wrapper
from pyo import Fader, Server, Sine
from threading import Timer


QWERTY = ['qwertyuiop',
          'asdfghjkl',
          'zxcvbnm']


def hz(n):
    base = 440
    return base * math.pow(2, (n - 49) / 12)


def generate_keyboard_map():
    keys = {}
    q, a, z = 38, 39, 50
    q_row, a_row, z_row = QWERTY
    q_notes = [hz(k) for k in range(q, q + 22, 2)]
    a_notes = [hz(k) for k in range(a, a + 20, 2)]
    z_notes = [hz(k) for k in range(z, z + 20, 2)]
    keys.update({l: h for l, h in zip(q_row, q_notes)})
    keys.update({l: h for l, h in zip(a_row, a_notes)})
    keys.update({l: h for l, h in zip(z_row, z_notes)})
    return keys


def play_note(hz):
    out = Sine(hz).out()
    return out


def stop_note(note):
    note.stop()


def interpret_key(key, signal, key_map=KEY_MAP):
    hz = key_map.get(key)
    if hz is not None:
        note = play_note(hz)
        t = Timer(1, stop_note, [note])
        t.start()
    return None


def setup_audio_server():
    s = Server().boot()
    s.start()
    return s


def main(stdscr):
    server = setup_audio_server()
    signal = Sine(100).out()
#    env = Fader(fadein=0.01, fadeout=1.5, dur=2, mul=0.3)

    key_map = generate_keyboard_map()
    c = None
    stdscr.clear()
    while c != 27:
        # Store the key value in the variable `c`
        c = stdscr.getch()
        # Clear the terminal
        if c == 127:
            y, x = stdscr.getyx()
            stdscr.addstr(y, x - 1, '')
        else:
            key = chr(c)
            note = key_map.get(key)
            if note is not None:
                signal.freq = note
#            interpret_key(key, signal=signal)
            stdscr.addstr(key)
    server.stop()
    server.shutdown()

wrapper(main)
