import mido
from mido import tick2second
import numpy as np
from pytweening import easeInQuad
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
import pickle


def tempo_deltares(tempo, delta, resolution):
    print(tempo, delta, resolution)
    if delta < 0:
        return 0
    const = 4
    return resolution * delta / (tempo / 1000000.0 * const)


def tempo_refres(tempo):
    const = 4
    return tempo / 1000000 * const * 100


def my_func(x):
    # 1/ln(x+exp(1))-3/4
    return (x-1)**2


def read_midi(filename):
    with mido.MidiFile(filename) as mid:
        for i, track in enumerate(mid.tracks):
            # print('Track {}: {}'.format(i, track.name))
            for msg in track:
                # print(msg)
                pass


def read_track(track, tick_per_beat):
    time_since_begin = 0
    notes = [[], [], []]
    for msg in track:
        if str(msg.type) == "note_on":
            # print(msg.time, tick_per_beat, get_tempo(track))
            delta = round(tick2second(msg.time, tick_per_beat, get_tempo(track)), 2)
            time_since_begin = time_since_begin + delta
            if msg.velocity is 0:
                # print("Pausa:", time_since_begin)
                notes[0].append("p")
            else:
                # print("Nota:", time_since_begin)
                notes[0].append("n")
            notes[1].append(time_since_begin)
            notes[2].append(get_tempo(track))
    return notes


def compute_values(notes, length, resolution=100):
    x_values = []
    y_values = []
    for i in range(len(notes[0])):
        note_res = 0
        try:
            delta = notes[1][i + 1] - notes[1][i]
            note_res = round(tempo_deltares(notes[2][i], delta, resolution))
            x_for_note = np.linspace(notes[1][i], notes[1][i + 1], note_res)
        except IndexError:
            delta = length - notes[1][i]
            note_res = round(tempo_deltares(notes[2][i], delta, resolution))
            x_for_note = np.linspace(notes[1][i], length, note_res)
        print(note_res)
        # Se è una nota...
        if notes[0][i] is 'n':
            x_range = np.linspace(0, 1, note_res)
            x_values = np.concatenate([x_values, x_for_note])
            y_for_note = []
            for x in x_range:
                y_for_note.append(my_func(x))
            y_values = np.concatenate([y_values, y_for_note])
        # Altrimenti (se è una pausa)
        else:
            x_values = np.concatenate([x_values, x_for_note])
            y_for_note = np.zeros(note_res, dtype=int)
            y_values = np.concatenate([y_values, y_for_note])
    return x_values, y_values


def get_tempo(track):
    for msg in track:
        hex_bytes = msg.hex().split(" ")
        if hex_bytes[0] == "FF" and hex_bytes[1] == "51":
            str = ""
            for i in range(int(hex_bytes[2])):
                str = str + hex_bytes[i+3]
            return int(str, 16)
    return 500000


def get_ticks_per_beat(filename):
    with mido.MidiFile(filename) as mid:
        return mid.ticks_per_beat


def split_midi(filename):
    music_tracks = []
    with mido.MidiFile(filename) as mid:
        # print(mid.ticks_per_beat)
        for i, track in enumerate(mid.tracks):
            # print('Track {}: {}'.format(i, track.name))
            for msg in track:
                if type(msg) is mido.messages.messages.Message:
                    music_tracks.append(track)
                    break
    return music_tracks


def get_length(filename):
    with mido.MidiFile(filename) as mid:
        return mid.length


def proto(filename):
    staves = []
    for track in split_midi(filename):
        notes = read_track(track, get_ticks_per_beat(filename))
        # print(notes)
        if len(notes[0]) is 0 and len(notes[1]) is 0:
            pass
        else:
            print(tempo_refres(get_tempo(track)))
            x, y = compute_values(notes, get_length(filename), resolution=tempo_refres(get_tempo(track)))
            staves.append([x, y])
    return staves


def multitrack_y(staves):
    # print(len(staves[0]), len(staves[1]))
    return np.multiply(staves[0], staves[1])


def multitrack_x(staves):
    return max(staves, key=len)


if __name__ == "__main__":
    staves = proto("everlasting_hymn.mid")
    # pickle.dump(staves, open("mario.p", "wb"))
    # staves = pickle.load(open("mario.p", "rb"))
    """
    plt.plot(staves[0][0], staves[0][1], "yo")
    plt.plot(staves[1][0], staves[1][1], "ro")
    plt.plot(multitrack_x([staves[0][0], staves[1][0]]),
             multitrack_y([staves[0][1], staves[1][1]]), "bo")
    """
    plt.plot(staves[0][0], staves[0][1], "yo")
    plt.show()