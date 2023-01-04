from loadBoard import loadBoard
import time
from printBoard import printBoard

class Solution:
    def solveSudoku(self, board: list[list[str]]) -> None:
        # print('\n\n\n\n\n\n\n\n\n\n\n\n\n')
        # printBoard(board)
        arr = [1,2,3,4,5,6,7,8,9]
        rowHashSet = []
        colHashSet = []
        blockHashSet = []
        emptyLocation = []
        for i in range(9):
            rowHashSet.append(set(arr))
            colHashSet.append(set(arr))
            blockHashSet.append(set(arr))
        for i in range(9):
            for j in range(9):
                if board[i][j] >= '1' and board[i][j] <= '9':
                    rowHashSet[i].remove( int(board[i][j]) )
                    colHashSet[j].remove( int(board[i][j]) )
                    indexOfBlock = i // 3 * 3 + j // 3                    
                    blockHashSet[indexOfBlock].remove( int(board[i][j]) )
                else: 
                    emptyLocation.append(f'{i},{j}')
        emptyLocation.append("9,9")
        def dfs(toFill, r, c):
            # printBoard(board)
            if toFill == len(emptyLocation)-1:
                return True
            
            cross = rowHashSet[r].intersection( colHashSet[c] )
            indexOfBlock = r // 3 * 3 + c // 3                    
            cross = blockHashSet[indexOfBlock].intersection(cross)

            for num in cross:
                board[r][c] = num
                rowHashSet[r].remove(num)
                colHashSet[c].remove(num)
                blockHashSet[indexOfBlock].remove(num)
                
                right = dfs(toFill+1, int(emptyLocation[toFill+1][0]), int(emptyLocation[toFill+1][2]))
                if right :
                    return True
                else:
                    board[r][c] = '.'
                    rowHashSet[r].add(num)
                    colHashSet[c].add(num)
                    blockHashSet[indexOfBlock].add(num)
            return False
        toFill = 0
        dfs(toFill, int(emptyLocation[toFill][0]), int(emptyLocation[toFill][2]))
        # printBoard(board)

board1 = loadBoard('board1.txt')
board2 = loadBoard('board2.txt')
board3 = loadBoard('board3.txt')


start_time = time.time()
Solution().solveSudoku(board3)
print("Method3 --- %s seconds ---" % (time.time() - start_time))
