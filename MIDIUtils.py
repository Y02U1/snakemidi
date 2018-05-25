import mido
from mido import tick2second
import numpy as np
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
import pickle

# TODO OOP


def tempo_deltares(tempo, delta, ref_res):
    """
    Calcola la risoluzione per 1 evento musicale
    :param tempo: tempo dell'evento (e.g. 500000 microsecondi -> 120 bpm)
    :param delta: durata dell'evento
    :param ref_res: risoluzione di riferimento
    :return: risoluzione di quell'evento
    """
    # In caso di errori di calcolo / arrotondamento...
    if delta < 0:
        # ... ignora
        return 0
    # Valore in 1/4 della nota di riferimento
    const = 4
    # Risolvi la proporzione e ritorna il valore
    # const (in secondi) : ref_res = delta : x
    return ref_res * delta / (tempo / 1000000.0 * const)


def tempo_refres(tempo):
    """
    Calcola la risoluzione di riferimento sulla base del tempo
    :param tempo: tempo (e.g. 500000 microsecondi -> 120 bpm)
    :return: risoluzione di riferimento adatta per quel tempo musicale
    """
    const = 4
    return tempo / 1000000 * const * 100


# TODO trova nome "meaningful"
def y_eased(x):
    """
    Calcola un valore di easing quadraticamente
    :param x: valore di cui calcolare l'eased
    :return: valore eased
    """
    return (x-1)**2


def read_track(track, tick_per_beat):
    """
    Leggi il track
    :param track: track da cui leggere gli eventi musicali
    :param tick_per_beat: ticks/1 beat
    :return: matrice (3 righe, n colonne) di eventi musicali
    """
    time_since_begin = 0
    notes = [[], [], []]
    for msg in track:
        # Se il messaggio è "note_on" (può anche essere una pausa)
        if str(msg.type) == "note_on":
            # Converti la durata in tick del messaggio in secondi
            delta = round(tick2second(msg.time, tick_per_beat, get_tempo(track)), 2)
            time_since_begin = time_since_begin + delta  # TODO controllare se questo non sia un passaggio inutile
            # Se è una pausa...
            if msg.velocity is 0:
                notes[0].append("p")
            # Se è una nota...
            else:
                notes[0].append("n")
            # Aggiungi poi gli altri parametri
            notes[1].append(time_since_begin)
            # FIXME uso improprio (il tempo può cambiare durante il track)
            notes[2].append(get_tempo(track))
    return notes


def compute_values(notes, length, resolution=100):
    """
    Calcola gli assi x, y della funzione della velocità di movimento del Player
    :param notes: matrice di 3 righe e n colonne dove
                        riga 0: tipologia di evento ("p" pausa, "n" nota)
                        riga 1: tempo dall'inizio del .mid (in secondi)
                        riga 2: "tempo" della nota (500000 microsecondi -> 120 bpm)
                        n: numero di eventi musicali
    :param length: durata del .mid
    :param resolution: valore di riferimento, specifica il numero di sample per
                        una nota di 4/4 (valore costante, può essere modificato)
    :return: x,y i valori dei 2 assi (x -> secondi, y -> velocità)
    """
    x_values = []
    y_values = []
    # Per ogni evento...
    for i in range(len(notes[0])):
        #
        # ------------------------------ CALCOLO X ---------------------------------
        #
        # Calcola la durata dell'evento (secondi)
        # Calcola la risoluzione dell'evento
        # Calcola le x per l'evento con la risoluzione trovata
        try:
            #   Error -------,,,,,
            delta = notes[1][i + 1] - notes[1][i]
            note_res = round(tempo_deltares(notes[2][i], delta, resolution))
            x_for_note = np.linspace(notes[1][i], notes[1][i + 1], note_res)
        except IndexError:
            # In caso d'ultimo evento (notes[1][i+1] -> IndexError)
            # Usa la lunghezza totale (del .mid) per calcolare la durata dell'evento
            delta = length - notes[1][i]
            note_res = round(tempo_deltares(notes[2][i], delta, resolution))
            x_for_note = np.linspace(notes[1][i], length, note_res)
        # Aggiungi i valori per questo evento alla x
        x_values = np.concatenate([x_values, x_for_note])
        #
        # ------------------------------- CALCOLO Y --------------------------------
        #
        # Se è una nota...
        if notes[0][i] is 'n':
            # Calcola l'intervallo sulla x
            x_range = np.linspace(0, 1, note_res)
            y_for_note = []
            # Per ogni valore nell'intervallo
            for x in x_range:
                # Computa il valore corrispondente sulla y (tramite easing)
                y_for_note.append(y_eased(x))
            # Aggiungi i valori per questo evento alla y
            y_values = np.concatenate([y_values, y_for_note])
        # Altrimenti (se è una pausa)
        else:
            # Calcola i valori sulla y (essendo una pausa sono n 0)
            #   n -> risoluzione per l'evento
            y_for_note = np.zeros(note_res, dtype=int)
            # Aggiungi i valori per questo evento alla y
            y_values = np.concatenate([y_values, y_for_note])
    return x_values, y_values


def get_tempo(track):
    """
    Ritorna il tempo (e.g. 500000 microsecondi -> 120 bpm) in microsecondi
    :param track: track da cui estrapolare il tempo
    :return: il tempo in microsecondi, se si evince da un MetaMessage set_tempo
    altrimenti ritorna 500000 (valore di default nei file .mid)
    """
    for msg in track:
        # Dividi in valori HEX -> A3 B5 23 E4 ...
        hex_bytes = msg.hex().split(" ")
        # Se il messaggio è un set_tempo (FF 51 sono i primi byte HEX)
        if hex_bytes[0] == "FF" and hex_bytes[1] == "51":
            tempo_str = ""
            # Itera n volte
            #   n = numero di byte che identifica il tempo
            #       che si trova alla posizione 2 del messaggio
            #
            #   pos  00 01 02 03 04 05
            #   e.g. FF 51 03 xx xx xx -> indica che il tempo è contenuto nei 3 byte successivi
            #           ---^^ ( tempo )
            for i in range(int(hex_bytes[2])):
                # Costruisci la stringa con il tempo in HEX
                tempo_str = tempo_str + hex_bytes[i+3]
            # Converti in decimale e ritorna quanto trovato
            return int(tempo_str, 16)
    # Altrimenti ritorna 500000, valore di default
    return 500000


def get_ticks_per_beat(filename):
    """
    Ritorna i ticks/beat del file .mid
    :param filename: file .mid
    :return: ticks/beat di quel file .mid
    """
    with mido.MidiFile(filename) as mid:
        return mid.ticks_per_beat


def split_midi(filename):
    """
    Dividi i track del file .mid e ritorna quelli con musica
    :param filename: file .mid da splittare
    :return: [] di track del file .mid; contiene solo quelli con almeno un'istanza di Message
    """
    music_tracks = []
    # Apri il file
    with mido.MidiFile(filename) as mid:
        # Per ogni track
        for i, track in enumerate(mid.tracks):
            # Per ogni messaggio
            for msg in track:
                # Se c'è un messaggio Message (tipicamente note_on / note_off)
                # Aggiungi il track (è musicale)
                # E rompi il loop (non c'è bisogno di andare avanti)
                # TODO documentare meglio
                if type(msg) is mido.messages.messages.Message:
                    music_tracks.append(track)
                    break
    return music_tracks


def get_length(filename):
    """
    Ritorna la durata del .mid (in secondi)
    :param filename: file .mid
    :return: durata del .mid (in secondi)
    """
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
            x, y = compute_values(notes, get_length(filename), resolution=tempo_refres(get_tempo(track)))
            staves.append([x, y])
    return staves


def multitrack_y(staves):
    """
    Funzione per la gestione multitrack (y)
    :param staves:
    :return:
    """
    # TODO trovare un uso pratico, o restare su .mid monofonici
    return np.multiply(staves[0], staves[1])


def multitrack_x(staves):
    """
    Funzione per la gestione multitrack (x)
    :param staves:
    :return:
    """
    # TODO trovare un uso pratico, o restare su .mid monofonici
    return max(staves, key=len)


if __name__ == "__main__":
    staves = proto("everlasting_hymn.mid")
    # pickle.dump(staves, open("mario.p", "wb"))
    # staves = pickle.load(open("mario.p", "rb"))
    plt.plot(staves[0][0], staves[0][1], "yo")
    plt.show()