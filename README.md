The chess engine uses the minimax algorithm with alpha-beta pruning to search for the best move. The evaluation function is based on a combination of piece values, pawn structure, and positional considerations. The depth of the search and the weights of the evaluation function can be configured in the files included in the repository.

This repository includes a chess engine, which has been inspired by engines such as Stockfish. This engine can be used to play against a human opponent or against another engine. The engine uses a combination of traditional chess algorithms and neural networks to evaluate positions and make moves.

Requirements
Python 3.6 or higher
TensorFlow 2.0 or higher
Pandas
python-chess

1. Creating Board; 5 binary digits - first 2: Color, last 3: Type of piece
2. FEN Notation
3. Drag n drop; Getting the legal move (sliding pieces: rook, queen, bishop) (others: double pawn move, en passant, knight, pawn → queen, castle)
4. Concept of Check
5. Depth

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/6004b059-b692-4675-a1d0-015f961e9c96/Untitled.png)

1. Evaluation Function (How good a move is)

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/810b7e6e-0ca0-45af-9071-edc077eaf85d/Untitled.png)

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/c16dd495-e9cd-453f-a60f-33629623d503/Untitled.png)

********************Optimization: Alpha Beta Pruning********************

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/dc3fc8d1-f4b7-4bec-9ebc-7459de2d7a4a/Untitled.png)

**********************Transpositions: Getting same result using different moves**********************

Using → Zobrist Hashing (64 bit number to represent current positions)

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/ed481d54-fa24-4f93-9b79-f7f3993bce3d/Untitled.png)