


def max_occ(votes=[]):
    p = {}

    for vote in votes:
        try:
            votes[vote] += 1
        except KeyError:
            votes[vote] = 1

    return p