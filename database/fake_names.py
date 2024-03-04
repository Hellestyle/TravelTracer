from faker import Faker


NUMBER_OF_NAMES = 5

def main():

    f = Faker()

    for _ in range(NUMBER_OF_NAMES):
        print(f.name())


if __name__ == "__main__":
    main()
