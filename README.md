# RhapsodyFlow
Transforming emotions into captivating melodies. Immerse yourself in a world where the language of music transcends boundaries, as RhapsodyFlow weaves your feelings into enchanting compositions. Embrace the power of expression and let your emotions sing with RhapsodyFlow.

<p align="center">
  <img src="./readme_imgs/rf1.png" alt="Image Description" width="60%">
  <br>
  <em>RhapsodyFlow: Unleash Your Imagination in a World of Musical Dreams <br> (Art generated using MidJourney) </em>
</p>

## *MeloCode*: RhapsodyFlow's Custom Notation System
__MeloCode__ is a notation system designed to enable effective communication between language models, humans, and other generative models about music.  MeloCode serves as a common language that simplifies interactions between different entities involved in the music creation process. Here is how the MeloCode notation system encodes music:
- *__Pitch__*
    - Uppercase letters for natural notes (C, D, E, F, G, A, B)
    - '#' for sharps and 'b' for flats (C#, Db, D#, Eb, F#, Gb, G#, Ab, A#, Bb)
    - numbers to indicate the octave of the notes (C4: middle C, A3: A below middle C)
- *__Duration__*: Numbers as fractions for note duration, placing them before the pitch notation:
    - 1: whole note (1C4: whole note C in the 4th octave)
    - 1/2: half note (1/2D4: half note D in the 4th octave)
    - 1/4: quarter note (1/4E4: quarter note E in the 4th octave)
    - 1/8: eighth note (1/8F4: eighth note F in the 4th octave)
    - 1/16: sixteenth note (1/16G4: sixteenth note G in the 4th octave)
    - 1/32: thirty-second note (1/32A4: thirty-second note A in the 4th octave)
- *__Rest__*: Uppercase 'R' followed by the duration number, placing them before or after a note as needed:
    - R1: whole rest (1/4C4 R1 1/4C4: quarter note C, whole rest, quarter note C)
    - R1/2: half rest (1/2D4 R1/2 1/4D4: half note D, half rest, quarter note D)
    - R1/4: quarter rest (1/8E4 R1/4 1/8E4: eighth note E, quarter rest, eighth note E)
    - R1/8: eighth rest (1/4F4 R1/8 1/16F4: quarter note F, eighth rest, sixteenth note F)
    - R1/16: sixteenth rest (1/16G4 R1/16 1/32G4: sixteenth note G, sixteenth rest, thirty-second note G)
- *__Bar lines and time signature__*: '|' for bar lines and a tuple for the time signature.
    - (4/4): time signature (4 beats per measure, with a quarter note receiving one beat)
    - The following example features a 4/4 time singnature and three measures separated by bar lines:
        - (4/4) | 1/4C4 1/4E4 1/4G4 1/4C5 | R1/4 1/8D4 1/8F4 1/4A4 1/4D5 | R1/2 1/4E4 1/4G4 1/4E5 |
- *__Dynamics__* :  angle brackets with the first letter of the dynamic marking.
    - `<p>`: piano (soft)
    - `<f>`: forte (loud)
    - `<m>`: mezzo (medium)
    - Example: (4/4) | `<p>` 1/4C4 1/4E4 `<m>` 1/4G4 `<f>` 1/4C5 | R1/4 `<p>` 1/8D4 1/8F4 `<f>` 1/4A4 1/4D5 | R1/2 `<m>` 1/4E4 1/4G4 1/4E5 |
- *__Ties__*:  A lowercase 't' followed by the pitch of the tied note.
    - If you want to tie two notes together, write the first note with its duration, followed by 't' and the pitch of the second note (without the duration).
    - Example: 1/2C4 tC4: a half note C in the 4th octave tied to another C in the 4th octave.
- *__Repeats__*: Curly brackets to indicate repeats.
    - { ... }: repeat the section within the brackets



