from gen import move_answer
# (unit, checkpoint index, new position of the correct option) — balances the key to 10/10/10/10
MOVES = [(1,0,0),(3,0,0),(5,0,0),(8,0,0),(10,1,0),(13,1,0),(15,0,0),(17,0,0),(18,1,0),(19,1,0),
         (1,1,2),(3,1,2),(9,0,2),(11,0,2),(12,1,2),(14,1,2),(16,0,2),(19,0,2),
         (2,0,3),(4,0,3),(9,1,3),(10,0,3),(11,1,3),(13,0,3),(16,1,3),(17,1,3)]
for n, qi, t in MOVES:
    move_answer(n, qi, t)
