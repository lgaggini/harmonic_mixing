import logging
import sys
import coloredlogs
import re
import argparse
import random

LOG_LEVELS = ['debug', 'info', 'warning', 'error', 'critical']
logger = logging.getLogger('harmonic_mixing')


def log_init(loglevel):
    """ initialize the logging system """
    FORMAT = '%(asctime)s %(levelname)s %(module)s %(message)s'
    logging.basicConfig(format=FORMAT, level=getattr(logging,
                                                     loglevel.upper()))
    coloredlogs.install(level=loglevel.upper(), stream=sys.stdout)


class CamelotKey:
    def __init__(self, index, interval):
        if index == 0:
            index = 12
        self.index = index
        self.interval = interval

    def __repr__(self):
        if self.interval == 'minor':
            key_repr = '%sA' % (self.index)
        elif self.interval == 'major':
            key_repr = '%sB' % (self.index)
        return key_repr

    def __eq__(self, other):
        if not isinstance(other, CamelotKey):
            return NotImplemented
        return self.index == other.index and self.interval == other.interval

    def __lt__(self, other):
        if other == 'gap':
            return False
        if self.index < other.index:
            return True
        elif self.index > other.index:
            return False
        else:
            if self.interval == 'minor' and other.interval == 'major':
                return False
            elif self.interval == 'major' and other.interval == 'minor':
                return True
            else:
                return False

    def get_harmonic_keys(self, shuffle=False):
        harmonic = []
        harmonic.append(self)
        harmonic.append(CamelotKey((self.index+1) % 12, self.interval))
        harmonic.append(CamelotKey((self.index-1) % 12, self.interval))
        if shuffle:
            random.shuffle(harmonic)
        return harmonic

    def get_subharmonic_keys(self, shuffle=False):
        subharmonic = []
        subharmonic.append(self.inv_key())
        subharmonic.append(self.diagonal_key())
        subharmonic.append(self.energy_boost_key())
        if shuffle:
            random.shuffle(subharmonic)
        return subharmonic

    def get_all_keys(self, shuffle=False):
        harmonic_keys = self.get_harmonic_keys(shuffle=True)
        subharmonic_keys = self.get_subharmonic_keys(shuffle=True)
        all_keys = harmonic_keys + subharmonic_keys
        if shuffle:
            random.shuffle(all_keys)
        return all_keys

    def inv_key(self):
        if self.interval == 'major':
            new_interval = 'minor'
        if self.interval == 'minor':
            new_interval = 'major'
        return CamelotKey(self.index, new_interval)

    def diagonal_key(self):
        if self.interval == 'major':
            new_interval = 'minor'
            new_index = self.index + 1
        if self.interval == 'minor':
            new_interval = 'major'
            new_index = self.index - 1
        return CamelotKey(new_index, new_interval)

    def energy_boost_key(self):
        return CamelotKey((self.index+2) % 12, self.interval)


class HarmonicMix:
    def __init__(self, keys):
        self.keys = keys
        self.harmonic_keys = self.get_harmonic_keys()
        self.subharmonic_keys = self.get_subharmonic_keys()
        self.all_keys = self.get_all_keys()

    def __repr__(self):
        return str(self.keys)

    def get_mix(self):
        return self.keys

    def init_from_string(self, keys):
        obj_keys = []
        for key in keys:
            index, interval = self.parse(key)
            logger.debug(index)
            logger.debug(interval)
            obj_key = CamelotKey(index, interval)
            obj_keys.append(obj_key)
        self.keys = obj_keys.copy()
        self.harmonic_keys = self.get_harmonic_keys()
        self.subharmonic_keys = self.get_subharmonic_keys()
        self.all_keys = self.get_all_keys()

    def parse(self, key):
        pattern = re.compile(r'^(\d+)([A-B])$')
        match = pattern.match(key)
        index = int(match.group(1))
        short_interval = match.group(2)
        if short_interval == 'A':
            interval = 'minor'
        elif short_interval == 'B':
            interval = 'major'
        return index, interval

    def get_harmonic_keys(self):
        harmonic_keys = {}
        for key in self.keys:
            harmonic_keys[str(key)] = key.get_harmonic_keys()
        return harmonic_keys

    def get_subharmonic_keys(self):
        subharmonic_keys = {}
        for key in self.keys:
            subharmonic_keys[str(key)] = key.get_subharmonic_keys()
        return subharmonic_keys

    def get_all_keys(self):
        all_keys = {}
        for key in self.keys:
            all_keys[str(key)] = self.harmonic_keys[str(key)] +\
                self.subharmonic_keys[str(key)]
        return all_keys

    def diff(self, used):
        all_keys = self.keys.copy()
        logger.debug('all: %s' % (all_keys))
        logger.debug('used: %s' % (used))
        for key in used.get_mix():
            if key in all_keys:
                all_keys.remove(key)
        return all_keys

    def find_all_recursive(self, gaps=False, all=False, sort=True):
        valid_mixes = []
        loop_keys = []
        for key in self.keys:
            if key not in loop_keys:
                loop_keys.append(key)
        for key in loop_keys:
            logger.info('finding mixes starting with %s' % (key))
            remaining_keys = self.keys.copy()
            remaining_keys.remove(key)
            mixes_found = self.search_next_key_all(key,
                                                   remaining_keys, [key],
                                                   all, gaps)
            for mix_found in mixes_found:
                mix_found.insert(0, key)
                logger.debug('mixes found starting with %s: %s' % (key,
                                                                   mix_found))
                if 'gap' in mix_found:
                    if gaps:
                        valid_mixes.append(mix_found)
                    else:
                        continue
                valid_mixes.append(mix_found)
        logger.debug('%s valid mixes found' % (len(valid_mixes)))
        if sort:
            valid_mixes.sort()
        return valid_mixes

    def search_next_key_all(self, actual_key, remaining_keys, actual_mix,
                            all, gaps):
        valid_mixes = []
        valid_sub_mixes = []
        logger.debug('actual key: %s' % (actual_key))
        if all:
            harmonic_keys = self.all_keys[str(actual_key)]
            logger.debug('all harmonic for %s: %s' % (actual_key,
                                                      harmonic_keys))
            subharmonic_keys = []
        else:
            harmonic_keys = self.harmonic_keys[str(actual_key)]
            logger.debug('harmonic for %s: %s' % (actual_key, harmonic_keys))
            subharmonic_keys = self.subharmonic_keys[str(actual_key)]
            logger.debug('subharmonic for %s: %s' % (actual_key,
                                                     subharmonic_keys))
        logger.debug('remaining_keys: %s' % (len(remaining_keys)))
        logger.debug('remaining_keys: %s' % (remaining_keys))

        if len(remaining_keys) == 1:
            for key in harmonic_keys:
                if key == remaining_keys[0]:
                    valid_mixes.append([key])

            if not all and len(valid_mixes) > 0:
                logger.debug('valid last: %s' % valid_mixes)
                return valid_mixes

            for key in subharmonic_keys:
                if key == remaining_keys[0]:
                    valid_mixes.append([key])

            if len(valid_mixes) > 0:
                logger.debug('valid last: %s' % valid_mixes)
                return valid_mixes
            else:
                logger.debug('invalid mixes on last key: %s'
                             % (actual_mix + ['gap'] + remaining_keys))
                if gaps:
                    valid_mixes.append(['gap']+remaining_keys)
                    logger.debug(valid_mixes)
                return valid_mixes
        else:
            logger.debug('intermediate')
            for key in harmonic_keys:
                logger.debug('finding match for key %s' % (key))
                tmp_remaining = remaining_keys.copy()
                tmp_actual = actual_mix.copy()
                if key in tmp_remaining:
                    logger.debug('match found for key %s' % (key))
                    tmp_remaining.remove(key)
                    tmp_actual.append(key)
                    valid_sub_mixes = self.search_next_key_all(key,
                                                               tmp_remaining,
                                                               tmp_actual,
                                                               all, gaps)
                    logger.debug('valid submixes: %s' % (valid_sub_mixes))
                    for valid_sub_mix in valid_sub_mixes:
                        valid_sub_mix.insert(0, key)
                        logger.debug('submix: %s' % (valid_sub_mix))
                        valid_mixes.append(valid_sub_mix)

            if not all and len(valid_mixes) > 0:
                return valid_mixes

            for key in subharmonic_keys:
                tmp_remaining = remaining_keys.copy()
                tmp_actual = actual_mix.copy()
                if key in remaining_keys:
                    tmp_remaining.remove(key)
                    tmp_actual.append(key)
                    valid_sub_mixes = self.search_next_key_all(key,
                                                               tmp_remaining,
                                                               tmp_actual,
                                                               all, gaps)
                    for valid_sub_mix in valid_sub_mixes:
                        valid_sub_mix.insert(0, key)
                        valid_mixes.append(valid_sub_mix)

            if len(valid_mixes) > 0:
                return valid_mixes
            else:
                if gaps:
                    logger.debug('invalid mixes during the search: %s' %
                                 (actual_mix + ['gap'] + remaining_keys))
                    valid_mixes.append(['gap'] + remaining_keys)
                return valid_mixes

    def gap_fill(self, gapped_list):
        return []


def is_sublist(lst, filter):
    filter_length = len(filter)
    lst_length = len(lst)
    for i in range(lst_length - filter_length + 1):
        if lst[i:i + filter_length] == filter:
            return True
    return False


if __name__ == '__main__':

    description = 'harmonic_mixing, find harmonic mixes'
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('-k', '--keys', default='settings',
                        required=True,
                        type=lambda s: [item for item in s.split(',')],
                        help='comma splitted list of keys to be mixed')
    parser.add_argument('-f', '--filter', default=None,
                        type=lambda s: [item for item in s.split(',')],
                        help='filter to get mixes with selected keys sequence')
    parser.add_argument('-a', '--all', action='store_true',
                        help='no priority to safer mixes (default disabled)')
    parser.set_defaults(priority=False)
    parser.add_argument('-u', '--unsort', action='store_false',
                        help='unsort mixes (default disabled)')
    parser.set_defaults(sort=False)
    parser.add_argument('-g', '--gaps', action='store_true',
                        help='enables mix with gaps (default disabled)')
    parser.set_defaults(gaps=False)
    parser.add_argument('-l', '--log-level', default=LOG_LEVELS[1],
                        help='log level (default info)', choices=LOG_LEVELS)

    options = {}
    cli_options = parser.parse_args()
    log_init(cli_options.log_level)
    logger.debug(cli_options)

    valid_mixes = []
    keys = cli_options.keys
    mix = HarmonicMix([])
    mix.init_from_string(keys)
    logger.debug(mix)
    valid_mixes = mix.find_all_recursive(cli_options.gaps,
                                         cli_options.all,
                                         cli_options.unsort)
    logger.debug(valid_mixes)
    uniq_valid_mixes = valid_mixes
    mix_filter = None
    found_mixes = len(uniq_valid_mixes)
    if cli_options.filter:
        mix_filter = HarmonicMix([])
        mix_filter.init_from_string(cli_options.filter)
        found_mixes = 0
        logger.info('filtering for %s' % (mix_filter.get_mix()))
    for valid_mix in uniq_valid_mixes:
        if cli_options.filter:
            if is_sublist(valid_mix, mix_filter.get_mix()):
                found_mixes += 1
                logger.info(valid_mix)
        else:
            logger.info(valid_mix)
    msg = 'found %s/%s filtered valid mixes'
    logger.info(msg % (found_mixes, len(uniq_valid_mixes)))
