import random, os, sys

TILE_BLANK = 0
TILE_DOUBLE_LETTER = 2
TILE_TRIPLE_LETTER = 3
TILE_DOUBLE_WORD = 4
TILE_TRIPLE_WORD = 6
TILE_START = 7

tileScores = [[6,0,0,2,0,0,0,6,0,0,0,2,0,0,6],
[0,4,0,0,0,3,0,0,0,3,0,0,0,4,0],
[0,0,4,0,0,0,2,0,2,0,0,0,4,0,0],
[2,0,0,4,0,0,0,2,0,0,0,4,0,0,2],
[0,0,0,0,4,0,0,0,0,0,4,0,0,0,0],
[0,3,0,0,0,3,0,0,0,3,0,0,0,3,0],
[0,0,2,0,0,0,2,0,2,0,0,0,2,0,0],
[6,0,0,2,0,0,0,7,0,0,0,2,0,0,6],
[0,0,2,0,0,0,2,0,2,0,0,0,2,0,0],
[0,3,0,0,0,3,0,0,0,3,0,0,0,3,0],
[0,0,0,0,4,0,0,0,0,0,4,0,0,0,0],
[2,0,0,4,0,0,0,2,0,0,0,4,0,0,2],
[0,0,4,0,0,0,2,0,2,0,0,0,4,0,0],
[0,4,0,0,0,3,0,0,0,3,0,0,0,4,0],
[6,0,0,2,0,0,0,6,0,0,0,2,0,0,6]]

letterScores = {'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4,
'i': 1,'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1,
's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10}

letterDistributions = {'a': 9, 'b': 2, 'c': 2, 'd': 4, 'e': 12, 'f': 2, 'g': 3,
'h': 2, 'i': 9, 'j': 1, 'k': 1, 'l': 4, 'm': 2, 'n': 6, 'o': 8, 'p': 2, 'q': 1,
'r': 6, 's': 4, 't': 6, 'u': 4, 'v': 2, 'w': 2, 'x': 1, 'y': 2, 'z': 1}

class Game:
    __lettersRemaining = None
    __currentPlayer = None
    __players = None
    __board = None
    __dictionary = None


    def getBoard(self):
        return self.__board

    def setBoard(self, value):
        self.__board = value

    board = property(getBoard, setBoard)


    def getPlayers(self):
        return self.__players

    def setPlayers(self, value):
        self.__players = value

    players = property(getPlayers, setPlayers)


    def getCurrentPlayer(self):
        return self.__currentPlayer

    def setCurrentPlayer(self, value):
        self.__currentPlayer = value

    currentPlayer = property(getCurrentPlayer, setCurrentPlayer)


    def getDictionary(self):
        return self.__dictionary

    def setdictionary(self, value):
        self.__dictionary = value

    dictionary = property(getDictionary, setdictionary)


    def __init__(self, playerCount):
        """Set up default game state."""
        self.__board = Board()

        # Copy letter distribution dictionary into letters remaining dictionary
        self.__lettersRemaining = {}

        for letter in letterDistributions:
            self.__lettersRemaining[letter] = letterDistributions[letter]

        # Create player objects
        self.__players = [Player(self) for i in range(0, playerCount)]

        self.__currentPlayer = playerCount - 1

        self.__dictionary = WordDictionary()


    def getRandomLetter(self):
        """Get a random letter from the letter bag and reduce that letter's
        remaining count by 1."""

        # Create a string containing a list of all characters that have at least
        # one letter remaining
        choices = ""

        for letter in self.__lettersRemaining:
            if self.__lettersRemaining[letter] > 0:
                choices = choices + letter

        # Choose random letter from the list of choices
        letter = random.choice(choices)

        self.__lettersRemaining[letter] = self.__lettersRemaining[letter] - 1
        return letter


    def getRemainingLetterCount(self):
        """Get the number of letters left in the bag."""
        remaining = 0

        for letter in self.__lettersRemaining:
            remaining += self.__lettersRemaining[letter]

        return remaining


    def newMove(self):
        """Select the next player and create a move for that player."""

        # Wrap-around the player index if necessary
        if self.__currentPlayer == len(self.__players) - 1:
            self.__currentPlayer = 0
        else:
            self.__currentPlayer += 1

        print("Creating move for player " + str(self.__currentPlayer))

        return Move(self, self.__players[self.__currentPlayer])


class WordDictionary:
    __words = None

    def __init__(self):
        """"Loads the dictionary file."""
        file = open(os.path.dirname(sys.argv[0]) + "\\dictionary.txt", "r")
        self.__words = file.readlines()


    def isWord(self, word):
        for i in self.__words:
            if i.replace('\n', '') == word:
                print("Word '" + word + "' is valid")
                return True

        print("Word '" + word + "' is not valid.")
        return False


class Board:
    __tiles = None
    __tileScores = None


    def get_tiles(self):
        return self.__tiles

    def set_tiles(self, value):
        self.__tiles = value

    tiles = property(get_tiles, set_tiles)


    def __init__(self):
        # Initialise tile array
        self.__tiles = [[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
        [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
        [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
        [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
        [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
        [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
        [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
        [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
        [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
        [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
        [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
        [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
        [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
        [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
        [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ']]

        # Copy tile scores
        self.__tileScores = []

        for row in tileScores:
            self.__tileScores.append([i for i in row])


    def print(self):
        output = ""

        for y in range(0, len(self.__tiles)):
            for x in range(0, len(self.__tiles[y])):

                # Get the letter at the current co-ordinates
                item = self.__tiles[y][x]

                if item == ' ':
                    # Try getting a tile score as there is no letter placed
                    item = str(self.__tileScores[y][x])

                    if item == '0': item = '.'

                output += item
            output += '\n'

        print(output)


    def getLetter(self, x, y):
        """Get the letter at the specified co-ordinates."""

        # Ensure that the co-ordinates fit in the grid
        if len(self.__tiles) < y:
            raise ValueError("Read outside horizontal grid at y co-ord " + str(y))
        if len(self.__tiles[y]) < x:
            raise ValueError("Read outside vertical grid at x co-ord " + str(x))

        return(self.__tiles[y][x])


    def placeLetter(self, letter, x, y):
        """Place the supplied letter at the specified co-ordinates."""

        # Ensure that the letter fits in the grid
        if len(self.__tiles) < y:
            raise ValueError("Letter outside horizontal grid at y co-ord " + str(y))
        if len(self.__tiles[y]) < x:
            raise ValueError("Letter outside vertical grid at x co-ord " + str(x))
        if self.__tiles[y][x] != ' ':
            raise ValueError("Grid not empty at co-ords " + str(x) + "," + str(y))

        # Update the grid
        self.__tiles[y][x] = letter


    def clearLetter(self, x, y):
        """Blank the tile at the specified co-ordinates."""

        # Ensure that the letter fits in the grid
        if len(self.__tiles) < y:
            raise ValueError("Letter outside horizontal grid at y co-ord " + str(y))
        if len(self.__tiles[y]) < x:
            raise ValueError("Letter outside vertical grid at x co-ord " + str(x))

        self.__tiles[y][x] = ' '


    def clearTileScore(self, x, y):
        """Remove the tile score at the specified co-ordinates so that it does
        not alter future scores."""
        self.__tileScores[y][x] = 0


    def getHorizontalWordLength(self, x, y):
        """Get the length of the word starting at x,y."""

        length = 0

        while x < len(self.__tiles[y]) and self.__tiles[y][x] != ' ':
            x += 1
            length += 1

        return(length)


    def getVerticalWordLength(self, x, y):
        """Get the length of the word starting at x,y."""

        length = 0

        while y < len(self.__tiles) and self.__tiles[y][x] != ' ':
            y += 1
            length += 1

        return(length)


    def getHorizontalWordStart(self, x, y):
        """Get the co-ords of the first letter in the word that contains the
        given co-ordinates."""

        while x > 0 and self.__tiles[y][x - 1] != ' ':
            x -= 1

        return({'x': x, 'y': y})


    def getVerticalWordStart(self, x, y):
        """Get the co-ords of the first letter in the word that contains the
        given co-ordinates."""

        while x > 0 and self.__tiles[y - 1][x] != ' ':
            y -= 1

        return({'x': x, 'y': y})


    def getHorizontalWord(self, x, y):
        """Get the horizontal word containing x,y."""

        # Get the start co-ordinates and length of the word
        wordStart = self.getHorizontalWordStart(x, y)
        wordLength = self.getHorizontalWordLength(x, y)

        # Collect the letters of the word
        word = ""
        for i in range(wordStart['x'], wordStart['x'] + wordLength):
            word = word + self.getLetter(i, y)

        return word


    def getVerticalWord(self, x, y):
        """Get the vertical word containing x,y."""

        # Get the start co-ordinates and length of the word
        wordStart = self.getVerticalWordStart(x, y)
        wordLength = self.getVerticalWordLength(x, y)

        # Collect the letters of the word
        word = ""
        for i in range(wordStart['y'], wordStart['y'] + wordLength):
            word = word + self.getLetter(x, i)

        return word


    def scoreHorizontalWord(self, x, y):
        """Score the horizontal word containing x,y."""

        # If the length of the word is 1, the score is 0
        wordLength = self.getHorizontalWordLength(x, y)

        if wordLength == 1:
            return 0

        wordStart = self.getHorizontalWordStart(x, y)

        # Score the word
        isDoubleWord = False
        isTripleWord = False
        isStart = False
        score = 0

        # Score individual letters
        for i in range(wordStart['x'], wordStart['x'] + wordLength):
            tileScore = self.scoreTile(i, y)
            score += tileScore['score']

            isDoubleWord = isDoubleWord or tileScore['isDoubleWord']
            isTripleWord = isTripleWord or tileScore['isTripleWord']
            isStart = isStart or tileScore['isStart']

        # Multiply any word scores
        if isDoubleWord:
            score *= 2
        if isTripleWord:
            score *= 3
        if isStart:
            score *= 2

        return(score)


    def scoreVerticalWord(self, x, y):
        """Score the vertical word containing x,y."""

        # If the length of the word is 1, the score is 0
        wordLength = self.getVerticalWordLength(x, y)

        if wordLength == 1:
            return 0

        wordStart = self.getVerticalWordStart(x, y)

        # Score the word
        isDoubleWord = False
        isTripleWord = False
        isStart = False
        score = 0

        # Score individual letters
        for i in range(wordStart['y'], wordStart['y'] + wordLength):
            tileScore = self.scoreTile(x, i)
            score += tileScore['score']

            isDoubleWord = isDoubleWord or tileScore['isDoubleWord']
            isTripleWord = isTripleWord or tileScore['isTripleWord']
            isStart = isStart or tileScore['isStart']

        # Multiply any word scores
        if isDoubleWord:
            score *= 2
        if isTripleWord:
            score *= 3
        if isStart:
            score *= 2

        return(score)


    def scoreTile(self, x, y):

        isDoubleWord = False
        isTripleWord = False
        isStart = False

        # Get the score for the letter
        score = letterScores[self.getLetter(x, y)]

        # Does the tile have a bonus?
        tile = self.__tileScores[y][x]
        if tile == TILE_DOUBLE_LETTER:
            score *= 2
        elif tile == TILE_TRIPLE_LETTER:
            score *= 3
        elif tile == TILE_DOUBLE_WORD:
            isDoubleWord = True
        elif tile == TILE_TRIPLE_WORD:
            isTripleWord = True
        elif tile == TILE_START:
            isStart = True

        return({'score': score, 'isDoubleWord': isDoubleWord,
            'isTripleWord': isTripleWord, 'isStart': isStart})


class Player:
    __score = 0
    __tiles = None
    __game = None


    def get_tiles(self):
        return self.__tiles

    def set_tiles(self, value):
        self.__tiles = value

    tiles = property(get_tiles, set_tiles)


    def __init__(self, game):
        """Initial setup.  Populates tiles with random letters."""

        self.__game = game

        # Populate tiles with random letters
        self.__tiles = [game.getRandomLetter() for i in range(0, 7)]

        # TODO: REMOVE THIS
        self.__tiles.extend(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
            'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v'
            'w', 'x', 'y', 'z'])


class Move:
    __game = None
    __player = None
    __score = 0
    __placements = None
    __viableLetters = None

    def __init__(self, game, player):
        self.__game = game
        self.__player = player
        self.__placements = []
        self.__viableLetters = []

        for i in player.tiles:
            self.__viableLetters.append(i)

    def placeLetter(self, letter, x, y):

        # Ensure that the letter is in the list of viable letters and, if so,
        # remove it
        try: self.__viableLetters.remove(letter)
        except ValueError:
            raise ValueError("Player does not possess letter '" + letter + "'")

        # Update the grid
        self.__game.board.placeLetter(letter, x, y)

        # Remember the placement
        self.__placements.append({'letter': letter, 'x': x, 'y': y})


    def commit(self):
        """Try to commit the move to the game."""

        # Check that the move is valid
        if not self.validate():
            self.rollback()
            return False

        # Calculate the score of the move
        self.calculateScore()

        self.clearTileScores()


    def rollback(self):
        """Restores the grid to its previous state."""
        for i in self.__placements:
            self.__game.board.clearLetter(i['x'], i['y'])


    def clearTileScores(self):
        """Clears the scores for all board positions involved in this move to
        ensure that they are not counted in future moves."""
        for i in self.__placements:
            self.__game.board.clearTileScore(i['x'], i['y'])


    def validate(self):
        direction = self.getPlacementDirection()

        if direction == 0:

            # Validate the horizontal word
            word = self.__game.board.getHorizontalWord(self.__placements[0]['x'], self.__placements[0]['y'])

            if not self.__game.dictionary.isWord(word):
                return False

            # Validate the vertical words adjacent to the horizontal word
            for i in self.__placements:
                word = self.__game.board.getVerticalWord(i['x'], i['y'])
                if len(word) > 1:
                    if not self.__game.dictionary.isWord(word):
                         return False

        else:
            # Validate the vertical word
            word = self.__game.board.getVerticalWord(self.__placements[0]['x'], self.__placements[0]['y'])

            if not self.__game.dictionary.isWord(word):
                return False

            # Validate the horizontal words adjacent to the vertical word
            for i in self.__placements:
                word = self.__game.board.getHorizontalWord(i['x'], i['y'])
                if len(word) > 1:
                    if not self.__game.dictionary.isWord(word):
                        return False

        return True


    def calculateScore(self):
        direction = self.getPlacementDirection()
        score = 0

        if direction == 0:

            # Score horizontal word
            score += self.__game.board.scoreHorizontalWord(self.__placements[0]['x'], self.__placements[0]['y'])

            # Score the vertical words adjacent to the horizontal word
            for i in self.__placements:
                score += self.__game.board.scoreVerticalWord(i['x'], i['y'])
        else:

            # Score vertical word
            score += self.__game.board.scoreVerticalWord(self.__placements[0]['x'], self.__placements[0]['y'])

            # Score the horizontal words adjacent to the vertical word
            for i in self.__placements:
                score += self.__game.board.scoreHorizontalWord(i['x'], i['y'])

        print(score)


    def getPlacementDirection(self):
        """0 indicates horizontal; 1 indicates vertical."""

        # If all letters are in a line, then either the x or y co-ords of one
        # placement multiplied by the number of placements will equal the total
        # x or y co-ordinate for the entire move
        xTotal = 0
        yTotal = 0
        for i in self.__placements:
            xTotal += i['x']
            yTotal += i['y']

        if self.__placements[0]['x'] * len(self.__placements) == xTotal:
            return 1
        elif self.__placements[0]['y'] * len(self.__placements) == yTotal:
            return 0

        # No match means letters are not lined up
        raise Exception("Letters are out of alignment.  Move is invalid.")

game = Game(2)


#print(game.getRemainingLetterCount())
#print(game.players[0].playWordHorizontal("cheese", 9, 11))
#print(game.players[0].playWordHorizontal("cheese", 9, 10))

print("Initial tiles")
print("Player 1:")
print(game.players[0].tiles)

print("Player 2:")
print(game.players[1].tiles)

print("Player " + str(game.currentPlayer + 1) + " places 'bin'")
move = game.newMove()
move.placeLetter('b', 2, 1)
move.placeLetter('i', 2, 2)
move.placeLetter('n', 2, 3)
move.commit()

print("Board state:")
game.board.print()


print("Player " + str(game.currentPlayer + 1) + " places 'chip'")
move = game.newMove()
move.placeLetter('c', 0, 2)
move.placeLetter('h', 1, 2)
move.placeLetter('p', 3, 2)
move.commit()

print("Board state:")
game.board.print()


print("Player " + str(game.currentPlayer + 1) + " places 'chips'")
move = game.newMove()
move.placeLetter('s', 4, 2)
move.commit()

print("Board state:")
game.board.print()