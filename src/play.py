import re
from music21 import stream, note, pitch, meter, duration, tie, dynamics

def melocode_to_stream(melocode):
    melody = stream.Stream()
    time_signature_pattern = re.compile(r'\(\d+/\d+\)')
    melocode = melocode.split("|")
    time_signature = time_signature_pattern.findall(melocode[0])[0]
    melody.append(meter.TimeSignature(time_signature))

    note_pattern = re.compile(r'\d+(?:/\d+)?[A-G][#b]?\d|[R]\d(?:/\d+)?')
    dynamics_pattern = re.compile(r'<[pmf]>')

    for bar in melocode[1:]:
        for token in bar.split():
            dynamic_match = dynamics_pattern.match(token)
            if dynamic_match:
                dynamic_symbol = dynamic_match.group()
                dynamic_value = dynamic_symbol[1]
                melody.append(dynamics.Dynamic(dynamic_value))
                continue

            note_match = note_pattern.match(token)
            if note_match:
                note_info = note_match.group()
                if note_info.startswith("R"):
                    rest_duration = duration.Duration(float(eval(note_info[1:])))
                    rest = note.Rest()
                    rest.duration = rest_duration
                    melody.append(rest)
                else:
                    first_letter_index = re.search('[A-G]', note_info).start()
                    dur = note_info[:first_letter_index]
                    pitch_str = note_info[first_letter_index:]
                    dur = float(eval(dur))
                    current_note = note.Note(pitch_str)
                    current_note.duration = duration.Duration(dur)
                    melody.append(current_note)


            tied_note = re.match(r't[A-G][#b]?\d', token)
            if tied_note:
                pitch_str = tied_note.group(1)
                current_note.tie = tie.Tie('start')
                tied_note = note.Note(pitch_str)
                tied_note.tie = tie.Tie('stop')
                melody.append(tied_note)

    return melody

def play_melocode(melocode):
    melody = melocode_to_stream(melocode)
    melody.show('midi')

if __name__ == "__main__":
    melocode_example = """(3/4) | <p> 1/4G4 R1/4 1/4A4 | 1/4B4 R1/4 1/4C5 | 1/4D5 1/4C5 1/4B4 | 1/4A4 1/4G4 1/4A4 |
1/4B4 1/4C5 1/4D5 | 1/4E5 1/4D5 1/4C5 | 1/4B4 1/4A4 1/4G4 | 1/4A4 R1/4 1/4B4 |
<m> 1/4C5 1/4B4 1/4A4 | 1/4G4 1/4F#4 1/4G4 | 1/4A4 1/4B4 1/4C5 | 1/4D5 1/4C5 1/4B4 |
1/4A4 1/4G4 1/4A4 | 1/4B4 1/4C5 1/4D5 | 1/4E5 1/4D5 1/4C5 | 1/4B4 1/4A4 1/4G4 |
<f> 1/4A4 R1/4 1/4B4 | 1/4C5 1/4B4 1/4A4 | 1/4G4 1/4F#4 1/4G4 | 1/4A4 1/4G4 1/4F#4 |
1/4G4 R1/4 1/4A4 | 1/4B4 R1/4 1/4C5 | 1/4D5 1/4C5 1/4B4 | 1/4A4 1/4G4 1/4A4 |
"""
    play_melocode(melocode_example)
