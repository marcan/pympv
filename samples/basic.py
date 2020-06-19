# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys

import mpv


def main(args):
    if len(args) != 1:
        print('pass a single media file as argument')
        return 1

    try:
        m = mpv.Context()
    except mpv.MPVError:
        print('failed creating context')
        return 1

    m.set_option('input-default-bindings')
    m.set_option('osc')
    m.set_option('input-vo-keyboard')
    m.initialize()

    m.command('loadfile', args[0])

    while True:
        event = m.wait_event(.01)
        if event.id == mpv.Events.none:
            continue
        print(event.name)
        if event.id in [mpv.Events.end_file, mpv.Events.shutdown]:
            break


if __name__ == '__main__':
    try:
        exit(main(sys.argv[1:]) or 0)
    except mpv.MPVError as e:
        print(str(e))
        exit(1)
