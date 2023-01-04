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

        def dfs(r, c):
            # printBoard(board)
            if r>=8 and c>=9:               # Depth search to the end and return True
                return True
            elif c>=9:                      # From the end of current row to the begin of next row
                r+=1
                c=0

            if str(board[r][c])>='1' and str(board[r][c])<='9':
                return dfs(r, c+1)          # if element has been filled, search next element
            
            indexOfBlock = r // 3 * 3 + c // 3
            cross = rowHashSet[r].intersection( colHashSet[c] )
            cross = blockHashSet[indexOfBlock].intersection(cross)
            # print(cross)
            for num in cross:
                board[r][c] = num
                rowHashSet[r].remove(num)
                colHashSet[c].remove(num)
                blockHashSet[indexOfBlock].remove(num)
                right = dfs(r, c+1)
                
                if right :
                    return True
                else:
                    board[r][c] = '.'
                    rowHashSet[r].add(num)
                    colHashSet[c].add(num)
                    blockHashSet[indexOfBlock].add(num)
            return False

        dfs(0,0)
        # printBoard(board)


from loadBoard import loadBoard
board1 = loadBoard('board1.txt')
board2 = loadBoard('board2.txt')
board3 = loadBoard('board3.txt')


import time
start_time = time.time()
Solution().solveSudoku(board3)
print("Method2 --- %s seconds ---" % (time.time() - start_time))
