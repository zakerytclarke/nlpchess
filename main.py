import chess
import chess.pgn
import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def getNextMove(game, board):
    # Call GPT-3 to solicit next moves
    gameTxt = "\n".join(game)+"\n"
    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=f"Let's play a game of chess:\n{gameTxt}",
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    try:
        # Isolate the next move set
        nextMoves = list(filter(lambda x:x!="",response.choices[0].text.split("\n")))
        return nextMoves[0]
    except Exception as e:
        # Error generating, let's use a random valid move
        print("(Unable to generate move)")
        return list(board.legal_moves)[0]

def makeMove(game, board, move):
    print(move)
    try:
        board.push_san(move)
        game.append(move)
        return move
    except Exception as e:
        print(e)
        return None
    

def main():
    #Intialize Board
    board = chess.Board()
    game = ["e4"]
    board.push_san("e4")
    # Startup Screen
    print("NLP CHESS")
    print("Test your wits against a language model not fine-tuned to play chess")
    print("")
    
    while not (board.is_checkmate() or board.is_stalemate()):
        # Human Move
        print(f"{board}\n")
        while not makeMove(game, board, input("Next move:")):
            print("?")
        print(f"{board}\n")

        # NLP Bot Move
        print(f"{board}\n")
        makeMove(game, board, getNextMove(game,board))
        print(f"{board}\n")

main()