# UnleashTheGeek2022

## Strategies

### Strategy 0 - Dummy moves :
- Step 1 - Information scraping and instanciation:
    - Iterate over all cells :
      - If one or more robots is on the cell :
          - For each robot, instanciate the robots :
            - Give an id
            - Give the owner id
            - Give to him its cell's infos
              - Position

- Step 2 - Compute the actions :
  - Iterate over all our robots
    - Compute the action and put it :
      - If MOVE 1 robot.x robot.y robot.x + (np.randint(-1, 1)) robot.y + (np.randint(-1, 1)) raise an error :
        - WAIT
      - Else :
        - MOVE 1 robot.x robot.y robot.x + 1 robot.y + 1

### Strategy 1 - 

Strategy 2 :
- Step 1 - Information scraping and instanciation:
    - Iterate over all cells :
      If one or more robots is on the cell :
        - Get the information of adjacent cells
        - Instanciate the robots :
          - For each robot :
            - Give an id
            - Give the owner id
            - Give to him its cell's infos
            - Give to him the list of adjacent cells infos
            - Give an empty action

- Step 2 - Compute the actions :
  - Iterate over all our robots
    - Compute the action and put it
      - If ??? :
        -  MOVE amount fromX fromY toX toY
      - Elif ??? :
        - Update
        - BUILD x y 
      - Elif ??? -> SPAWN amount x y
              - Else -> WAIT

