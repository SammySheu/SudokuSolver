
# Sudoku Solver

###### tags: `Backtrack`, `DFS`, 

## **Backtrack vs DFS**

在寫數獨問題之前，可能常聽到Backtrack&DFS這兩個演算法詞彙，兩者好像相似，但又不完全一樣，我們先來看wikipedia的定義：

#### Backtrack:
> Backtracking is a class of algorithms for finding solutions to some computational problems, notably **constraint satisfaction problems**, that incrementally **builds candidates** to the solutions, and abandons a candidate ("backtracks") as soon as it determines that the candidate cannot possibly be completed to a valid solution.

#### DFS:
> Depth-first search (DFS) is an algorithm for traversing or searching tree or graph data structures. The algorithm starts at the root node and **explores as far as possible along each branch before backtracking**. Extra memory, usually a stack, is needed to keep track of the nodes discovered so far along a specified branch which helps in backtracking of the graph

我們不難發現，兩者有一些相似之處：
- 採用策略皆為：**一路走到底，遇到死路即折返**
- 都屬於**窮舉**式演算法，或稱為暴力法（brute force search）

在兩者的定義之中，我們也可以發現相異的地方：
- Backtrack當中，適用於**約束滿足類**的問題，且會列舉可能的解(build candidates to the problem)
- Backtrack會進行**剪枝**的行為，當某些路線不可行時，進行捨棄（abandon candidates）

在StackOverflow當中，也有人詢問這個問題，其中有一些回答值得討論
> For me, the difference between backtracking and DFS is that backtracking handles an **implicit** tree and DFS deals with an **explicit** one. This seems trivial, but it means a lot. When the search space of a problem is visited by backtracking, the implicit tree gets traversed and pruned in the middle of it. Yet for DFS, the tree/graph it deals with is explicitly constructed and unacceptable cases have already been thrown ~~i.e. pruned~~ away before any search is done.
> **So, backtracking is DFS for implicit tree, while DFS is backtracking without pruning.**

用一些我自己的語言翻譯：
- DFS處理顯示樹, Backtrack處理隱式樹，顯式與隱式差別不大，且也不一定要是樹（皆為Graph Algorithm）但意義在於
    - DFS已建構好樹，剩下的做搜尋&記憶 -> **Top-down + Memorization** 
    - Backtrack在過程中逐漸建立樹，並且建立候選人且淘汰候選人，即所謂剪枝行為
    - 剪枝行為會反覆經過某個Node，而DFS不會



## Sudoku Solving Techniques（Backtrack / DFS）

因此要說明Sudoku的解法是利用Backtrack或DFS其實不這麼重要了，我們只要記得兩者的特性
- 窮舉所有的解
- 做完A假設後繼續B假設，直到走到死路為止

---
### Method1
`**Hint** 窮舉所有的解，為最原始的暴力法`

在使用Backtrack Algorithm之前，可以藉由三個方向思考起
- Base Cases（When to terminate）
- Decisions（When to go further）
- State（How to optimize）

話不多說，直接範例解釋：
```Python
********Base Cases********
if r>=8 and c>=9:                         # 當呼叫到最後一列最後一行的右邊元素時，代表搜尋結束
    return True                   
elif c>=9:                                # 每一列的結尾，跳轉到下一列的起始位置
    r+=1
    c=0
```
```Python
********Decisions********
if str(board[r][c])>='1' and str(board[r][c])<='9':
    return dfs(r, c+1)                    # 如該元素已填好數字，往下一格前進
            
for num in range(1,10):                   # 由數字1開始窮舉，利用isSafe()檢查是否安全，
    if self.isSafe(board, r, c, num):     # 安全則填寫數字，並往下一格前進
        board[r][c] = str(num)
        right = dfs(r, c+1)
        if right :
            return True
        else:                             # 如果往右遇到困難，則刪除數字
            board[r][c] = '.'
return False
```
![GIF](https://i.imgur.com/yPELyk7.gif)

---
### Method2
`**Hint** 優化Method1，將「填數字並判斷是否安全」這個動作，以HashSet完成`

思想上，因為一個element需要查看所處的row, column, 以及block，因此在遞迴之前，先建立HashSet供查表，速度可以快上許多。HashSet數量為9(row)+9(column)+9(block) = 27 -> 分別用list儲存
```Python
for i in range(9):                        # 建立List[Set(int)]
    rowHashSet.append(set(arr))
    colHashSet.append(set(arr))
    blockHashSet.append(set(arr))
for i in range(9):
    for j in range(9):                    # 初始化HashSet(如遇到數字，則代表HashSet可能選項少一)
        if board[i][j] >= '1' and board[i][j] <= '9':
            rowHashSet[i].remove( int(board[i][j]) )
            colHashSet[j].remove( int(board[i][j]) )
            indexOfBlock = i // 3 * 3 + j // 3                    
            blockHashSet[indexOfBlock].remove( int(board[i][j]) )
```
此時，也不需呼叫原本的isSafe()函數，因為HashSet機制已經確保該數字的安全性
```Python
indexOfBlock = r // 3 * 3 + c // 3        # 利用 (A ∩ B) ∩ C 取得該元素可能的解
cross = rowHashSet[r].intersection( colHashSet[c] )
cross = blockHashSet[indexOfBlock].intersection(cross)

for num in cross:                         # 由交集的地方開始窮舉，並且不需isSafe()判斷
    board[r][c] = num
    rowHashSet[r].remove(num)             # 當該格填上數字時，HashSet即可更新(減少組合)
    colHashSet[c].remove(num)
    blockHashSet[indexOfBlock].remove(num)
    right = dfs(r, c+1)                   # 不需判斷，可直接往下一格前進

    if right :
        return True
    else:                                 # 如果往右遇到困難，則刪除數字，並刪除對應的HashSet
        board[r][c] = '.'
        rowHashSet[r].add(num)
        colHashSet[c].add(num)
        blockHashSet[indexOfBlock].add(num)
return False
```
![GIF](https://i.imgur.com/7w1f2yr.gif)

---
### Method3
`**Hint** 既然在遞迴之前已經掃過整個board（建立HashSet），何不順便紀錄空格的位置？`

原本Method1 & Method2的Decision making是填完數字之後，進入下一格(r, c+1)，現在Method3是「跳到下一個空格」，相形之下又少了更多的判斷時間。

```Python
for i in range(9):
    for j in range(9):
        if board[i][j] >= 49 and board[i][j] <= 57:
            rowHashSet[i].remove( int(board[i][j]) )
            colHashSet[j].remove( int(board[i][j]) )
            indexOfBlock = i // 3 * 3 + j // 3                    
            blockHashSet[indexOfBlock].remove( int(board[i][j]) )
        else: 
            emptyLocation.append(f'{i},{j}')    # 利用emptyLocation儲存空格所在的x,y
```

因為已經用emptyLocation尋找空格，因此Base Cases可以稍加更改。使用變數'toFill'計算空格被完成了多少，當toFill到達emptyLocation的最末端時，回傳True
```Python
********Base Cases********
if toFill == len(emptyLocation)-1:
    return True
```
Decision Making中，原本呼叫下一格元素(r,c+1)，變成呼叫下一個空格的所在位置（下一個“空格”即為emptyLocation的下一個元素）
```Python
********Decisions********
right = dfs(toFill+1, int(emptyLocation[toFill+1][0]), int(emptyLocation[toFill+1][2]))
```

## Conclusion

三個Method之中，time complexity皆為 ${\rm{O}(9^{81})}$，但因為Method2 & Method3皆有適度的優化，速度會比Method1快上許多
```Shell
********EasyProblem********
Method1 --- 0.007818937301635742 seconds ---
Method2 --- 0.000294923782348632 seconds ---
Method3 --- 0.000301837921142578 seconds ---
(26.5x faster than Method1)

********HardProblem********
Method1 --- 1.3151030540466309 seconds --- 
Method2 --- 0.0665199756622314 seconds ---
Method3 --- 0.0671439170837402 seconds ---
(19.8x faster than Method1)
```
