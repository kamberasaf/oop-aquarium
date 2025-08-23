import time
import Aqua


def valid_num_check(word: str, num=0) -> float or bool:
    # This is checking for a valid number.
    try:
        if '.' in word:
            for s in set(*word.split('.')[1:]):
                if s != '0':
                    print('\nPlease enter a valid number.\n')
                    return False
        word = float(word)
        word = int(word)
        if word < num or word <= 0:
            raise ValueError
    except (ValueError, TypeError):
        print('\nPlease enter a valid number.\n')
        return False
    return word


def demo(myaqua):
    myaqua.add_animal("scalarfish1", 4, 10, 10, 1, 0, 'sc')
    myaqua.add_animal("molyfish2", 12, 35, 15, 0, 1, 'mo')
    myaqua.add_animal("shrimpcrab1", 3, 20, myaqua.aqua_height, 1, 0, 'sh')
    myaqua.add_animal("ocypodcrab1", 13, 41, myaqua.aqua_height, 0, 0, 'oc')
    myaqua.print_board()

    for i in range(120):
        if i % 50 == 0:
            myaqua.feed_all()
        myaqua.next_turn()
        if i != 119:  # we want to print the final run once.
            myaqua.print_board()
            print('\n')
        time.sleep(0.5)


def add_animal(myaqua):
    valid_int = False
    while not valid_int:
        print("\nPlease select:")
        print("1. Scalar")
        print("2. Moly")
        print("3. Ocypode")
        print("4. Shrimp")
        fish_type = input("What animal do you want to put in the aquarium?")
        fish_type = valid_num_check(fish_type)
        if fish_type not in [1, 2, 3, 4]:
            if fish_type:
                print('\nPlease enter a valid number.\n')
                continue
            continue
        valid_int = True
    valid_name = False
    while not valid_name:
        name = input("Please enter a name:")
        try:
            for i in name.replace(" ", ""):
                if not i.isalnum():
                    raise ValueError
            if len(name.replace(" ", "")) == 0:
                raise ValueError
        except (ValueError, TypeError):
            print('\nPlease enter a valid name.')
            continue
        valid_name = True

    valid_age = False
    while not valid_age:
        age = input("Please enter age:")
        age = valid_num_check(age)
        if age not in [i for i in range(1, 101)]:
            if age:
                print('\nPlease enter a valid number.\n')
                continue
            continue
        valid_age = True

    success = False
    while not success:
        x, y = 0, 0
        valid_x_int = False
        while not valid_x_int:
            x = input("Please enter an X axis location (1 - %d):" % (myaqua.aqua_width - 1))
            x = valid_num_check(x)
            if not (1 <= x <= (myaqua.aqua_width - 1)):
                if x:
                    print('Please enter a valid number.\n')
                    continue
                continue
            valid_x_int = True

        if fish_type in [1, 2]:  # if a fish was selected
            valid_y_int = False
            while not valid_y_int:
                y = input("Please enter an Y axis location (%d - %d):" % (Aqua.WATERLINE, myaqua.aqua_height - 1))
                y = valid_num_check(y)
                if not (Aqua.WATERLINE <= y <= (myaqua.aqua_height - 1)):
                    if y:
                        print('Please enter a valid number.\n')
                        continue
                    continue
                valid_y_int = True

        directionH, directionV = -1, -1
        while not (directionH == 0 or directionH == 1):
            directionH = input("Please enter horizontal direction (0 for Left, 1 for Right):")
            try:
                if '.' in directionH:
                    for s in set(*directionH.split('.')[1:]):
                        if s != '0':
                            print('\nPlease enter a valid number.\n')
                            return False
                directionH = float(directionH)
                directionH = int(directionH)
            except (ValueError, TypeError):
                print('Please enter a valid number.\n')
                continue
        if fish_type in [1, 2]:  # a fish
            while not (directionV == 0 or directionV == 1):
                directionV = input("Please enter vertical direction  (0 for Down, 1 for Up):")
                try:
                    if '.' in directionV:
                        for s in set(*directionV.split('.')[1:]):
                            if s != '0':
                                print('\nPlease enter a valid number.\n')
                                return False
                    directionV = float(directionV)
                    directionV = int(directionV)
                except (ValueError, TypeError):
                    print('Please enter a valid number.\n')
                    continue

        if fish_type == 1:
            success = myaqua.add_animal(name, age, x, y, directionH, directionV, 'sc')
        elif fish_type == 2:
            success = myaqua.add_animal(name, age, x, y, directionH, directionV, 'mo')
        elif fish_type == 3:
            success = myaqua.add_animal(name, age, x, y, directionH, 0, 'oc')
        else:
            success = myaqua.add_animal(name, age, x, y, directionH, 0, 'sh')

    return None


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    width = 0
    height = 0

    print('\nWelcome to "The OOP Aquarium"')
    valid_input = False
    while not valid_input:
        width = input("The width of the aquarium (Minimum 40): ")
        width = valid_num_check(width, 40)
        if not width:
            continue
        valid_height = False
        while not valid_height:
            height = input("The height of the aquarium (Minimum 25): ")
            height = valid_num_check(height, 25)
            if not height:
                continue
            valid_height = True

        valid_input = True

    myaqua = Aqua.Aqua(width, height)

    while True:
        valid_input = False
        while not valid_input:
            print("\nMain menu")
            print("-" * 30)
            print("1. Add an animal")
            print("2. Drop food into the aquarium")
            print("3. Take a step forward")
            print("4. Take several steps")
            print("5. Demo")
            print("6. Print all")
            print("7. Exit")

            choice = input("\nWhat do you want to do?")
            choice = valid_num_check(choice)
            if choice not in [1, 2, 3, 4, 5, 6, 7]:
                if choice:
                    print('\nPlease enter a valid number.\n')
                    continue
                continue
            valid_input = True

        if choice == 1:
            add_animal(myaqua)
        elif choice == 2:
            myaqua.feed_all()
        elif choice == 3:
            myaqua.next_turn()
        elif choice == 4:
            myaqua.several_steps()
        elif choice == 5:
            demo(myaqua)
        elif choice == 6:
            myaqua.print_all()
        else:
            print("Bye bye")
            exit()

        myaqua.print_board()
        print('\n')