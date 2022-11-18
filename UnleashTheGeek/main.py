game = Game(HEIGHT, WIDTH)

while True:
    inputs = Inputs(HEIGHT, WIDTH)
    inputs.readInput()
    game.inputs = inputs
    try:
        actions = game.play()
        print(actions, file=sys.stderr, flush=True)
    except:
        actions = ["WAIT"]
        print("Something went wrong when running the gameplay !", file=sys.stderr, flush=True)

    # To debug: print("Debug messages...", file=sys.stderr, flush=True)
    print(';'.join(actions) if len(actions) > 0 else 'WAIT')
