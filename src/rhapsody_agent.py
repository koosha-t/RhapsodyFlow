import re

def fraction_to_float(fraction):
    numerator, denominator = fraction.split('/')
    return float(numerator) / float(denominator)

def find_violating_measures(time_signature, melocode):
    measures = [measure.strip() for measure in melocode.split('|') if measure.strip()]
    violating_measures = {}
    beat_sum_target = float(time_signature.split('/')[0]) / float(time_signature.split('/')[1])

    for index, measure in enumerate(measures, start=1):

        hands = measure.split('&&')
        
        for hand in hands:
            beat_sum = 0
            for duration in re.findall(r'(\d+/\d+)', hand):
                beat_sum += fraction_to_float(duration)
            
            if beat_sum != beat_sum_target:
                violating_measures[index] = measure
                break
                
    return violating_measures

time_signature = "4/4"
melocode = '''
(4/4) | 1/4C4 1/4E4 1/4G4 1/4C5 && 1/4C3 1/4E3 1/4G3 1/4C4 | 1/4D4 1/4F4 1/4A4 1/4D5 && 1/4D3 1/4F3 1/4A3 1/4D4 | 1/4E4 1/4G4 1/4B4 1/4E5 && 1/4E3 1/4G3 1/4B3 1/4E4 | 1/4C4 1/4E4 1/4G4 1/2C5 && 1/4C3 1/4E3 1/4G3 1/2C4 |
'''

violating_measures = find_violating_measures(time_signature, melocode)
print(violating_measures)




# import re

# def find_violating_measures(time_signature, melocode):
#     def duration_of(element):
#         duration = re.match(r'(\d*/\d*)', element)
#         return fraction_to_float(duration.group(1)) if duration else 0

#     def fraction_to_float(fraction):
#         numerator, denominator = fraction.split('/')
#         return float(numerator) / float(denominator)

#     measures = re.split(r'\s*\|\s*', melocode.strip())[1:-1]
#     beats_per_measure, beat_value = time_signature.split('/')
#     beat_sum = float(beats_per_measure) * (1 / float(beat_value))

#     violating_measures = {}
#     for i, measure in enumerate(measures):
#         elements = re.findall(r'(\d*/\d*[\w#bR]+\d*)', measure)
#         duration_sum = sum([duration_of(element) for element in elements])

#         if round(duration_sum, 2) != round(beat_sum, 2):
#             violating_measures[i + 1] = measure

#     return violating_measures

# Example usage:

# time_signature = "4/4"
# melocode = "(4/4) | 1/4C4 1/4E4 1/4G4 1/4C5 | 1/4E4 1/4G4 1/4C5 1/4E5 1/8A4 | R1/4 1/4D4 1/8F4 1/8A4 1/4D5 |"
# violating_measures = find_violating_measures(time_signature, melocode)
# print(violating_measures)

# time_signature = "3/4"
# melocode = "(3/4) | 1/4C4 1/4E4 1/4G4 | 1/2C4 1/4D4 1/4E4 | R1/4 1/4F4 1/4G4 1/4A4 1/4B4 | 1/4C5 1/4D5 1/4E5 |"
# violating_measures = find_violating_measures(time_signature, melocode)
# print(violating_measures)
