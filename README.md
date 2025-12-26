# Wordle-Dordle-Solver

This Python prgoram is an information theory based solved for both Wordle and Dordle. It uses Shannon Entropy to determine the most optimal guess by calculating which word will on average narrow the list of possible answers the most.

##### Prerequisites

This was written in Python 3.13

```pip install tqdm```

##### Usage

1. Run the script ```python solver.py```
2. Select either ```1``` for Wordle or ```2``` for Dordle.
3. The bot automatically selects the word ```SALET``` by default for optimization. The user needs to enter the pattern seen ingame with numbers:
   - ```0```: Grey (Incorrect)
   - ```1```: Yellow (Wrong Spot)
   - ```2```: Green (Correct Spot)
4. Follow the recommended guesses until the board is solved.

The solver uses the Shannon Entroy Formula to evaluate guesses:

H(X)=−i=1∑n​P(xi​)log2​P(xi​)

##### Troubleshooting and Limitations

The ```words.txt``` was specifically designed with Wordle's set in mind. The Dordle game uses a different word set with added words that is not available. However, the program does still have a high success rate with solving Dordle. 

##### Credits

- ```words.txt``` was taken from GitHub user: https://github.com/cfreshman
