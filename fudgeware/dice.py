import hashlib


class DiceContainer(object):
    """
    Container simulating rolling multiple dice at once.
    """
    def __init__(self, dice=None):
        """
        Create a new container object

        :param dice: A list of dice to add.
        :type dice: list[WeightedDie]
        """
        self.dice = dice or []

    def add(self, die) -> ():
        """Add a new die."""
        self.dice.append(die)

    def roll(self) -> list[int]:
        """Roll all the dice.

        :return: The current roll for all the dice in the container.
        :rtype: list[int]
        """
        for die in self.dice:
            die.roll()
        return self.eyes()

    def eyes(self) -> list[int]:
        """
        Return the current roll for all the dice.

        The eyes are returned in the order the dice have been added.

        :rtype: list[int]
        """
        return [
            d.eyes()
            for d in self.dice
        ]


class WeightedDie(object):
    """Simulate a single weighted (or loaded) 6-sided die.

    Rolls are determined by the `hashing_algorithm` supplied
    used as a deterministic random number generator.

    The die maintains an internal state which is updated on every
    roll. Given the same seed and hashing_algorithm, the rolls
    will be identical.
    """
    def __init__(self, seed, hashing_algorithm):
        cipher = hashlib.new(hashing_algorithm)
        cipher.update(seed)
        self.cipher = cipher

    def roll(self):
        """
        Roll the die

        Updates the current state with.

        :return:
        :rtype:
        """
        self.cipher.update(self.cipher.digest())
        return self.eyes()

    def eyes(self):
        """
        Return the current roll.

        The roll is computed by interpreting the current
        digest as a large integer and performing modulus operation.

        :rtype: int
        """
        intdigest = int.from_bytes(self.cipher.digest(), 'big')
        return (intdigest % 6) + 1
