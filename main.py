from RuthSql import RuthSql


def main():
    db = RuthSql('ruthdb.db')
    print(db.execute('create table s (uid)'))


if __name__ == '__main__':
    main()
