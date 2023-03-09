#!/usr/bin/env python3
'''BLH client'''
from argparse import ArgumentParser
import sys

from ocs.ocs_client import OCSClient
from ocs import OK


def main():
    '''BLH client'''

    parser = ArgumentParser()
    parser.add_argument('operation',
                        choices=['start', 'stop', 'set'],
                        help='Operation type.')
    parser.add_argument('-s', '--speed', type=int,
                        help='Speed in RPM.')
    parser.add_argument('-a', '--accl_time', type=float,
                        help='Acceleration time in seconds.')
    parser.add_argument('-d', '--decl_time', type=float,
                        help='Deceleration time in seconds.')
    parser.add_argument('-f', '--forward', action='store_true',
                        help='Forward rotation')
    parser.add_argument('-b', '--backward', action='store_true',
                        help='Forward rotation')

    args = parser.parse_args()

    blh_client = OCSClient('blh', args=[])

    
    if args.operation == 'stop':
        status, message, _ = blh_client.stop_rotation()
        return

    params = {k: v for k, v in args.__dict__.items() if v is not None}
    status, message, _ = blh_client.set_values(**params)
    print(message)

    if status != OK:
        sys.exit(1)

    if args.operation == 'start':
        if args.forward and args.backward:
            print('Direction specification inconcistent')
            sys.exit(1)

        if args.backward:
            blh_client.start_rotation(forward=False)
        else: # Default is forward
            blh_client.start_rotation(forward=True)


if __name__ == '__main__':
    main()
