from .exceptions import *
import random


class GuessAttempt(object):
    def __init__(self, letter, hit=None, miss=None):
        if hit == True and miss == True:
            raise InvalidGuessAttempt  
        self.letter=letter.lower()
        self.hit=hit
        self.miss=miss
       
            
    def is_hit(self):
        if self.hit == True:
            return True
        return False
    
    def is_miss(self):
        if self.miss == True:
            return True
        return False
    

class GuessWord(object):
    def __init__(self, word=None):
        if not word:
            raise InvalidWordException
        self.answer=word
        self.masked="*"*len(word)

       
    def perform_attempt(self, character):
        if len(character) > 1:
            raise InvalidGuessedLetterException
        char1=character.lower()
        answer_word1=self.answer.lower()
        count1=answer_word1.count(char1)
        answer_list=list(answer_word1)
        masked_list=list(self.masked)
        for i in range(len(answer_list)):
            itr=0
            if answer_list[i] == char1 and itr < count1:
                masked_list[i] = char1
            itr+=1
        masked_answer="".join(masked_list)
        if masked_answer == self.masked:
            return GuessAttempt(char1, False, True)
        else:
            self.masked=masked_answer
            return GuessAttempt(char1, True, False)


class HangmanGame(object):
    WORD_LIST = ['rmotr', 'python', 'awesome']
    def __init__(self, word_list=None, number_of_guesses=5):
        if word_list == None:
            word_list=self.WORD_LIST
        self.remaining_misses = number_of_guesses
        self.previous_guesses=[]
        select_word=HangmanGame.select_random_word(word_list)
        self.word=GuessWord(select_word)

        
    @classmethod
    def select_random_word(cls, word_list):
        if len(word_list) == 0:
            raise InvalidListOfWordsException
        return random.choice(word_list)

    def guess(self, letter):
        if self.is_finished():
            raise GameFinishedException()
        attempt = self.word.perform_attempt(letter)
        self.previous_guesses.append(letter.lower())
        if attempt.is_miss():
            self.remaining_misses-=1
            if self.is_lost():
                raise GameLostException()
        if self.is_won():
            raise GameWonException()
        return attempt
    
    def is_finished(self):
        if self.is_won() or self.is_lost():
            return True
        return False
    
    def is_won(self):
        if self.word.answer==self.word.masked:
            return True
        return False
    
    def is_lost(self):
        if self.remaining_misses < 1:
            return True
        return False