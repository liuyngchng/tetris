import logging  # 引入logging模块

# logging.basicConfig函数对日志的输出格式及方式做相关配置
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')


if __name__ == '__main__':
    # 由于日志基本配置中级别设置为DEBUG，所以一下打印信息将会全部显示在控制台上
    a = 123
    logging.info('this is a logging info message %s', a)
    logging.debug('this is a logging debug message')
    logging.warning('this is logging a warning message')
    logging.error('this is an logging error message')
    logging.critical('this is a logging critical message')
    logging.debug("sqs.squares:\r\n")
