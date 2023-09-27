from uno import Uno

#To Do:
# 1 - Try making deck display sideways rather than vertically (will be difficult)
# 2 - Add stacking of +2 and +4
# 3 - Add stacking of duplicate cards

def main():
    inputting = True
    print('''Welcome to Uno!!!
=================''')
    while inputting:
        try:
            n = int(input('How many players?'))
            inputting = False
        except ValueError:
            print('Please enter an integer')
    playing = True
    game = Uno(n)
    while playing:
        game.startGame()
        print("Do you want to play again? (y/n)")
        ans=input()
        if ans.lower() == 'n':
            playing = False
    print("Thanks for playing!")

main()
