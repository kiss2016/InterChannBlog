# -*- coding: utf-8 -*-

import configparser
import os
import cx_Oracle
from displayfunction import display


def getconfig(index, key):
    curpath = os.path.dirname(os.path.realpath(__file__))
    print(curpath)
    parent = os.path.dirname(curpath)
    print(parent)
    targetpath = os.path.join(parent, "conf\\config.ini")
    conf = configparser.ConfigParser()
    conf.read(targetpath, encoding="utf-8")
    value = conf[index][key]
    return value


if __name__ == '__main__':
    getconfig('DATABASE', 'user')


class Oracle():
    os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

    def __init__(self, user, pwd, ip, port, sid):
        try:
            self.conn = cx_Oracle.connect(user + '/' + pwd + '@' + ip + ':' + port + '/' + sid)
            self.cursor = self.conn.cursor()
        except Exception as e:
            print("oracle connect error,[name=%s,password=%s,host=%s,sid=%s]!%s" % (
                self.user, self.pwd, self.ip, self.sid, e))

    # 关闭连接函数
    def closeConn(self):
        self.cursor.close()
        self.conn.close()

    # 查询函数
    def select(self, selectSql):
        try:
            self.cursor.execute(selectSql)
            rows = self.cursor.fetchall()
            for row in rows:
                print("%d %s" % row)
        except Exception as e:
            print(e)
        finally:
            self.closeConn()

    # 更新函数
    def update(self, updateSql):
        try:
            self.cursor.execute(updateSql)
            self.conn.commit()
        except Exception as e:
            print(e)
        finally:
            self.closeConn()

    # 批量插入函数
    def insert(self, insertSql, insertDatas):
        try:
            self.cursor.executemany(insertSql, insertDatas)
            self.conn.commit()
            '''
            样例：
            insertSql =  "insert into tablename values(:1,:2)"
            insertDatas = [(1,'a'),(2,'b'),(3,'c'),(4,'d'),(5,'e'),(6,'f'),(7,'g'),(8,'h')]
            则插入8条数据
            '''
        except Exception as e:
            print(e)
        finally:
            self.closeConn()

    # 删除函数
    def delete(self, deleteSql):
        try:
            print("Begin deleting...")
            self.cursor.execute(deleteSql)
            print(str(self.cursor.rowcount) + " has be deleted.")
            self.conn.commit()
            print("End deleting...")
        except Exception as e:
            print(e)
        finally:
            self.closeConn()
