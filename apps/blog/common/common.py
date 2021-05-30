# -*- coding: utf-8 -*-

import configparser
import os, time, datetime
import shutil
import logging
from logging import handlers
import paramiko
import select
from hashlib import md5
import base64
import random
from datetime import date, timedelta
import cx_Oracle
import xmltodict
import json
from ftplib import FTP
from displayfunction import display

# 当前目录
current_path = os.path.dirname(__file__)
# 项目根目录
root_path = os.path.abspath(current_path).split('apps')[0]
# 创建日志目录
logs_path = os.path.join(root_path, 'logs')
log_path = os.path.join(logs_path, 'log')
loghis_path = os.path.join(logs_path, 'loghis')

now = time.strftime("%Y%m%d", time.localtime(time.time()))
filename = now + '_console.log'
logfile = os.path.join(log_path, filename)


def getconfig(index, key):
    parent = os.path.dirname(current_path)
    targetpath = os.path.join(parent, "conf\\config.ini").replace('\\', '/')
    conf = configparser.ConfigParser()
    conf.read(targetpath, encoding="utf-8")
    value = conf[index][key]
    return value


class Oracle(object):
    # os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

    def __init__(self, section, notLatin1=True):
        if notLatin1:
            os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.ZHS16GBK'
        else:
            # 走WE8ISO8859P1字符集之后，查询出的中文数据得转码，string.encode('iso-8859-1').decode('gbk')
            os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.WE8ISO8859P1'
            user = getconfig(section, 'username')
            pwd = getconfig(section, 'userpwd')
            ip = getconfig(section, 'host')
            port = getconfig(section, 'port')
            sid = getconfig(section, 'sid')
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
    def query(self, selectSql):
        try:
            self.cursor.execute(selectSql)
            # 获取数据表的列名并输出
            # title = [i[0] for i in self.cursor.description]
            # self.cursor.rowfactory = lambda args: dict(zip(title, args))
            rows = self.cursor.fetchall()
            return rows
            # for row in rows:
            #     print("%d %s" % row)
        except Exception as e:
            print("查询失败：%s" % e)

    # 更新函数
    def update(self, updateSql):
        try:
            self.cursor.execute(updateSql)
            self.conn.commit()
            print(str(self.cursor.rowcount) + "has be updated.")
        except Exception as e:
            print(e)

    # 批量插入函数
    def insert(self, insertSql, insertDatas):
        try:
            self.cursor.executemany(insertSql, insertDatas)
            self.conn.commit()
            print(str(self.cursor.rowcount) + "has be inserted.")
            '''
            样例：
            insertSql =  "insert into tablename values(:1,:2)"
            insertDatas = [(1,'a'),(2,'b'),(3,'c'),(4,'d'),(5,'e'),(6,'f'),(7,'g'),(8,'h')]
            则插入8条数据
            '''
        except Exception as e:
            print("插入失败：%s" % e)

    # 删除函数
    def delete(self, deleteSql):
        try:
            self.cursor.execute(deleteSql)
            self.conn.commit()
            print(str(self.cursor.rowcount) + " has be deleted.")
        except Exception as e:
            print(e)


class Logger(logging.Logger):
    # 日志级别关系映射
    leve_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'crit': logging.CRITICAL
    }

    def __init__(self, filename=logfile, level='debug', when='D', backCount=3,
                 fmt='[%(asctime)s] - [%(levelname)s] - [thread:%(thread)s]: %(message)s'):
        super(Logger, self).__init__(self)
        # 设置日志格式
        format_str = logging.Formatter(fmt)
        Logfile = handlers.TimedRotatingFileHandler(filename=filename, when=when, backupCount=backCount,
                                                    encoding='utf-8')
        # 指定间隔时间自动生成文件处理器
        # 实例化TimedRotatingFileHandler
        # interval是间隔时间，backupCount是备份文件的个数，如果超过这个个数就会自动删除，when是间隔的时间单位，单位有以下几种：
        # S 秒
        # M 分
        # H 小时
        # D 天
        # W 每星期{0-6} （interval==0时代表星期一）
        # midnight 每天凌晨
        Logfile.setLevel(self.leve_relations.get(level))  # 设置日志级别
        Logfile.setFormatter(format_str)  # 设置文件里写入的格式
        # 往屏幕上输出
        console_out = logging.StreamHandler()
        # 设置屏幕上显示的格式
        console_out.setFormatter(format_str)
        # 加入handler
        self.addHandler(Logfile)
        self.addHandler(console_out)


def remove_files():
    '''
    1、将log目录下日志定期移入loghis下；
    2、定期清理loghis下日志文件
    :return:
    '''
    if not os.path.exists(logs_path):
        os.mkdir(logs_path)
        os.mkdir(log_path)
        os.mkdir(loghis_path)
    else:
        if not os.path.exists(log_path):
            os.mkdir(log_path)
        elif not os.path.exists(loghis_path):
            os.mkdir(loghis_path)
    # 删除log目录下前一天文件
    breoneday = time.time() - 3600 * 24 * 1
    filelist = os.listdir(log_path)
    for file in filelist:
        filename = log_path + os.sep + file
        if os.path.getmtime(filename) < breoneday:
            try:
                if os.path.isfile(filename):
                    shutil.move(filename, loghis_path)
                    print("%s move to loghis success." % filename)
                else:
                    continue
            except Exception as e:
                print("%s move faild, the reason is %s" % (filename, str(e)))
    # 删除loghis目录下七天前的文件
    bresevenday = time.time() - 3600 * 24 * 7
    filehislist = os.listdir(loghis_path)
    for file in filehislist:
        filename = loghis_path + os.sep + file
        if os.path.getmtime(filename) < bresevenday:
            try:
                os.remove(filename)
                print("remove %s from %s ok." % (filename, loghis_path))
            except Exception as e:
                print("%s move faild, the reason is %s." % (filename, e))
        else:
            continue


def sshRunCmd(hostname, username, passwod, cmdlist):
    '''
    通过paramiko远程调用linux指令
    :param hostname: 主机IP
    :param username: 登录用户
    :param passwod: 登录密码
    :param cmdlist: 指令
    :return:
    '''
    try:
        # 创建ssh对象
        client = paramiko.SSHClient()
        # 如果之前没有连接过的ip，会出现 Are you sure you want to continue connecting(yes/no)? yes；自动选择yes
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # 创建ssh连接
        client.connect(hostname=hostname, port=22, username=username, password=passwod, timeout=10)
        # 执行指令
        start = time.time()
        stdin, stdout, stderr = client.exec_command(cmdlist)
        end = time.time()
        result = stdout.read().decode('UTF-8').strip()
        logging.info("命令耗时：%.2f秒" % (end - start))
        logging.info(result)
        return result
    except Exception as e:
        logging.error("[%s] %s target failed, the reason is %s" % (
            datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), hostname, str(e)))
        return e
    finally:
        client.close()


def encrypt_md5(instr):
    '''
    md5加密
    :param instr: 明文字符串
    :return:
    '''
    MD5 = md5()
    # 这里必须用encode()函数对字符串编码，不然会报 TypeError: Unicode-objects must be encoded before hashing
    MD5.update(str(instr).encode(encoding='utf-8'))
    encrypt = MD5.hexdigest().upper()
    logging.info(encrypt)
    return encrypt


def encrypt_base64(instr):
    '''
    base64加密
    :param instr:
    :return:
    '''
    encodestr = base64.b64encode(instr.encode('utf-8'))
    return str(encodestr, 'utf-8')


def decrypt_base64(instr):
    '''
    base64解密
    :param instr:
    :return:
    '''
    try:
        decodestr = base64.b64decode(instr)
        return str(decodestr, 'utf-8')
    except Exception as e:
        logging.info("base64解码失败：%s" % e)
        return e


def picToBase64(image):
    '''
    图片base64化
    :param image: 前台传递的图片
    :return:
    '''
    if image:
        temp_path = os.path.join(logs_path, 'tempimg')
        curtime = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
        image_name = str(curtime) + str(image)
        image_path = "%s/%s" % (temp_path, image_name)
        if not os.path.exists(temp_path):
            os.mkdir(temp_path)
        with open(image_path, 'wb+') as f:
            for content in image.chunks():
                f.write(content)
        try:
            with open(image_path, 'rb') as pf:
                data = pf.read()
                encodestr = base64.b64encode(data)  # 得到byte编码数据
                image_encode = str(encodestr, 'utf-8')
                return image_encode
        except Exception as e:
            logging.error("请检查图片是否正确：%s" % e)
        finally:
            logging.info("base64加密完成，删除%s" % image_path)
            os.remove(image_path)
    else:
        pont = "请先上传图片"
        return pont


def XmlToJson(instr):
    '''
    xml报文转换为json报文
    :param instr: xml格式报文
    :return:
    '''
    try:
        convertDict = xmltodict.parse(instr)
        jsonStr = json.dumps(convertDict, sort_keys=True, indent=4, ensure_ascii=False, separators=(',', ': '))
        jsonmsg = json.loads(jsonStr)
        return jsonmsg
    except Exception as e:
        logging.error("转换失败：%s" % e)
        return e


class generateIdNumber():
    def zoneCodeName():
        '''
        区划编码、名称字典组
        :return:
        '''
        dict_temp = {}
        with open(r'D:\liums\InterChannBlog\static\uploads\files\identityTop6.txt', mode='r', encoding='utf-8') as f:
            for line in f.readlines():
                # 如果每行中去重后不为空，且6位数字中最后两位部位00，则添加到列表中。（最后两位为00时为省份或地市级代码）
                if line.strip() != '' and (line.strip())[:6][-2:] != '00':
                    kv = line.strip().split(',')
                    dict_temp[kv[0]] = kv[1]
            return dict_temp

    def generate_certId(self, gender, count=10):
        '''
        身份证号生成
        :param gender: 性别 1：男，0：女
        :param count: 生成证件个数
        :return: 身份证详情
        '''
        gender_realtion = {'1': '男', '0': '女'}
        certid_key = random.sample(generateIdNumber.zoneCodeName().keys(), count)
        # 权重项
        weight = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
        # 校验码
        check_code_list = [1, 0, 'X', 9, 8, 7, 6, 5, 4, 3, 2]
        age = random.randint(18, 66)
        birthday = str(date(date.today().year - age, 1, 1) + timedelta(days=random.randint(0, 365)))
        datestring = birthday.replace("-", "")
        rd = random.randint(0, 999)
        if gender == 0:
            gender_num = rd if rd % 2 == 0 else rd + 1
        else:
            gender_num = rd if rd % 2 == 1 else rd - 1
        list = []
        for number in certid_key:
            result = str(number) + datestring + str(gender_num).zfill(3)
            certid_value = generateIdNumber.zoneCodeName()[number]
            certid = '%s, %s, %s, %s, %s' % (
            result + str(check_code_list[sum([a * b for a, b in zip(weight, [int(a) for a in result])]) % 11]),
            certid_value, birthday, age, gender_realtion.get(str(gender)))
            list.append(certid)
        return list

class ftp_updown(object):
    # 连接ftp
    def ftpconnect(host, username,password):
        ftp = FTP()
        ftp.connect(host, 21)
        ftp.login(username, password)
        return ftp
    # 上传本地文件到ftp
    def uploadfile(ftp, remotepath, localpath):
        bufsize = 1024
        fp = open(localpath, 'rb')
        ftp.storbinary('SORT ' + remotepath, fp, bufsize)
        ftp.set_debuglevel(0)
        ftp.quit()
    # 下载本地文件到本地
    def downloadfile(ftp, remotpath, localpath):
        bufsize = 1024
        fp = open(localpath, 'wb')
        ftp.retrbinary('RETR ' + remotpath, fp, bufsize)
        ftp.set_debuglevel(0)
        ftp.quit()
