key = "t"
size = 9
def game_rules(game_state):
    rule = []
    rnge = int(size ** 0.5)
    print('range : {}'.format(rnge))
    diagnol_first = []
    diagnol_second = []
    for num in range(rnge):
        diagnol_first.append(key+str(num*rnge+num))
        diagnol_second.append(key+str(rnge*(num+1)-num-1))
        horizontal_check = []
        vertical_check = []
        for x in range(rnge):
            horizontal_check.append(key+str(num*rnge+x))
            vertical_check.append(key+str(x*rnge+num))
        rule.append(tuple(horizontal_check))
        rule.append(tuple(vertical_check))
    rule.append(tuple(diagnol_first))
    rule.append(tuple(diagnol_second))
    return rule

def filter_position (data):
    response = dict()
    response["status"] = "success"
    response["exit"] = False
    try:
        if data.isdigit() and int(data) in range(size):
            response["data"] = dict()
            response["data"]["input"] = key+data
        else:
            response["error"] = "invalid input"
            response["status"] = "failure"
    except ValueError:
        print(f'Error caught:\t{ValueError}')
        response["status"] = "failure"
        response["exit"] = True
        response["error"] = ValueError
    return response

def user_input(player):
    response = dict()
    response["status"] = "success"
    response["exit"] = False
    try:
        player_input = input(f'{player} ')
        plyr_input = player_input.lower()

        if plyr_input == "q" or plyr_input == "quit" or plyr_input == "exit":
            response["exit"] = True
        response["data"] = dict()
        response["data"]["input"] = plyr_input
    except ValueError:
        print(f'Error caught:\t{ValueError}')
        response["status"] = "failure"
        response["exit"] = True
        response["error"] = ValueError
    return response

def check(result):
    if result["exit"]:
        confirmation = input("are you sure you want to exit the game (y/n)")
        confirmation.lower()
        if confirmation == 'y' or confirmation == 'yes':
            exit()
        else:
            result["status"] = "failure"
            return result
    else:
        return result

def update_position(game_state, position, player_input):
    response = dict()
    response["status"] = "success"
    game_over = True
    won = False
    try:
        rnge = int(size**0.5)
        state = game_state
        if state[position]=="-":
            state[position] = player_input
            rule = game_rules(state)
            for num in range(rnge):
                print('{}|{}|{}\n'.format(state[key+str(num*rnge)],state[key+str(num*rnge+1)],state[key+str(num*rnge+2)]))
            
            for one,two,three in rule:
                if state[one] == state[two] == state[three] != "-":
                    won = True
                    game_over = True
                    state[one] = state[two] = state[three] = "*"
                    response["data"] = state
                    break
                elif state[one] == "-" or state[two] == "-" or state[three] == "-":
                    game_over = False
                    response["data"] = state
                else:
                    pass
        else:
            for num in range(rnge):
                print('{}|{}|{}\n'.format(state[key+str(num*rnge)],state[key+str(num*rnge+1)],state[key+str(num*rnge+2)]))
            response["data"] = state
            response["error"] = "invalid input"
            response["status"] = "failure"
            game_over = False
    except ValueError:
        print(f'Error caught:\t{ValueError}')
        response["status"] = "failure"
        response["error"] = ValueError
    response["exit"] = game_over
    response["won"] = won
    return response
        
def game():
    game_state = dict()
    number = 2
    rnge = int(size**0.5)
    for m in range(size):
        game_state[key + str(m)] = "-"
    player_moves = {1:'X',0:'O'}

    for num in range(rnge):
        print('{}|{}|{}\n'.format(game_state[key+str(num*rnge)],game_state[key+str(num*rnge+1)],game_state[key+str(num*rnge+2)]))

    while True:
        player = "player "+str(number%2+1)
        player_move = player_moves[number%2]
        print('\n{} turn : '.format(player))
        user_response = user_input(player+ " enter the position")
        
        check_response = check(user_response)
        if(user_response["status"] != "success" or check_response["status"] != "success"):
            if "error" in user_response.keys():
                print(user_response["error"])
            elif "error" in check_response.keys():
                print(check_response["error"])
            continue

        positional_result = filter_position(user_response["data"]["input"])
        
        check(positional_result)
        if(positional_result["status"] != "success"):
            print(positional_result["error"])
            continue
        
        game_result = update_position(game_state, positional_result["data"]["input"], player_move)
        print("\n")
        if 'error' in game_result:
            print(game_result["error"])
            if game_result["exit"]:
                break
            continue
        elif game_result["won"] and game_result["exit"]:
            print('\n{} won the game'.format(player))
            break
        elif not game_result["won"] and game_result["exit"]:
            print('\nAlas the game ended in draw')
            break
        else:
            pass
        number+=1
    
    for num in range(rnge):
        print('{}|{}|{}\n'.format(game_state[key+str(num*rnge)],game_state[key+str(num*rnge+1)],game_state[key+str(num*rnge+2)]))
game()