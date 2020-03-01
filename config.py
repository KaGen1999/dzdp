import pymysql


def connect():
    # 数据库自行配置
    db = pymysql.connect("localhost", "u", "p", "dzdp")
    return db


if __name__ == '__main__':
    db = connect()
