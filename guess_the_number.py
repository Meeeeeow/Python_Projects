import random;

# user as player
play_game = 'y';
print('Welcome to the guessing game'.center(40, '-'));
counter = 1;
while play_game == 'y':

    try:
        cpu_number = random.randint(1, 100);
        user_number = int(input(f'try guessing a number between 1 and 100: '));

        if user_number <= 100:
            while cpu_number != user_number:
                if user_number > cpu_number:
                    print('your number is too large');
                if user_number < cpu_number:
                    print('your number is too small');
                if abs(user_number - cpu_number) <= 5:
                    print('you are really close to the number!!fight!!');
                counter += 1;
                print(counter);
                user_number = int(input(f'Give try again: '));
            print(f'Banzai!!!You got it!You took {counter} tries!');
            play_game = input(f'Continue? ');
            if play_game == 'n':
                print('Thank you for playing!!');
                break;
        else:
            print('You have entered a number greater than 100');
            counter += 1;
    except ValueError:
        print('please enter a valid number');
        counter += 1;

# computer as player
play_the_game = 'y';
start = 1;
end = 100;

smallest = start;
largest = end;
print('Guide your cpu to your lucky number'.center(47, '-'));
while play_the_game == 'y':
    try:
        smallest = start;
        print(f'smallest {smallest}');
        largest = end;
        print(f'largest {largest}');
        direction = 'n';
        counter = 0;
        print('guess a number between 1 and 100 : ');
        try_guess = random.randint(smallest, largest);
        print(try_guess);
        while direction != 'c':
            direction = input('Is it too large(l),too small(s) or correct(c)? ');
            if direction == 's':
                if try_guess >= smallest:
                    smallest = try_guess + 1;
                    print(f'smallest {smallest}');
                    print(f'largest {largest}');
                    try_guess = random.randint(smallest, largest);
                    print(try_guess);
            if direction == 'l':
                if try_guess <= largest:
                    largest = try_guess;
                    print(f'smallest {smallest}');
                    print(f'largest {largest}');

                    try_guess = random.randint(smallest, largest);
                    print(try_guess);
            counter += 1;
            print(counter);
        print(f'you have done it!!!! you took {counter} tries!');
        play_the_game = input('Continue? ');
        if play_the_game == 'n':
            print('thank you for playing');
            break;
    except ValueError:
        print('please input correct initial');







