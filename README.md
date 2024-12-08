## MonteCarlo Simulation Package

## Metadata

Package Name: MonteCarlo

Developer: Sarah Hall (CEJ2VH)

## Synopsis  

```
#Make 3 dice using a NumPy array
dt1=die(np.array([1,2,3,4]))
dt2=die(np.array([1,2,3,4]))
dt3=die(np.array([1,2,3,4]))

#Add those dice to a list
dt=[dt1,dt2,dt3]

#Pass the list to a game object. This allows you to "play"
gt=game(dt)
gt.play(10)

#You can pass the game to an analyzer to get other metrics
anlyz=analyzer(gt)
anlyz.combo_count()
```

## Module Metadata 

There are three modules in this package- the die, the game, and the analyzer.  

The die takes a simple array of faces, and can be "rolled"  by randomly selecting one of the faces.  

Each die can be added to a list, which is passed to the game object.  

The game rolls all dice simultaneously the same number of times.  

The most recent roll is recorded as a state of all dice and what face was rolled.  

This can be accessed in narrow or wide data formats.  

## Die Class  

Methods and objects (from the docstring)  

    Die object. Goal is to create an object that can be _rolled_ to 
    produce a random output of results based on the faces of the die.
    
    Methods: __init__, change_weight, roll_die

    Callable attributes:
        n_sides: number of sides of the die object
    
    __init__ takes a NumPy array of values equal to the faces of a die
        object. Each face is initially given a weight of 1. This is passed 
        into a DataFrame private to the object for producing weighted rolls.

    Arguments: faces- NumPy array of unique sides of a die.
        Outputs: None

        __init__ takes a NumPy array of values equal to the faces of a die
        object. Each face is initially given a weight of 1. This is passed 
        into a DataFrame private to the object for producing weighted rolls.

        Arguments: faces- NumPy array of unique sides of a die.
        Outputs: None

     *Change_Weight*
        Given a face value and weight, update the weight for that particular side 
        of the die.
        Arguments: 
                    face- value of the side of a die
                    newweight- castable number for new weight 
        Outputs: None

       Roll a die one or more times and return the results.

    *Current_State*
        
        Arguments: n_rolls- number of times the die should be rolled (default 1)
        Outputs: a list of all values randomly obtained n times

        Returns the current list of die sides and weights
        Arguments: None
        Outputs: Dataframe of die sides and weights
  

## Game Class  
Methods and objects (from the docstring) 
    
    Game object designed to take one or more dice objects and roll all dice objects
    at once. The results can then be viewed.
    
    Methods: __init__, play, most_recent_play
    Callable attributes:
        dice- list of dice for rolling
        num_dice- number of dice per game

    **__init__* Creates a game object, which is simply a collection of dice. 
        Arguments: List of dice with sides and weights
        Outputs:None 

    *play* Clears any previous roll results.
        Rolls all dice in the dice list a given number of times  and saves the results

        Arguments: n_rolls- number of times all dice should be rolled
        Outputs: None  

    *most_recent_play* Returns the last sets of rolled dice results with two format options.
        'Wide' table format has a row for each roll, with eache die as a column
        'narrow' table format is stacked so that the result of the roll is the only 
        and the roll number and die number

        Arguments: tableformat- specifies wide or narrow table, with wide as default
        Outputs: Dataframe of results in wide or narrow form


## Analyzer Class  
Methods and objects (from the docstring) 

    *__init__* Creates an object that is passed a game to initialize. Saves the last results
        of the game.play() output, as well as the die and side information

        Arguments: gameobj- object of type 'game'
        Outputs: None

    *jackpot* Based on the last play() method, calculates how many times all dice in the
        game object got the same face value for a given roll.

    Arguments: None
        Outputs: Count of times all dice rolled the same face value

    *face_counts_per_roll* Takes the last play result from the game object and calculates how many
        times each face was rolled, per roll.

        Arguments: None
        Outputs: Dataframe with with the faces and counts per roll

    *combo_counts* Takes the most recent play from the game object and calculates how many times
        each combination of sides was rolled. This is not order dependent (i.e. 1-2-1
        is equivalent to 2-1-1)

        Arguments: None
        Outputs: Dataframe with with the combinations and counts 
    
    *permutation_counts* Takes the most recent play from the game object and calculates how many times
        each permutation of sides was rolled. This IS order dependent (i.e. 1-2-1
        is NOT equivalent to 2-1-1)

        Arguments: None
        Outputs: Dataframe with with the permutations and counts
