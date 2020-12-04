# froggers.py to log work time

# import reload tool
from importlib import reload

# import system tools
import os
import sys

# import datetime
from datetime import datetime, timedelta
from time import time


# define Frogger class
class Frogger(list):
    """Class Frogger to keep track of hours.

    Inherits from:
        list
    """

    def __init__(self, path, discrete=False):
        """Initialize an instance.

        Arguments:
            path: str
            discrete: boolean, use discrete mode?

        Returns:
            None
        """

        # set path
        self.path = path

        # start time
        self.start = None

        # record discrete events?
        self.discrete = discrete

        # ingest current file
        self.ingest()

        return

    def ask(self):
        """Ask how many hours have gone by.

        Arguments:
            None

        Returns:
            None
        """

        # get finish time
        start = self.start
        finish = datetime.now()
        duration = (finish - start).total_seconds() / (60 * 60)

        # print total for the day
        total = round(sum([entry['duration'] for entry in self[0]['entries']] + [duration]), 2)
        print('{} hours so far...'.format(total))

        return None

    def croak(self, note=None):
        """Make a single timepoint entry.

        Arguments:
            note: str

        Returns:
            None

        Populates:
            self
        """

        # splish and splash
        self.splish()
        self.splash(note)

        return None

    def digest(self):
        """Write the log file.

        Arguments:
            None

        Returns:
            None
        """

        # make weekdays
        week = ['Mon', 'Tues', 'Wed', 'Thurs', 'Fri', 'Sat', 'Sun']

        # Get lines
        lines = []
        work = 0
        for day in self:

            # convert date
            date = datetime.strftime(day['date'], '%m/%d/%Y')
            weekday = week[day['date'].weekday()]

            # make day
            lines.append('{} {}\n'.format(weekday, date))

            # go through each line
            for entry in day['entries']:

                # format start
                start = datetime.strftime(entry['start'], '%H:%M')

                # format finish
                finish = datetime.strftime(entry['finish'], '%H:%M')

                # erase finish
                if self.discrete:

                    # set finish to blank
                    finish = ''

                # add to lines, assuming discrete mode
                line = '{} - {}) {}\n'.format(start, finish, entry['note'])
                lines.append(line)

            # if not in discrete mode
            if not self.discrete:

                # add total
                total = round(sum([entry['duration'] for entry in day['entries']]), 2)
                lines.append('Total: {} hours\n'.format(total))

                # determine weekly total
                work += total

                # add weekly total if day is mondday
                if weekday == 'Mon':

                    # add weekly total
                    lines.append('Total Week Hours: {} hours\n'.format(work))
                    work = 0

            # add spacer
            lines.append('\n')
            lines.append('\n')

        # write line
        with open(self.path, 'w') as pointer:

            # write file
            pointer.writelines(lines)

        return None

    def eat(self):
        """Refresh the page with an ingest digest cycle.

        Arguments:
            None

        Returns:
            None

        Populates:
            self
        """

        # ingest, digest
        self.ingest()
        self.digest()

        return None

    def flick(self):
        """Flick away checked off items.

        Arguments:
            None

        Returns:
            None
        """

        # reingest
        self.ingest()

        # go through each day
        for day in self:

            # remove entries ending with X
            day['entries'] = [entry for entry in day['entries'] if not entry['note'].endswith('X')]

        # digest
        self.digest()

        return None

    def ingest(self):
        """Ingest the contents of the current work log.

        Arguments:
            None

        Returns:
            None

        Populates:
            self
        """

        # try
        try:

            # to retrieve the current file
            with open(self.path, 'r') as pointer:

                # get lines
                lines = pointer.readlines()

        # unless it doesn't exit
        except FileNotFoundError:

            # create file
            with open(self.path, 'w') as pointer:

                # write blank
                lines = []
                pointer.writelines(lines)

        # remove returns
        lines = [line.strip() for line in lines]
        lines += ['']

        # break lines into days
        days = []
        day = {'entries': []}
        for line in lines:

            # check for blank or total line
            if line == '' or line.startswith('Total'):

                # add current day to days
                days.append(day)
                day = {'entries': []}

            # otherwise
            else:

                # check for first day
                if 'date' not in day.keys():

                    # get a date object
                    date = datetime.strptime(line.split()[1], '%m/%d/%Y')

                    # assume date is first line
                    day.update({'date': date})

                # otherwise assume a time row
                else:

                    # begin entry
                    entry = {}

                    # get start time
                    time = line.split('-')[0].strip()
                    hour, minute = time.split(':')
                    start = day['date'].replace(hour=int(hour), minute=int(minute), second=0, microsecond=0)
                    entry['start'] = start

                    # default finish to same
                    finish = start
                    entry['finish'] = finish

                    # if not in discrete mode
                    if not self.discrete:

                        # get finish time
                        time = line.split('-')[1].split(')')[0].strip()
                        hour, minute = time.split(':')
                        finish = day['date'].replace(hour=int(hour), minute=int(minute), second=0, microsecond=0)
                        entry['finish'] = finish

                    # calculate duration
                    duration = (finish - start).total_seconds() / (60 * 60)

                    # adjust for negative durations
                    duration += 24 * int(duration < 0)
                    entry['duration'] = duration

                    # make note entry
                    entry['note'] = line.split(')')[1].strip()

                    # add to current day
                    day['entries'].append(entry)

        # depopulate instance
        while len(self) > 0:

            # popoff
            self.pop()

        # repopulate
        for day in days:

            # filter out blanks
            if len(day['entries']) > 0:

                # append to self
                self.append(day)

        return None

    def splash(self, note=None):
        """Clock out.

        Arguments:
            note: str

        Returns:
            None
        """

        # get note
        if not note:

            # get from input
            note = input('note? ')

        # get finish time
        start = self.start
        finish = datetime.now()
        duration = (finish - start).total_seconds() / (60 * 60)

        # make entry
        entry = {'start': start, 'finish': finish, 'duration': duration, 'note': note}

        # append to current day
        self[0]['entries'].append(entry)

        # print
        print('splash!')

        # if not discrete
        if not self.discrete:

            # print total for the day
            total = round(sum([entry['duration'] for entry in self[0]['entries']]), 2)
            print('{} hours today.'.format(total))

        # update file
        self.digest()

        return None

    def splish(self):
        """Clock in.

        Arguments:
            None

        Returns:
            None

        Populates:
            self.start
        """

        # get now
        now = datetime.now()
        self.start = now

        # make new date entry if needed
        if len(self) < 1 or now.date() != self[0]['date'].date() and now.hour > 4:

            # make new entry
            day = {'date': now, 'entries': []}

            # append
            self.insert(0, day)

        # print
        print('splish...')

        return None


# fro.reload(fro); froggo = fro.froggo; jerko = fro.jerko; pondo = fro.pondo; frodo = fro.frodo
# toado = fro.toado; shoppo = fro.shoppo; scopo = fro.scopo; banko = fro.banko; testo = fro.testo
froggo = Frogger('frogs/omi_log.txt')
pondo = Frogger('frogs/omi_thoughts.txt', discrete=True)
jerko = Frogger('frogs/doucheberry_diaries.txt', discrete=True)
frodo = Frogger('frogs/omi_todo.txt', discrete=True)
toado = Frogger('frogs/general_todo.txt', discrete=True)
shoppo = Frogger('frogs/shopping.txt', discrete=True)
scopo = Frogger('frogs/historian_to_do.txt', discrete=True)
banko = Frogger('frogs/cc_log.txt', discrete=True)
testo = Frogger('frogs/test_log.txt', discrete=True)
