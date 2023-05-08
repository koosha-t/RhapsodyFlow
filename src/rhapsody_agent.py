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


def count_measures(melocode):
    measure_pattern = r'\|'
    measures = re.findall(measure_pattern, melocode)
    return len(measures)

