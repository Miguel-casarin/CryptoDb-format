

def lower(intra_day):
    if not intra_day:
        return None
    return min(intra_day.values())

def max(intra_day):
    if not intra_day:
        return None
    return max(intra_day.values())
