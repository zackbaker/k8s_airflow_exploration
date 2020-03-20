from random import randint


def run():
    if randint(0, 1) == 1:
        print('It is Heads!')
    else:
        print('It is Tails!')

if __name__ == '__main__':
    run()