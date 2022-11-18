import time

game = Game(HEIGHT, WIDTH)


while True:
    t0 = time.time()
    inputs = Inputs(HEIGHT, WIDTH)
    inputs.readInput()
    game.inputs = inputs
    # actions = game.play(t0)
    # print(actions, file=sys.stderr, flush=True)
    # print(time.time()-t0, file=sys.stderr, flush=True)
    try:
        actions = game.play(t0)
        print(actions, file=sys.stderr, flush=True)
    except:
        actions = ["WAIT"]
        print("Something went wrong when running the gameplay !", file=sys.stderr, flush=True)

    # To debug: print("Debug messages...", file=sys.stderr, flush=True)
    print(';'.join(actions) if len(actions) > 0 else 'WAIT')
