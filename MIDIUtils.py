import mido


def read_midi(filename):
    with mido.MidiFile(filename) as mid:
        for i, track in enumerate(mid.tracks):
            print('Track {}: {}'.format(i, track.name))
            for msg in track:
                print(msg)


def split_midi(filename):
    music_tracks = []
    with mido.MidiFile(filename) as mid:
        for i, track in enumerate(mid.tracks):
            print('Track {}: {}'.format(i, track.name))
            for msg in track:
                if type(msg) is mido.messages.messages.Message:
                    music_tracks.append(track)
                    break
    print(len(music_tracks))
    with mido.MidiFile() as mid:
        mid.tracks.append(music_tracks[0])
        mid.play()