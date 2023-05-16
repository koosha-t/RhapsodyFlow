
class MusicBluePrint:

    def __init__(self, scale, time_signature, tempo, genre, mood, inspired_by):
        """
            scale: EMinor, or CMajor, or ...
            time_signature: '4/4' or '3/4' or etc.
            tempo: 80, 116, 140, etc.
            genre: classic or pop
            mood: romance, love, epic, happy, sad, aggressive, calm, relaxed, etc...
            inspired_by: Chopin, Mozart, Yan Tiersen, etc.
        """
        self.scale = scale
        self.time_signature = time_signature
        self.tempo = tempo
        self.genre = genre 
        self.mood = mood
        self.inspired_by = inspired_by
