# Checkers-AI

To make our AI agent “smart” we combined the minimax algorithm with alpha-beta pruning and a strong evaluation function. We decided to use the minimax algorithm for our AI because it always returns the most optimal move given that the opponent plays optimally. Alpha-beta pruning was included in our minimax algorithm to improve the efficiency of our AI choosing an optimal move. 
In our evaluation function, we placed a larger weight on getting our AI’s pawns to the opponent’s side of the board in order to be kinged. We also placed an emphasis on piece differentials when there wasn’t a clear path to the opponent’s side of the board so that our AI wouldn’t lose a piece without gaining an advantage. In previous AIs, our first king would remain in the corner and repeat the same two moves until the game is tied or won. To improve our AI’s aggressiveness, we implemented an end game evaluation to determine king differential. If the king differential favored our AI, our AI would play more aggressive compared to if the differential favored our opponent. With a less favorable king differential, our AI would prefer to preserve the safety of its pieces over attacking the opponent pieces. 
