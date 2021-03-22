# -*- coding: utf-8 -*-

'''
    Tulip library
    Author Twilight0

    SPDX-License-Identifier: GPL-3.0-only
    See LICENSES/GPL-3.0-only for more information.
'''


from __future__ import absolute_import, print_function

import re
import functools
import time
import hashlib
import os
import shutil

from ast import literal_eval as evaluate
from tulip.compat import str, database, is_py2, pickle

try:
    from tulip import control
    from tulip.log import log_debug
    cache_path = control.join(control.dataPath, 'cache')
except Exception:
    control = None
    cache_path = os.path.join(os.curdir, 'function_cache')

# noinspection PyUnboundLocalVariable
def get(function_, time_out, *args, **table):

    try:

        response = None

        f = repr(function_)
        f = re.sub(r'.+\smethod\s|.+function\s|\sat\s.+|\sof\s.+', '', f)

        a = hashlib.md5()
        for i in args:
            a.update(str(i))
        a = str(a.hexdigest())

    except Exception:

        pass

    try:
        table = table['table']
    except Exception:
        table = 'rel_list'

    try:

        if control:
            control.makeFile(control.dataPath)
            dbcon = database.connect(control.cacheFile)
        else:
            db_file = os.path.join(os.path.curdir, 'cache.db')
            dbcon = database.connect(db_file)

        dbcur = dbcon.cursor()
        dbcur.execute("SELECT * FROM {tn} WHERE func = '{f}' AND args = '{a}'".format(tn=table, f=f, a=a))
        match = dbcur.fetchone()

        try:
            response = evaluate(match[2].encode('utf-8'))
        except AttributeError:
            response = evaluate(match[2])

        t1 = int(match[3])
        t2 = int(time.time())
        update = (abs(t2 - t1) / 3600) >= int(time_out)
        if not update:
            return response

    except Exception:

        pass

    try:

        r = function_(*args)
        if (r is None or r == []) and response is not None:
            return response
        elif r is None or r == []:
            return r

    except Exception:
        return

    try:

        r = repr(r)
        t = int(time.time())
        dbcur.execute(
            "CREATE TABLE IF NOT EXISTS {} (""func TEXT, ""args TEXT, ""response TEXT, ""added TEXT, ""UNIQUE(func, args)"");".format(table)
        )
        dbcur.execute("DELETE FROM {0} WHERE func = '{1}' AND args = '{2}'".format(table, f, a))
        dbcur.execute("INSERT INTO {} Values (?, ?, ?, ?)".format(table), (f, a, r, t))
        dbcon.commit()

    except Exception:
        pass

    try:
        return evaluate(r.encode('utf-8'))
    except Exception:
        return evaluate(r)


# noinspection PyUnboundLocalVariable
def timeout(function_, *args, **table):

    try:

        f = repr(function_)
        f = re.sub(r'.+\smethod\s|.+function\s|\sat\s.+|\sof\s.+', '', f)

        a = hashlib.md5()
        for i in args:
            a.update(str(i))
        a = str(a.hexdigest())
    except Exception:
        pass

    try:
        table = table['table']
    except Exception:
        table = 'rel_list'

    try:

        if control:

            control.makeFile(control.dataPath)
            dbcon = database.connect(control.cacheFile)

        else:

            db_file = os.path.join(os.path.curdir, 'cache.db')
            dbcon = database.connect(db_file)

        dbcur = dbcon.cursor()
        dbcur.execute("SELECT * FROM {tn} WHERE func = '{f}' AND args = '{a}'".format(tn=table, f=f, a=a))
        match = dbcur.fetchone()
        return int(match[3])

    except Exception:

        return


def clear(table=None, withyes=False, notify=True, file_=None, label_yes_no=30401, label_success=30402):

    if file_ is None:
        if control:
            file_ = control.cacheFile
        else:
            file_ = os.path.join(os.path.curdir, 'cache.db')

    try:
        if control:
            control.idle()

        if table is None:
            table = ['rel_list', 'rel_lib']
        elif not type(table) == list:
            table = [table]

        if withyes and control:

            try:
                yes = control.yesnoDialog(control.lang(label_yes_no).encode('utf-8'), '', '')
            except Exception:
                yes = control.yesnoDialog(control.lang(label_yes_no), '', '')

            if not yes:
                return

        dbcon = database.connect(file_)
        dbcur = dbcon.cursor()

        for t in table:
            try:
                dbcur.execute("DROP TABLE IF EXISTS {0}".format(t))
                dbcur.execute("VACUUM")
                dbcon.commit()
            except Exception:
                pass

        if control and notify:
            control.infoDialog(control.lang(label_success).encode('utf-8'))
    except Exception:
        pass


def delete(withyes=True, label_yes_no=30401, label_success=30402):

    if withyes:

        yes = control.yesnoDialog(control.lang(label_yes_no).encode('utf-8'), '', '')

        if not yes:
            return

    else:

        pass

    control.deleteFile(control.cacheFile)

    control.infoDialog(control.lang(label_success).encode('utf-8'))

# Functions below shamelessly taken and adapted from ResolveURL, so thanks to all of its contributors

class FunctionCache:

    def __init__(self):

        if not os.path.exists(cache_path):
            os.makedirs(cache_path)

    def reset_cache(self, notify=False, label_success=30402):

        try:
            shutil.rmtree(cache_path)
            if notify:
                control.infoDialog(control.lang(label_success).encode('utf-8'))
            return True
        except Exception as e:
            if control:
                log_debug('Failed to create cache: {0}: {1}'.format(cache_path, e))
            else:
                print('Failed to create cache: {0}: {1}'.format(cache_path, e))
            return False

    def _get_func(self, name, args=None, kwargs=None, cache_limit=1):

        now = time.time()
        max_age = now - (cache_limit * 60 * 60)

        if args is None:
            args = []

        if kwargs is None:
            kwargs = {}

        full_path = os.path.join(cache_path, self._get_filename(name, args, kwargs))

        if os.path.exists(full_path):

            mtime = os.path.getmtime(full_path)

            if mtime >= max_age:

                with open(full_path, 'rb') as f:
                    pickled_result = f.read()

                return True, pickle.loads(pickled_result)

        return False, None

    def _save_func(self, name, args=None, kwargs=None, result=None):

        try:

            if args is None:
                args = []

            if kwargs is None:
                kwargs = {}

            pickled_result = pickle.dumps(result, protocol=pickle.HIGHEST_PROTOCOL)
            full_path = os.path.join(cache_path, self._get_filename(name, args, kwargs))

            with open(full_path, 'wb') as f:
                f.write(pickled_result)

        except Exception as e:

            if control:
                log_debug('Failure during cache write: {0}'.format(e))
            else:
                print('Failure during cache write: {0}'.format(e))

    def _get_filename(self, name, args, kwargs):

        if is_py2:
            arg_hash = hashlib.md5(name).hexdigest() + hashlib.md5(str(args)).hexdigest() + hashlib.md5(str(kwargs)).hexdigest()
        else:
            arg_hash = hashlib.md5(name.encode('utf8')).hexdigest() + hashlib.md5(str(args).encode('utf8')).hexdigest() + hashlib.md5(str(kwargs).encode('utf8')).hexdigest()

        return arg_hash

    def cache_method(self, cache_limit):

        def wrap(func):

            @functools.wraps(func)
            def memoizer(*args, **kwargs):

                if args:

                    klass, real_args = args[0], args[1:]
                    full_name = '%s.%s.%s' % (klass.__module__, klass.__class__.__name__, func.__name__)

                else:

                    full_name = func.__name__
                    real_args = args

                in_cache, result = self._get_func(full_name, real_args, kwargs, cache_limit=cache_limit)

                if in_cache:

                    if control:
                        log_debug('Using method cache for: |{0}|{1}|{2}| -> |{3}|'.format(full_name, args, kwargs, len(pickle.dumps(result, protocol=pickle.HIGHEST_PROTOCOL))))
                    else:
                        print('Using method cache for: |{0}|{1}|{2}| -> |{3}|'.format(full_name, args, kwargs, len(pickle.dumps(result, protocol=pickle.HIGHEST_PROTOCOL))))
                    return result

                else:

                    if control:
                        log_debug('Calling cached method: |{0}|{1}|{2}|'.format(full_name, args, kwargs))
                    else:
                        print('Calling cached method: |{0}|{1}|{2}|'.format(full_name, args, kwargs))
                    result = func(*args, **kwargs)
                    self._save_func(full_name, real_args, kwargs, result)

                    return result

            return memoizer

        return wrap
