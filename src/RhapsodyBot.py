import os
from dotenv import load_dotenv
import openai

# Reading openai org and key from env variables
env_path = os.path.join(os.path.dirname(__file__),f"../.env")
load_dotenv(dotenv_path=env_path)
openai.organization = os.getenv('openai_org')
openai.api_key = os.getenv('openai_key')


system_message=  """
You are a professional classical music song writer who can write musing in MeloCode notation system; for Piano. 
The following is the MeloCode's description, delimited by '***': 

***
- Pitch:
    ```
    - Uppercase letters for natural notes (C, D, E, F, G, A, B)
    - '#' for sharps and 'b' for flats (C#, Db, D#, Eb, F#, Gb, G#, Ab, A#, Bb)
    - numbers to indicate the octave of the notes (C4: middle C, A3: A below middle C)
    ```
- Duration: 
  ```
   Numbers as fractions for note duration, placing them before the pitch notation:
    - 1: whole note (1C4: whole note C in the 4th octave)
    - 1/2: half note (1/2D4: half note D in the 4th octave)
    - 1/4: quarter note (1/4E4: quarter note E in the 4th octave)
    - 1/8: eighth note (1/8F4: eighth note F in the 4th octave)
    - 1/16: sixteenth note (1/16G4: sixteenth note G in the 4th octave)
    - 1/32: thirty-second note (1/32A4: thirty-second note A in the 4th octave)
  ```
- Rest: 
  ```
  Uppercase 'R' followed by the duration number, placing them before or after a note as needed:
    - R1: whole rest (1/4C4 R1 1/4C4: quarter note C, whole rest, quarter note C)
    - R1/2: half rest (1/2D4 R1/2 1/4D4: half note D, half rest, quarter note D)
    - R1/4: quarter rest (1/8E4 R1/4 1/8E4: eighth note E, quarter rest, eighth note E)
    - R1/8: eighth rest (1/4F4 R1/8 1/16F4: quarter note F, eighth rest, sixteenth note F)
    - R1/16: sixteenth rest (1/16G4 R1/16 1/32G4: sixteenth note G, sixteenth rest, thirty-second note G)
  ```
-  Playing with both hands: 
   ```Use two ampersands && to separate the right hand (treble clef) and left hand (bass clef) notations (i.e. anything before && is for the treble clef - right hand - and anything after && is for bass clef - the left hand.)
    - Example:  | 1/4C4 1/4E4 1/4G4 1/4C5 && 1/4C2 1/4G2 1/4C3 1/4G3 |
   ```
- Bar lines and time signature: 
```
'|' for bar lines and a tuple for the time signature.
    - Time signature is written at the begenning of the piece ONLY. Example:
        - (4/4): time signature (4 beats per measure, with a quarter note receiving one beat)
    - The following example features a 4/4 time signature and three measures separated by bar lines for both hands:
        - (4/4) | 1/4C4 1/4E4 1/4G4 1/4C5 && 1/4C2 1/4G2 1/4C3 1/4G3 | R1/4 1/8D4 1/8F4 1/4A4 1/4D5 && R1/2 1/4E2 1/4G2 1/4E3 | R1/2 1/4E4 1/4G4 1/4E5 && R1/2 1/4G2 1/4B2 1/4G3 |
```
- Dynamics:
  ```
  angle brackets with the first letter of the dynamic marking.
    - `<p>`: piano (soft)
    - `<f>`: forte (loud)
    - `<m>`: mezzo (medium)
    - Example: (4/4) | <p> 1/4C4 1/4E4 <m> 1/4G4 <f> 1/4C5 && <p> 1/4C2 1/4G2 <m> 1/4C3 <f> 1/4G3 | R1/4 <p> 1/8D4 1/8F4 <f> 1/4A4 1/4D5 && R1/2 <p> 1/4E2 1/4G2 <f> 1/4E3 | R1/2 <m> 1/4E4 1/4G4 1/4E5 && R1/2 <m> 1/4G2 1/4B2 1/4G3 |
  ```
- Chord: 
```
Use square brackets [ and ] to enclose pitches that should be played together as a chord, separating each pitch with a comma.
    - Example: (4/4) | 1/4[C4,E4,G4] R1/2 && 1/4[C2,G2,C3] R1/2 |: a quarter note C major chord in the 4th octave in the treble clef, and a quarter note C major chord in the 2nd octave in the bass clef.
```
***

As a professional classical music song writer, your job is to give the users very good songs. You must follow these instructions:
- Learn MeloCode in detail, become a master of MeloCode, take your time to learn! Read the provided examples in the MeloCode description very CAREFULLY. DO NOT VIOLATE THE RULES!
- You answer in MeloCode ONLY - no English.
- Please use ALL capabilities that MeloCode offer, the songs you create are advanced.
- Use Chords in both clefs. Be Careful of duration of the chords. 
- PLEASE, PLEASE, PLEASE, make sure the duration of each bar is correct.  

"""

def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0.2):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, # this is the degree of randomness of the model's output
    )
    #print(str(response.choices[0].message))
    return response.choices[0].message["content"]


user_prompt= """ 
  As a songwriter, you have 7 tasks. Tasks 1 to 6 are supposed to prepare you for task 7.
  Task 1: Define 3/4 time tigniture in details. 
  Task 2: List the notes in the E-Minor scale.
  Task 3: Write a few sample chords with various durations in MeloCode. Remember, duration comes before the chord; example: 1/4[C4,E4,G4]
  Task 4: Write a few sample measures in '3/4' time signiture in MeloCode. The sum of durations in each bar for each hand must be equal to three quarter note beats per measure, use your response to task 1 as reference.
  Task 5: Write a few sample measures containing chords in '3/4' time signiture in MeloCode. The sum of durations in each bar for each hand must be equal to three quarter note beats per measure.
  Task 6: Write a few sample measures with both treble (write-hand) and bass (left-hand) clefs in '3/4' time signiture. The sum of durations in each bar for each hand must be equal to three quarter note beats per measure.
  Task 7: Given your learnings throughout tasks 1 to 6, write a lovely and emotional song in MeloCode in the E-Minor scale and in '3/4' time signiture. The sum of durations in each bar for each hand must be equal to three quarter note beats per measure. Do not forget this general format for each measure: |[right-hand] && [left-hand]|. Don't forget about Chords' durations (e.g. 1/4[]). And remember, your output must be all in MeloCode, no English comments. 
"""

messages = [
    {'role': 'system', 'content':system_message},
    {'role': 'user', 'content': user_prompt},
]

print(get_completion_from_messages(messages=messages))
