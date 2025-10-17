# Tetris AI
An AI that trains against itself using a keras model and reinforcement learning to play the game Tetris. Collects data by playing thousands of games, then trains off of that data and learns from itself. 
### Instructions
#### From GUI:
usage: python main.py

#### From the command Line:
usage: tetris_ai.py [-h] [--mode {human_player,ai_player_training,ai_player_watching}] [--out_start N] [--outer_max N] [-V] [-help]

tetris_ai.py — run your Tetris program in different modes.

Modes:
  human_player        start the game for a human to play
  ai_player_training  train the AI (uses OUT_START as the starting level)
  ai_player_watching  load a saved model and let the AI play (GUI shown)

options:
  -h, --help            show this help message and exit
  --mode {human_player,ai_player_training,ai_player_watching}
                        Select program mode. Default: ai_player_watching
  --out_start N         Integer training level / OUT_START used when training or watching. Default: 0
  --outer_max N         OUTER_MAX (only used for training). Default: 10
  -V, --version         Show program version and exit.
  -help                 show this help message and exit

Examples:
  python tetris_ai.py                     # run with defaults (ai_player_watching)
  python tetris_ai.py --mode ai_player_watching --out_start 5
  python tetris_ai.py --mode ai_player_training --out_start 2 --outer_max 20