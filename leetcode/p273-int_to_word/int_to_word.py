
LOOKUP_TABLE_LESS_THAN_20 = [
    'Zero', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 
    'Ten', 'Eleven', 'Twelve', 'Thirteen', 'Fourteen', 'Fifteen', 'Sixteen', 'Seventeen', 'Eighteen', 'Nineteen'
]

LOOKUP_TABLE_TENS = [
    'Zero', 'Ten', 'Twenty', 'Thirty', 'Forty', 'Fifty', 'Sixty', 'Seventy', 'Eighty', 'Ninty'
]

def numberToWord(num):
    if num == 0:
        return 'Zero'
    elif num < 20:
        return LOOKUP_TABLE_LESS_THAN_20[num]
    elif num < 100:
        t = num // 10
        r = num % 10
        if r == 0:
            return f'{LOOKUP_TABLE_TENS[num // 10]}'
        else:
            return f'{LOOKUP_TABLE_TENS[num // 10]} {LOOKUP_TABLE_LESS_THAN_20[num % 10]}'
    elif num < 1000:
        h = num // 100
        r = num % 100
        if r == 0:
            return f'{numberToWord(h)} Hundred'
        else:
            return f'{numberToWord(h)} Hundred {numberToWord(r)}'
        
    elif num < 10**6:
        t = num // 1000
        r = num % 1000
        if r == 0:
            return f'{numberToWord(t)} Thousand'
        else:
            return f'{numberToWord(t)} Thousand {numberToWord(r)}'
    elif num < 10**9:
        m = num // 10**6
        r = num % 10**6
        if r == 0:
            return f'{numberToWord(m)} Million'
        else:
            return f'{numberToWord(m)} Million {numberToWord(r)}'
    else:
        b = num // 10**9
        r = num % 10**9
        if r == 0:
            return f'{numberToWord(b)} Billion'
        else:
            return f'{numberToWord(b)} Billion {numberToWord(r)}'
    
def main():
    test_cases = [x for x in range(26)] + [x for x in range(90,120)] + [x for x in range(990, 1010)] + [1234567890]

    for case in test_cases:
        print(f'{case}: \"{numberToWord(case)}\"')

if __name__ == '__main__':
    main()
