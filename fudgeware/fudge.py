"""Main module."""
from argparse import ArgumentParser
import getpass
import hashlib
import pyperclip
import sys

from fudgeware.dice import DiceContainer, WeightedDie
from fudgeware.wordlist import builtin_wordlists, Wordlist

MASTER_SALT = b'correct horse battery staple'


def main(opts):
    seed_generator = initialise_seed(opts.domain.encode())

    wordlist_config = builtin_wordlists[opts.wordlist]

    wordlist = Wordlist(wordlist_config['source'])
    container = load_dice(seed_generator, wordlist_config['dice'])

    passphrase = generate_passphrase(wordlist, container, opts.words)

    copy_to_clipboard(passphrase)


def initialise_seed(domain):
    # TODO: Store/obtain seed from file
    # TODO^2: Store it in memory in background process
    seed = getpass.getpass('Master: ').encode()

    salt = hashlib.pbkdf2_hmac(
        'sha256',
        seed,
        MASTER_SALT,
        100000,
    )
    salt = hashlib.new('sha512_256')
    salt.update(seed)

    password = getpass.getpass('Password: ').encode()

    genesis_hash = hashlib.pbkdf2_hmac(
        'sha256',
        password,
        salt.digest(),
        100000,
    )

    seed_generator = SeedGenerator(genesis_hash)
    seed_generator.update(domain)

    return seed_generator


class SeedGenerator(object):
    """Wrapper serving as a random number generator."""

    def __init__(self, seed):
        self.generator = hashlib.new('sha512_256')
        self.generator.update(seed)

    def update(self, bs):
        self.generator.update(bs)

    def digest(self):
        d = self.generator.digest()
        self.update(d)
        return d


def load_dice(rng, number_of_dice):
    """Initialize container of loaded dice."""
    container = DiceContainer()
    for _ in range(number_of_dice):
        seed = rng.digest()
        rng.update(seed)

        die = WeightedDie(seed, 'sha512_256')
        container.add(die)

    return container


def generate_passphrase(
    wordlist: Wordlist,
    container: DiceContainer,
    number_of_words: int):
    words = [
        wordlist.from_roll(container.roll())
        for _ in range(number_of_words)
    ]

    return ' '.join(words)


def copy_to_clipboard(passphrase):
    try:
        pyperclip.copy(passphrase)
        print('Passphrase copied to clipboard')
    except pyperclip.PyperclipException:
        print('Could not copy passphrase to clipboard')
        query = input('Print to terminal? (type "yes") ')
        if query != 'yes':
            sys.exit(1)
        print(passphrase)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument(
        '-d', '--domain',
        type=str,
        help='Context for passphrase',
        required=True,
    )
    parser.add_argument(
        '-w', '--words',
        type=int,
        default=6,
        help='Number of words the passphrase consists of.',
    )
    parser.add_argument(
        '--wordlist',
        choices=builtin_wordlists.keys(),
        default='long',
    )
    parser.add_argument(
        '-p', '--print',
        action='store_true',
        default=False,
    )
    main(parser.parse_args())
