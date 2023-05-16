import re
import pdb

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
                violating_measures[index-1] = measure
                break
    
    return violating_measures


def count_measures(melocode):
    measure_pattern = r'\|'
    measures = re.findall(measure_pattern, melocode)
    return len(measures)



if __name__ == "__main__":
    score ="""
(4/4) | <p> 1/4C4 1/4E4 1/4G4 1/4C5 && 1/4C2 1/4G2 1/4C3 1/4G3 |
1/4[E2,G2,B2,E3] R3/4 && 1/4[E3,G3,B3,E4] R3/4 |
1/8E4 1/16G4 1/16B4 1/8E5 1/16G5 1/16B5 R1/2 && 1/4[E2,G2,B2,E3] R1/2 |
1/8G4 1/16B4 1/16D5 1/8G5 1/16B5 1/16D6 R1/2 && 1/4[G2,B2,D3,G3] R1/2 |
1/8E4 1/16G4 1/16B4 1/8E5 1/16G5 1/16B5 R1/2 && 1/4[E2,G2,B2,E3] R1/2 |
R1/2 1/4E4 1/4G4 1/4B4 && 1/4E2 1/4G2 1/4B2 R1/4 |
1/4G4 1/4B4 1/4D5 && 1/4G2 1/4B2 1/4D3 R1/4 |
1/4E4 1/4G4 1/4B4 && 1/4E2 1/4G2 1/4B2 R1/4 |
1/8E4 1/16G4 1/16B4 1/8E5 1/16G5 1/16B5 R1/2 && 1/4[E2,G2,B2,E3] R1/2 |
<f> 1/4E4 1/4G4 1/4B4 && 1/4E2 1/4G2 1/4B2 R1/4 |
1/4G4 1/4B4 1/4D5 && 1/4G2 1/4B2 1/4D3 R1/4 |
1/4E4 1/4G4 1/4B4 && 1/4E2 1/4G2 1/4B2 R1/4 |
1/4[E2,G2,B2,E3] R3/4 && 1/4[E3,G3,B3,E4] R3/4 | """
    
    print(find_violating_measures('4/4',score))