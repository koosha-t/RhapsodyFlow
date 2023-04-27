import re
from music21 import stream, note, chord,pitch, meter, duration, tie, dynamics, midi, tempo, clef
import pdb


def melocode_to_stream(melocode, tempo_bpm=100):
    # Create empty stream objects to store notes, rests, and other musical elements for both hands
    right_hand = stream.Stream()
    left_hand = stream.Stream()

    # Add the treble clef to the right_hand stream and the bass clef to the left_hand stream
    right_hand.append(clef.TrebleClef())
    left_hand.append(clef.BassClef())
    
    # Define regex patterns to match time signature, notes, and dynamic markings
    time_signature_pattern = re.compile(r'\(\d+/\d+\)')
    
    # stripping any whitespace at the beginning and end
    melocode = re.split(r'\s*\|\s*', melocode.strip())
    melocode = [x for x in melocode if x not in ['','{','}']]

    # Extract the time signature from the MeloCode notation
    time_signature = time_signature_pattern.findall(melocode[0])[0]
    
    # Add the time signature to both streams
    right_hand.append(meter.TimeSignature(time_signature))
    left_hand.append(meter.TimeSignature(time_signature))

    # Add the tempo to both streams
    right_hand.append(tempo.MetronomeMark(number=tempo_bpm))
    left_hand.append(tempo.MetronomeMark(number=tempo_bpm))

    # Define regex patterns to match notes, rests, dynamics, and tied notes
    note_pattern = re.compile(r'\d+(?:/\d+)?[A-G][#b]?\d|[R]\d(?:/\d+)?|t[A-G][#b]?\d')
    dynamics_pattern = re.compile(r'<[pmf]>')
    chord_pattern = re.compile(r'\d+(?:/\d+)?\[[A-G][#b]?\d(,[A-G][#b]?\d)*\]')
    hands_separator_pattern = re.compile(r'&&')

    # Iterate through each bar in the MeloCode notation
    for bar in melocode[1:]:
        # Split the bar into right hand and left hand parts

        right_hand_bar, left_hand_bar = hands_separator_pattern.split(bar)
        

        # Create a new Measure object for each bar and for each hand
        right_hand_measure = stream.Measure()
        left_hand_measure = stream.Measure()

        # Iterate through each hand's tokens in the current bar
        for hand_bar, measure in [(right_hand_bar, right_hand_measure), (left_hand_bar, left_hand_measure)]:
            for token in hand_bar.split():
                # Check if the token matches a dynamic marking
                dynamic_match = dynamics_pattern.match(token)
                if dynamic_match:
                    dynamic_symbol = dynamic_match.group()
                    dynamic_value = dynamic_symbol[1]
                    measure.append(dynamics.Dynamic(dynamic_value))
                    continue

                # Check if the token matches a chord
                chord_match = chord_pattern.match(token)  
                if chord_match:
                    chord_info = chord_match.group()
                    dur_start = re.search('\d', chord_info).start()
                    dur_end = re.search('\[', chord_info).start()
                    dur = chord_info[dur_start:dur_end]
                    pitch_strs = chord_info[dur_end + 1:-1].split(',')
                    dur = float(eval(dur)) * 4
                    current_chord = chord.Chord(pitch_strs)
                    current_chord.duration = duration.Duration(dur)
                    measure.append(current_chord)
                    continue

                # Check if the token matches a note, rest, or tied note
                note_match = note_pattern.match(token)
                if note_match:
                    note_info = note_match.group()
                    # If the token represents a rest
                    if note_info.startswith("R"):
                        rest_duration = duration.Duration(float(eval(note_info[1:])) * 4)
                        rest = note.Rest()
                        rest.duration = rest_duration
                        measure.append(rest)
                    else:
                        # If the token represents a tied note
                        if note_info.startswith("t"):
                            pitch_str = note_info[1:]
                            tied_dur = note.Note(pitch_str).duration.quarterLength
                            current_note.duration.quarterLength += tied_dur
                            current_note.tie = tie.Tie('start')
                            measure[-1].tie = tie.Tie('stop')  # Update the last note in the measure
                        else:
                            # If the token represents a note
                            first_letter_index = re.search('[A-G]', note_info).start()
                            dur = note_info[:first_letter_index]
                            pitch_str = note_info[first_letter_index:]
                            dur = float(eval(dur)) * 4
                            current_note = note.Note(pitch_str)
                            current_note.duration = duration.Duration(dur)
                            measure.append(current_note)

            # Add the completed measure to the appropriate hand stream
            if measure == right_hand_measure:
                right_hand.append(measure)
            else:
                left_hand.append(measure)

    # Combine both hand streams into a single stream
    complete_melody = stream.Score()
    complete_melody.insert(0, right_hand)
    complete_melody.insert(0, left_hand)

    return complete_melody



def play_melocode(melocode):
    # Convert MeloCode notation to a music21 stream
    melody = melocode_to_stream(melocode)
    
    # Play the melody using music21's MIDI playback
    melody.show()



def save_melocode_to_midi(melocode, output_filename):
    # Convert MeloCode notation to a music21 stream
    melody = melocode_to_stream(melocode, tempo_bpm=160)
    # Save the melody to a MIDI file using music21's write function
    melody.write('midi',output_filename)
    #melody.write('midi', fp=output_filename)
    print(f"MIDI file saved as {output_filename}")



if __name__ == "__main__":
    romantic_melody = """(4/4) | <p> 1/4A4 1/4C5 1/4E5 1/4A5 && <p> 1/4A2 1/4E3 1/4A3 1/4E3 |
| <m> 1/8A5 1/8E5 1/8C5 1/8E5 R1/4 <f> 1/4A4 && <m> 1/4E2 1/4A2 1/4E3 <f> 1/4A3 |
| 1/2C5 tC5 R1/2 && 1/2C3 tC3 R1/2 |
| 1/4[B4,E5,G5] R1/2 && 1/4[E2,B2,E3] R1/2 |
| 1/4A4 1/4C5 1/4E5 1/4A5 && 1/4A2 1/4E3 1/4A3 1/4E3 |
| 1/8A5 1/8E5 1/8C5 1/8E5 R1/4 1/4A4 && 1/4E2 1/4A2 1/4E3 1/4A3 |
{1/4A4 1/4C5 1/4E5 1/4A5 && 1/4A2 1/4E3 1/4A3 1/4E3 |
| 1/8A5 1/8E5 1/8C5 1/8E5 R1/4 1/4A4 && 1/4E2 1/4A2 1/4E3 1/4A3 |}
| <f> 1/4[F4,A4,C5] 1/4[F4,A4,E5] 1/4[F4,A4,C5] 1/4[F4,A4,E5] && <f> 1/4F2 1/4C3 1/4F3 1/4C3 |
| R1/4 1/4E5 1/4C5 1/4A4 && R1/4 1/4C3 1/4F2 1/4C2 |
| <p> 1/2A4 tA4 R1/2 && <p> 1/2A2 tA2 R1/2 |
| 1/4[B4,E5,G5] R1/2 && 1/4[E2,B2,E3] R1/2 |
| 1/4A4 1/4C5 1/4E5 1/4A5 && 1/4A2 1/4E3 1/4A3 1/4E3 |
| <f> 1/8A5 1/8E5 1/8C5 1/8E5 R1/4 1/4A4 && <f> 1/4E2 1/4A2 1/4E3 1/4A3 |
| <m> 1/4[D4,F4,A4] 1/4[D4,F4,B4] 1/4[D4,F4,A4] 1/4[D4,F4,B4] && <m> 1/4D2 1/4A2 1/4D3 1/4A3 |
| 1/8A4 1/8F4 1/16D4 1/16F4 1/16A4 1/16F4 1/16D4 1/16F4 && 1/4A2 1/4D3 1/4A3 1/4D3 |
| 1/16E5 1/16C5 1/16A4 1/16C5 1/16E5 1/16C5 1/16A4 1/16C5 && 1/4C3 1/4G2 1/4C3 1/4G3 |
| <f> 1/4[B4,E5,G5] 1/4[B4,E5,A5] 1/4[B4,E5,G5] 1/4[B4,E5,A5] && <f> 1/4E2 1/4B2 1/4E3 1/4B3 |
| 1/8C5 1/8G4 1/8E4 1/8G4 1/8C5 1/8G4 && 1/4C3 1/4G2 1/4C3 1/4G3 |
| 1/32A4 1/32C5 1/32E5 1/32A5 1/32E5 1/32C5 1/32A4 1/32C5 && 1/4A2 1/4E3 1/4A3 1/4E3 |
| 1/16A5 1/16E5 1/16C5 1/16E5 1/16A5 1/16E5 1/16C5 1/16E5 && 1/4E2 1/4A2 1/4E3 1/4A3 |
| <f> 1/4[F4,A4,C5] 1/4[F4,A4,E5] 1/4[F4,A4,C5] 1/4[F4,A4,E5] && <f> 1/4F2 1/4C3 1/4F3 1/4C3 |
| R1/4 1/4E5 1/4C5 1/4A4 && R1/4 1/4C3 1/4F2 1/4C2 |
| <p> 1/2A4 tA4 R1/2 && <p> 1/2A2 tA2 R1/2 |
| 1/4[B4,E5,G5] R1/2 && 1/4[E2,B2,E3] R1/2 |
| 1/4A4 1/4C5 1/4E5 1/4A5 && 1/4A2 1/4E3 1/4A3 1/4E3 |
| <ff> 1/4[F4,A4,D5,F5] 1/4[F4,A4,E5,F5] 1/4[F4,A4,D5,F5] 1/4[F4,A4,E5,F5] && <ff> 1/4F2 1/4C3 1/4F3 1/4C3 |
| 1/8A4 1/8C5 1/8E5 1/8A5 1/8E5 1/8C5 1/8A4 1/8C5 && 1/4A2 1/4E3 1/4A3 1/4E3 |
| <f> 1/4[B4,D5,G5,B5] 1/4[B4,E5,G5,B5] 1/4[B4,D5,G5,B5] 1/4[B4,E5,G5,B5] && <f> 1/4G2 1/4D3 1/4G3 1/4D3 |
| 1/8D5 1/8G5 1/8B5 1/8D6 1/8B5 1/8G5 1/8D5 1/8G5 && 1/4D2 1/4G2 1/4D3 1/4G3 |

| <ff> 1/4[C4,E4,A4,C5] 1/4[C4,E4,B4,C5] 1/4[C4,E4,A4,C5] 1/4[C4,E4,B4,C5] && <ff> 1/4C2 1/4G2 1/4C3 1/4G3 |
| 1/8E4 1/8G4 1/8C5 1/8E5 1/8C5 1/8G4 1/8E4 1/8G4 && 1/4C3 1/4G3 1/4C3 1/4G3 |
| <f> 1/4[A4,C5,F5,A5] 1/4[A4,C5,F5,G5] 1/4[A4,C5,F5,A5] 1/4[A4,C5,F5,G5] && <f> 1/4F2 1/4C3 1/4F3 1/4C3 |
| 1/8A5 1/8F5 1/8C5 1/8F5 1/8A5 1/8F5 1/8C5 1/8F5 && 1/4C3 1/4F2 1/4C2 1/4F2 |

| <ff> 1/4[B4,D5,G5,B5] 1/4[B4,E5,G5,B5] 1/4[B4,D5,G5,B5] 1/4[B4,E5,G5,B5] && <ff> 1/4G2 1/4D3 1/4G3 1/4D3 |
| 1/8D5 1/8G5 1/8B5 1/8D6 1/8B5 1/8G5 && 1/4D2 1/4G2 1/4D3 1/4G3 |
| <ff> 1/4[A4,C5,E5,A5] 1/4[A4,C5,F5,A5] 1/4[A4,C5,E5,A5] 1/4[A4,C5,F5,A5] && <ff> 1/4A2 1/4E3 1/4A3 1/4E3 |
| 1/8E5 1/8A5 1/8C6 1/8A5 1/8E5 1/8A5 1/8C6 1/8A5 && 1/4E3 1/4A2 1/4E3 1/4A3 |
| <f> 1/4[D4,F4,A4,D5] 1/4[D4,F4,B4,D5] 1/4[D4,F4,A4,D5] 1/4[D4,F4,B4,D5] && <f> 1/4D2 1/4A2 1/4D3 1/4A3 |

| <ff> 1/4[C4,E4,G4,C5] 1/4[C4,E4,A4,C5] 1/4[C4,E4,G4,C5] 1/4[C4,E4,A4,C5] && <ff> 1/4C2 1/4G2 1/4C3 1/4G3 |
| 1/8G4 1/8C5 1/8E5 1/8G5 1/8E5 1/8C5 1/8G4 1/8C5 && 1/4C3 1/4G3 1/4C3 1/4G3 |
| <f> 1/4[B4,D5,F5,B5] 1/4[B4,D5,G5,B5] 1/4[B4,D5,F5,B5] 1/4[B4,D5,G5,B5] && <f> 1/4B2 1/4F3 1/4B3 1/4F3 |
| 1/8F5 1/8B5 1/8D6 1/8B5 1/8F5 1/8B5 1/8D6 1/8B5 && 1/4F2 1/4B2 1/4F3 1/4B3 |

| <ff> 1/4[A4,C5,E5,A5] 1/4[A4,C5,F5,A5] 1/4[A4,C5,E5,A5] 1/4[A4,C5,F5,A5] && <ff> 1/4A2 1/4E3 1/4A3 1/4E3 |
| 1/8E5 1/8A5 1/8C6 1/8A5 1/8E5 1/8A5 1/8C6 1/8A5 && 1/4E3 1/4A2 1/4E3 1/4A3 |
| <mf> 1/4[D4,F4,A4,D5] 1/4[D4,F4,B4,D5] 1/4[D4,F4,A4,D5] 1/4[D4,F4,B4,D5] && <mf> 1/4D2 1/4A2 1/4D3 1/4A3 |
| 1/8D5 1/8A5 1/8F5 1/8A5 1/8D5 1/8A5 1/8F5 1/8A5 && 1/4D3 1/4A2 1/4D3 1/4A3 |

| <p> 1/4[C4,E4,G4,C5] 1/4[C4,E4,A4,C5] 1/4[C4,E4,G4,C5] 1/4[C4,E4,A4,C5] && <p> 1/4C2 1/4G2 1/4C3 1/4G3 |
| 1/8C5 1/8G4 1/8E4 1/8G4 1/8C5 1/8G4 1/8E4 1/8G4 && 1/4C3 1/4G2 1/4C3 1/4G3 |

| <pp> 1/4[A4,C5,E5,A5] 1/4[A4,C5,F5,A5] 1/4[A4,C5,E5,A5] 1/4[A4,C5,F5,A5] && <pp> 1/4A2 1/4E3 1/4A3 1/4E3 |
| 1/8A5 1/8E5 1/8C5 1/8E5 1/8A5 1/8E5 1/8C5 1/8E5 && 1/4E2 1/4A2 1/4E3 1/4A3 |

| <p> 1/4A4 1/4C5 1/4E5 1/4A5 && 1/4A2 1/4E3 1/4A3 1/4E3 |
| R1/2 1/2A4 && R1/2 1/2A2 |
| R1/2 1/2A4 && R1/2 1/2A2 |

| <pp> 1/4A4 1/4C5 1/4E5 1/4A5 && 1/4A2 1/4E3 1/4A3 1/4E3 |
| R1/2 1/2A4 && R1/2 1/2A2 |
"""

play_melocode(romantic_melody)
# output_filename = "romantic_melody.mid"
# save_melocode_to_midi(romantic_melody, output_filename)


