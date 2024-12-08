import pandas as pd
import numpy as np
class die():
    """Die object. Goal is to create an object that can be _rolled_ to 
    produce a random output of results based on the faces of the die.
    
    Methods: __init__, change_weight, roll_die

    Callable attributes:
        n_sides: number of sides of the die object
    """
    
    def __init__(self, faces):
        """
        __init__ takes a NumPy array of values equal to the faces of a die
        object. Each face is initially given a weight of 1. This is passed 
        into a DataFrame private to the object for producing weighted rolls.

        Arguments: faces- NumPy array of unique sides of a die.
        Outputs: None
        """
        #take array of faces
        #number of sides is equal to length of array
        #weight is equal to 1 for each face to begin with
        if(type(faces)!=np.ndarray):
            raise TypeError("Die sides/faces must be submitted in a NumPy array.")       
        elif(len(set(faces))!=len(faces)):
            raise ValueError("Dice sides are not distinct!")
        else:
            self.n_sides = len(faces)
            #self.probs = [1/len(faces) for i in faces]
            self._die_info = pd.DataFrame({
             'faces': faces,
             'weights':[1 for i in faces]})
             #'probs': self.probs}
        

    def change_weight(self, face, newweight):
        """
        Given a face value and weight, update the weight for that particular side 
        of the die.
        Arguments: 
                    face- value of the side of a die
                    newweight- castable number for new weight 
        Outputs: None
        """
        
        #Check if it's numeric or castable string
        if(type(newweight)==str and newweight.isdigit()==False):
            raise TypeError("Proposed new weight must be a positive number")
        
        elif (newweight < 0 or type(newweight) not in(int, float, str)):
            raise TypeError("Proposed new weight must be a positive number")
        #Check to see if face entered is in the list and if not raise index error
        if(face not in self._die_info.values):
            raise IndexError('Side entered does not exist in die!')
        
        
        else:
            faceindex=self._die_info.index[self._die_info['faces'] == face].tolist()[0]
            self._die_info.at[faceindex,'weights']=int(newweight)

            
        
    
    def roll_die(self, n_rolls=1):
        """Roll a die one or more times and return the results.
        
        Arguments: n_rolls- number of times the die should be rolled (default 1)
        Outputs: a list of all values randomly obtained n times
        """
        results = []
        for i in range(n_rolls):
            result = self._die_info.faces.sample(weights=self._die_info.weights,replace=True).values[0]
            results.append(result)
        return list(results)

    def current_state(self):
        """
        Returns the current list of die sides and weights
        Arguments: None
        Outputs: Dataframe of die sides and weights
        """
        return self._die_info

class game():
    """Game object designed to take one or more dice objects and roll all dice objects
    at once. The results can then be viewed.
    
    Methods: __init__, play, most_recent_play
    Callable attributes:
        dice- list of dice for rolling
        num_dice- number of dice per game


    """
   
    def __init__(self, dice):
        """
        Creates a game object, which is simply a collection of dice. 
        Arguments: List of dice with sides and weights
        Outputs:None
        """
        self.dice = dice
        self.num_dice=len(dice)
        #_results is the private instantiation of the empty list where roll results will be appended in play()
        self._results=[]
        self._df="No dice have been rolled yet!"
        #Check to make sure the dice are the same
        #empty lists for sides and faces
        sides=[]
        faces=[]
        for i in self.dice:
            sides.append(i.n_sides,)
            faces.append(tuple(i._die_info['faces']))
        if(len(set(faces))!=1 or len(set(sides)) !=1):
            raise ValueError("Dice are not the same!")

    def play(self,n_rolls=1):
        """
        Clears any previous roll results.
        Rolls all dice in the dice list a given number of times  and saves the results

        Arguments: n_rolls- number of times all dice should be rolled
        Outputs: None
        """
         #Clear last results
        self._results.clear()
        
        for die in self.dice:
            dierolls=die.roll_die(n_rolls)
            self._results.append(dierolls)
        self._df=pd.DataFrame(self._results)
        #results in a df where each row is a die's result rather than a roll # so transposing
        self._df=self._df.transpose()
        
        self._df.index.names = ['roll_number']
        #return self.df


    
    def most_recent_play(self,tableformat='wide'):
        """
        Returns the last sets of rolled dice results with two format options.
        'Wide' table format has a row for each roll, with eache die as a column
        'narrow' table format is stacked so that the result of the roll is the only 
        and the roll number and die number

        Arguments: tableformat- specifies wide or narrow table, with wide as default
        Outputs: Dataframe of results in wide or narrow form
        """
        if(tableformat not in('narrow','wide')):
            raise ValueError('most_recent_play takes input of narrow or wide.')
        elif(tableformat=='wide'):
            return self._df
        else:
            #Probably easier way to do this but I needed the roll # as an explicit column for my solution
            #instantiated an empty list and filled it with the indices from the df of most recent results
            rollnum=[]
            flat=self._df.copy()
            for i in range(0,len(self._df.index)):
                rollnum.append(i)
            flat['rollnum']=rollnum
            flat['rollnum']=flat.index
            #using the melt function to create a narrow version of the table
            narrow=pd.melt(flat,id_vars=['rollnum'],var_name='dienum',value_name='result')
            narrow=narrow.set_index(['rollnum','dienum'])
            return narrow
class analyzer():
    """ Analyzer class designed to take game, comprised of a list of dice.
        The class is designed to return statistics of a game played with dice.

        Methods: jackpot, face_counts_per_roll, combo_count, permutation_count

        Callable attributes: 
            game- the game object passed for analyzing
            stats- the most recent result of play from the game object
    """
    
    def __init__(self, gameobj):
        """
        Creates an object that is passed a game to initialize. Saves the last results
        of the game.play() output, as well as the die and side information

        Arguments: gameobj- object of type 'game'
        Outputs: None
        """
        self.game = gameobj
        if(type(self.game)==game):
            self.stats=self.game.most_recent_play()
            #get a list of faces for the dice in the game object and save it to a private variable
            self._faces=list(self.game.dice[1].current_state().iloc[:,0])
            #get the dice in list form to use in other methods, stored privately
            self._dicelist=list(self.stats.columns.values)
        else: 
            raise ValueError('Must be of type game!')
        
    def jackpot(self):
        """
        Based on the last play() method, calculates how many times all dice in the
        game object got the same face value for a given roll.

        Arguments: None
        Outputs: Count of times all dice rolled the same face value
        """
        jkptcount=0
        #Need to iterate through rows (or transposed columns)
        #If the length of distinct values is equal to 1, the jackpot counter goes up by 1
        for i in range(0,len(self.stats.index)):
            col=list(self.stats.loc[i,:])
            if(len(set(col))==1):
                jkptcount +=1
        return int(jkptcount) 
    
    def face_counts_per_roll(self):
        """
        Takes the last play result from the game object and calculates how many
        times each face was rolled, per roll.

        Arguments: None
        Outputs: Dataframe with with the faces and counts per roll
        """
        #Rows: # of times dice were rolled
        #Columns: Equal to # of sides in dice
        counts = self.stats.copy()
        faces = self._faces
        num_dice = self._dicelist
        
        # get most recent play, melt it down, and add count
        temp = counts.reset_index()

        temp = temp.melt(id_vars=['roll_number'], value_vars=num_dice,
                        var_name='die_number', value_name='result')
        temp['count'] = 1

        # set up dataframes for unique roll numbers & faces
        counts = pd.DataFrame(temp['roll_number'].unique(), columns=['roll_number'])
        faces = pd.DataFrame(self._faces, columns=['faces'])

        # add common key & then cross join
        # (so all faces are included even if they aren't rolled)
        counts['key'] = 1
        faces['key'] = 1
        staging = counts.merge(faces, on='key', how='outer').drop('key', axis=1)

        # now join counts into final df
        final = staging.merge(temp, left_on=['roll_number', 'faces'], right_on=['roll_number', 'result'], how='left')

        # fill in zeroes for nulls in count col
        final['count'] = final['count'].fillna(0)

        # drop unneeded columns
        final = final[['roll_number', 'faces', 'count']]

        final = final.pivot_table(index='roll_number', columns='faces', values='count', aggfunc='sum')
        
        
        #1) Get list of distinct values that were rolled (iterate through entire dataframe) and sort it
        #2) Make a list, from 0 to n-1 (where n is the df size) 
        return final

    def combo_count(self):
        """
        Takes the most recent play from the game object and calculates how many times
        each combination of sides was rolled. This is not order dependent (i.e. 1-2-1
        is equivalent to 2-1-1)

        Arguments: None
        Outputs: Dataframe with with the combinations and counts 
        """
        #currently not using num_dice
        num_dice = self._dicelist
        combos=self.stats.copy()
        
        # make order independent roll df
        combos['ordered_rolls'] = pd.Series([tuple(x) for x in np.sort(combos.values, 1)])
        combos['count'] = 1

        combos = combos[['ordered_rolls', 'count']]

        # now group by the new dies
        combo_counts = combos.groupby('ordered_rolls')['count'].count()
        return combo_counts

    
    def permutation_count(self):
        """
        Takes the most recent play from the game object and calculates how many times
        each permutation of sides was rolled. This IS order dependent (i.e. 1-2-1
        is NOT equivalent to 2-1-1)

        Arguments: None
        Outputs: Dataframe with with the permutations and counts 
        """
        perms=self.stats.copy()
        perms['rolls'] = pd.Series([tuple(x) for x in perms.values])
        perms['count'] = 1
        perm_counts=perms.groupby(['rolls']).count()
        perm_counts=perm_counts[['count']]

        
        return perm_counts