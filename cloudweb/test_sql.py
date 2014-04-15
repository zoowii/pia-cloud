# coding: utf8
from __future__ import print_function, unicode_literals
from cloudsql import engine


def main():
    session = engine.Session()
    sql1 = 'use games'
    sql2 = 'select songs.song, songs.game from songs'
    sql3 = "select * from songs where artist='pia-cloud'"
    sql4 = "insert into songs values (game='test song', artist='pia-cloud', song='cloud', age=23)"
    print(engine.squeal(session, sql1))
    print(engine.squeal(session, sql2))
    print(engine.squeal(session, sql3))
    print(engine.squeal(session, sql4))


if __name__ == '__main__':
    main()