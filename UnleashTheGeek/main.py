game = Game(HEIGHT, WIDTH)

while True:
    inputs = Inputs(HEIGHT, WIDTH, ME, OPP)
    inputs.readInput()
    game.inputs = inputs
    actions = game.play()

    print(actions, file=sys.stderr, flush=True)

    # To debug: print("Debug messages...", file=sys.stderr, flush=True)
    print(';'.join(actions) if len(actions) > 0 else 'WAIT')
