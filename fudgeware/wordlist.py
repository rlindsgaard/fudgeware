import os

here = os.path.dirname(os.path.abspath(__file__))

# TODO: Obtain wordlists from eff.org and compare with hash
# on first use.
builtin_wordlists = {
    'long': {
        'dice': 5,
        'source': os.path.join(here, 'eff_large_wordlist.txt'),
    },
    'short': {
        'dice': 4,
        'source': os.path.join(here, 'eff_short_wordlist_1.txt'),
    },
    'short-prefix': {
        'dice': 4,
        'source': os.path.join(here, 'eff_short_wordlist_2_0.txt'),
    }
}


class Wordlist(object):
    """A wordlist to lookup

    The wordlist is expected to be in the format

    iiiiii value

    where `i` is an integer and `value` is the value
    returned.
    """

    def __init__(self, filename):
        self.wordlist = {}
        self.read_file(filename)

    def read_file(self, filename):
        """Read a wordlist file and store in memory."""
        with open(filename, mode='r') as f:
            for line in f:
                key, word = line.split()
                self.wordlist[key] = word

    def from_roll(self, roll):
        """Get a value from the wordlist based on a roll"""
        roll_str = ''.join(map(str, roll))
        return self.wordlist[roll_str]
