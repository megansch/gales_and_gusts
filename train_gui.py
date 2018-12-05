
import argparse
import gui.dialog
from train_tracks import train_tracks
from PyQt5 import QtWidgets
import sys

args = None


def parse_args():
    global args

    parser = argparse.ArgumentParser(description='run trainer')
    parser.add_argument('-i',
                        '--input_dir',
                        required=False,
                        dest='input_dir',
                        type=str,
                        help='collection of files to train')
    parser.add_argument('-c',
                        '--command_line',
                        required=False,
                        action='store_true',
                        help='Run as command-line application, with no GUI')
    parser.add_argument('-a',
                        '--all',
                        required=False,
                        dest='all',
                        action='store_true',
                        help='If passed, train on all the hurricane tracks. Otherwise, use the first ten.')
    args = parser.parse_args()


if __name__ == '__main__':
    parse_args()
    if args.command_line:
        # Run application as CLI
        assert args.input_dir != '', 'Missing input dir'

        train_tracks(args.input_dir, args.all)
    else:
        # Run application with GUI
        app = QtWidgets.QApplication(sys.argv)
        train_dialog = gui.dialog.Dialog(options=args)
        train_dialog.show()
        sys.exit(app.exec_())
