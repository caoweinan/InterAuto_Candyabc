import pymysql
from utils.LogUtil import my_log


class Mysql:

    def __init__(self, host, user, password, database, charset="utf8", port=3306):

        self.log = my_log()

        self.conn = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            charset=charset,
            port=port)

        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    def fetchone(self, sql):
        """
        单个查询
        :param sql:
        :return:
        """
        self.cursor.execute(sql)
        return self.cursor.fetchone()

    def fetchall(self, sql):
        """
        多个查询
        :param sql:
        :return:
        """
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def exec(self, sql):
        """
        执行
        :return:
        """
        try:
            if self.conn and self.cursor:
                self.cursor.execute(sql)
                self.conn.commit()
        except Exception as ex:
            self.conn.rollback()
            self.log.error("MySql 执行失败")
            self.log.error(ex)
            return False
        return True

    # 4.关闭对象
    def __del__(self):

        # 关闭光标对象
        if self.cursor is not None:
            self.cursor.close()
        # 关闭数据库连接对象
        if self.conn is not None:
            self.conn.close()


if __name__ == "__main__":
    mysql = Mysql("xxxxx",
                  "xxxxx",
                  "xxxxx",
                  "xxxxx",
                  charset="utf8mb4",
                  port=3306)
    # 查询
    res = mysql.fetchone("select * from user where mobile = '19900002000'")
    # res = mysql.fetchall("select x,x from x")

    # 更新
    # res = mysql.exec("update x set x = 'x' where x = 'x'")

    print(res)
