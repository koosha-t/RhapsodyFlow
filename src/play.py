import re
from music21 import stream, note, pitch, meter, duration, tie, dynamics

def melocode_to_stream(melocode):
    # Create an empty stream object to store notes, rests, and other musical elements
    melody = stream.Stream()
    
    # Define regex patterns to match time signature, notes, and dynamic markings
    time_signature_pattern = re.compile(r'\(\d+/\d+\)')
    melocode = melocode.split("|")
    
    # Extract the time signature from the MeloCode notation
    time_signature = time_signature_pattern.findall(melocode[0])[0]
    
    # Add the time signature to the stream
    melody.append(meter.TimeSignature(time_signature))

    # Define regex patterns to match notes, rests, and dynamics
    note_pattern = re.compile(r'\d+(?:/\d+)?[A-G][#b]?\d|[R]\d(?:/\d+)?')
    dynamics_pattern = re.compile(r'<[pmf]>')

    # Iterate through each bar in the MeloCode notation
    for bar in melocode[1:]:
        # Iterate through each token in the current bar
        for token in bar.split():
            # Check if the token matches a dynamic marking
            dynamic_match = dynamics_pattern.match(token)
            if dynamic_match:
                dynamic_symbol = dynamic_match.group()
                dynamic_value = dynamic_symbol[1]
                melody.append(dynamics.Dynamic(dynamic_value))
                continue

            # Check if the token matches a note or rest
            note_match = note_pattern.match(token)
            if note_match:
                note_info = note_match.group()
                # If the token represents a rest
                if note_info.startswith("R"):
                    rest_duration = duration.Duration(float(eval(note_info[1:])))
                    rest = note.Rest()
                    rest.duration = rest_duration
                    melody.append(rest)
                else:
                    # If the token represents a note
                    first_letter_index = re.search('[A-G]', note_info).start()
                    dur = note_info[:first_letter_index]
                    pitch_str = note_info[first_letter_index:]
                    dur = float(eval(dur))
                    current_note = note.Note(pitch_str)
                    current_note.duration = duration.Duration(dur)
                    melody.append(current_note)

            # Check if the token represents a tied note
            tied_note = re.match(r't[A-G][#b]?\d', token)
            if tied_note:
                pitch_str = tied_note.group(1)
                current_note.tie = tie.Tie('start')
                tied_note = note.Note(pitch_str)
                tied_note.tie = tie.Tie('stop')
                melody.append(tied_note)

    return melody

def play_melocode(melocode):
    # Convert MeloCode notation to a music21 stream
    melody = melocode_to_stream(melocode)
    
    # Play the melody using music21's MIDI playback
    melody.show('midi')


def play_melocode_with_chords(melody_melocode, chords_melocode):
    # Convert MeloCode notation to music21 streams for melody and chords
    melody = melocode_to_stream(melody_melocode)
    chords = melocode_to_stream(chords_melocode)
    
    # Create a new stream to store both melody and chords
    combined_stream = stream.Stream()
    
    # Add the melody (right-hand) and chords (left-hand) parts to the combined stream
    combined_stream.insert(0, melody)
    combined_stream.insert(0, chords)
    
    # Play the combined melody and chords using music21's MIDI playback
    combined_stream.show('midi')



if __name__ == "__main__":

    # Example melody and chords in MeloCode notation
    melody_melocode = """(4/4) | 1/4C5 1/4D5 1/4E5 1/4F5 | 1/4G5 1/4A5 1/4B5 1/4C6 | 1/4C6 1/4B5 1/4A5 1/4G5 | 1/4F5 1/4E5 1/4D5 1/4C5 |"""
    chords_melocode = """(4/4) | 1/4C3 1/4E3 1/4G3 1/4C4 | 1/4F3 1/4A3 1/4C4 1/4F4 | 1/4G3 1/4B3 1/4D4 1/4G4 | 1/4C3 1/4E3 1/4G3 1/4C4 |"""

    # Play the melody and chords together
    play_melocode_with_chords(melody_melocode, chords_melocode)



# if __name__ == "__main__":
#     melocode_example = """(3/4) | <p> 1/4G4 R1/4 1/4A4 | 1/4B4 R1/4 1/4C5 | 1/4D5 1/4C5 1/4B4 | 1/4A4 1/4G4 1/4A4 |
# 1/4B4 1/4C5 1/4D5 | 1/4E5 1/4D5 1/4C5 | 1/4B4 1/4A4 1/4G4 | 1/4A4 R1/4 1/4B4 |
# <m> 1/4C5 1/4B4 1/4A4 | 1/4G4 1/4F#4 1/4G4 | 1/4A4 1/4B4 1/4C5 | 1/4D5 1/4C5 1/4B4 |
# 1/4A4 1/4G4 1/4A4 | 1/4B4 1/4C5 1/4D5 | 1/4E5 1/4D5 1/4C5 | 1/4B4 1/4A4 1/4G4 |
# <f> 1/4A4 R1/4 1/4B4 | 1/4C5 1/4B4 1/4A4 | 1/4G4 1/4F#4 1/4G4 | 1/4A4 1/4G4 1/4F#4 |
# 1/4G4 R1/4 1/4A4 | 1/4B4 R1/4 1/4C5 | 1/4D5 1/4C5 1/4B4 | 1/4A4 1/4G4 1/4A4 |
# """
#     play_melocode(melocode_example)
