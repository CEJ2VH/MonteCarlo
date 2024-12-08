import numpy as np, pandas as pd
from MonteCarlo import die, game, analyzer
import unittest

class DiceGameSuite(unittest.TestCase):
    
    def test_1_die_add(self): 
        # Add dice of different kinds
        coinvals=np.array(['heads','tails'])
        dievals=np.array([1,2,3,4,5,6])
        coin1=die(coinvals)
        coin2=die(coinvals)
        die1=die(dievals)
        die2=die(dievals)
        die3=die(dievals)
        #Test if coin is of type die
        self.assertTrue(type(coin1) is die)

    def test_2_die_change_weight(self):
        # change weight of coin 2 and confirm
        coinvals=np.array(['heads','tails'])
        coin2=die(coinvals)
        coin2.change_weight('heads',4)
        self.assertEqual(coin2._die_info['weights'][0], 4)
                
    def test_3_die_roll(self): 
        # Roll a die and confirm the results have the expected length
        rollnum=5
        coinvals=np.array(['heads','tails'])
        coin1=die(coinvals)
        coin1roll=coin1.roll_die(rollnum)
        self.assertEqual(len(coin1roll),rollnum)
        
    def test_4_die_current_state(self): 
        # get last state of a rolled die
        #if a die/coin has not been "rolled" yet, it returns a message saying nothing has been rolled
        coinvals=np.array(['heads','tails'])
        coin1=die(coinvals)
        initstate=coin1.current_state().copy()
        nr=3
        coin1.roll_die(nr)
        nextstate=coin1.current_state()
        self.assertEqual(type(nextstate),type(initstate))
       
        
    def test_5_game_add(self): 
        # Add 2 coins to a game, confirm the array of coins passed matches the number of coins in the game
        dievals=np.array([1,2,3,4,5,6])
        d1=die(dievals)
        d2=die(dievals)
        dietst=[d1,d2]
        game1=game(dietst)
        self.assertEqual(len(dietst),len(game1.dice))

    def test_6_game_play(self):
        # Add some dice to a game, roll 10 times, and make sure the number of times rolled matches the df size
        dievals=np.array([1,2,3,4,5,6])
        d3=die(dievals)
        d4=die(dievals)
        setdie=[d3,d4]
        game2=game(setdie)
        playnum=10
        game2.play(playnum)
        g2=game2.most_recent_play()
        self.assertEqual(playnum,int(g2.shape[0]))
        
    def test_7_most_recent_play(self):
        # Get most recent play and test if the most recent value is correctly
        # typed to game
        dievals=np.array([1,2,3,4,5,6])
        d5=die(dievals)
        d6=die(dievals)
        setdie=[d5,d6]
        game3=game(setdie)
        playnum=10
        game3.play(playnum)
        g3chk = game3.most_recent_play()
        self.assertEqual(type(game3),game)
        
    def test_8_analyzer_add(self):
        #Create dice, a game for the dice, and an analyzer and check type
        dievals=np.array([1,2,3,4,5,6])
        die1=die(dievals)
        die2=die(dievals)
        dielist=[die1,die2]
        game4=game(dielist)
        game4.play(2)
        an1=analyzer(game4)
        self.assertEqual(type(an1),analyzer)
    
    def test_9_analyzer_jackpot(self):
        #Check if jackpot returns an int
        dievals=np.array([1,2,3,4,5,6])
        die1=die(dievals)
        die2=die(dievals)
        dielist=[die1,die2]
        game4=game(dielist)
        game4.play(200)
        an1=analyzer(game4)
        jackpot=an1.jackpot()
        self.assertEqual(type(jackpot),int)
    def test_10_analyzer_face_counts_per_roll(self):
        #Make analyzer and ensure the face counts per roll df
        # has the same # of columns as faces of the die
        dievals=np.array([1,2,3,4,5,6])
        die1=die(dievals)
        die2=die(dievals)
        dielist=[die1,die2]
        game4=game(dielist)
        game4.play(200)
        an1=analyzer(game4)
        self.assertEqual(len(dievals),len(an1.face_counts_per_roll().columns))
    def test_11_analyzer_combo_counts(self):
        #Checking to see if the multi index worked
        #Index name should be 'ordered_rolls'
        dievals=np.array([1,2,3,4,5,6])
        die1=die(dievals)
        die2=die(dievals)
        dielist=[die1,die2]
        game4=game(dielist)
        game4.play(200)
        an1=analyzer(game4)
        self.assertEqual(an1.combo_count().index.name,'ordered_rolls')

    def test_12_analyzer_perm_counts(self):
        #Very similar to combo_count, want to see if the multi index worked
        #Index name should be 'rolls'
        dievals=np.array([1,2,3,4,5,6])
        die1=die(dievals)
        die2=die(dievals)
        dielist=[die1,die2]
        game4=game(dielist)
        game4.play(200)
        an1=analyzer(game4)
        self.assertEqual(an1.permutation_count().index.name,'rolls')
       
if __name__ == '__main__':
    unittest.main(verbosity=3)
