"""main.py

Entry point for the project.
"""
import h2p


def main(path):
    with open(path, 'r') as file:
        print(h2p.parser.parse(file.read()))


if __name__ == '__main__':
    main()
