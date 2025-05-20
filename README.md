# Tetris AI
An AI that trains against itself using a keras model and reinforcement learning to play the game Tetris. Collects data by playing thousands of games, then trains off of that data and learns from itself. 
### Instructions
Setup.py must be edited - 

OUTER_MAX is the number of outer loops to be ran

CPU_MAX is the number of cores to be used. More cores, faster training time, higher CPU load

OUT_START number is the outer_*.keras file that training will start on. 

MODE is the mode that will be used. Use ai_player_training for training, ai_player_watching to see results of training.


Once settings are as desired, run python tetris_ai.py from the command line to start training the AI!
