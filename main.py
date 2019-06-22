from argparse import ArgumentParser



parser = ArgumentParser(description='Bila Automation Service')
parser.add_argument('--start-mode', help="modo de inicio (socket_mode/ rest service)",
                    choices=['socket_mode', 'rest'], required=True, nargs=1)


args = parser.parse_args()



