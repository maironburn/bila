from argparse import ArgumentParser



parser = ArgumentParser(description='Bila Automation Service')
parser.add_argument('--start-mode', help="modo de inicio (socket/ rest service)",
                    choices=['socket', 'rest'], required=True, nargs=1)


args = parser.parse_args()



