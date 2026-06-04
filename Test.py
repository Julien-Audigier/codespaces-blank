def showList(list,start="",finish="",between=" | "):
    print(f"{start}{list[0]}")
    list.remove()

def showBoard(board):
    for row in board:
        showList(row)

showBoard([[1,0,0],[0,1,0],[0,0,1]])