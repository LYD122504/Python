import logging
name=__name__
log=logging.getLogger(name)
log.debug("Debug message from %s", name)
log.info("Info message from %s", name)
log.warning("Warning message from %s", name)
log.error("Error message from %s", name)
log.critical("Critical message from %s", name)
logmsg="Logging setup complete in %s" % name
print(logmsg)

import logging

logger = logging.getLogger("demo")
logger.setLevel(logging.DEBUG)

# Handler 1：终端
h1 = logging.StreamHandler()
h1.setLevel(logging.INFO)

# Handler 2：文件
h2 = logging.FileHandler("app.log")
h2.setLevel(logging.WARNING)

logger.addHandler(h1)
logger.addHandler(h2)

logger.debug("debug")
logger.info("info")
logger.warning("warning")


import logging
import sys

# ============================================================
# 1. basicConfig —— 兜底配置（防止第三方库乱打日志）
# ============================================================
logging.basicConfig(
    level=logging.WARNING,  # 兜底级别
    format="%(levelname)s:%(name)s:%(message)s"
)

# ============================================================
# 2. 自定义 Filter
#    规则：过滤掉包含关键字 "ignore" 的日志
# ============================================================
class IgnoreKeywordFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return "ignore" not in record.getMessage()


# ============================================================
# 3. 创建 Logger（模块级）
# ============================================================
logger = logging.getLogger("demo.app")
logger.setLevel(logging.DEBUG)  # Logger 总闸门
logger.propagate = False        # 避免重复输出到 root logger


# ============================================================
# 4. 创建 Formatter（两个：控制台 / 文件）
# ============================================================
console_formatter = logging.Formatter(
    fmt="%(levelname)s - %(message)s"
)

file_formatter = logging.Formatter(
    fmt="%(asctime)s [%(levelname)s] "
        "%(name)s %(filename)s:%(lineno)d - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)


# ============================================================
# 5. 创建 Handler
# ============================================================

# ---- 控制台 Handler ----
console_handler = logging.StreamHandler(sys.stderr)
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(console_formatter)
console_handler.addFilter(IgnoreKeywordFilter())

# ---- 文件 Handler ----
file_handler = logging.FileHandler("app.log", mode="w", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(file_formatter)
file_handler.addFilter(IgnoreKeywordFilter())


# ============================================================
# 6. 绑定 Handler 到 Logger
# ============================================================
logger.addHandler(console_handler)
logger.addHandler(file_handler)


# ============================================================
# 7. 示例代码（模拟真实业务）
# ============================================================
def main():
    logger.debug("This is a DEBUG message")
    logger.info("Application started")
    logger.warning("Low disk space")
    logger.error("Something went wrong")

    # 这条会被 Filter 丢弃
    logger.warning("This message should be ignored")

    try:
        1 / 0
    except ZeroDivisionError:
        logger.exception("Unhandled exception occurred")


if __name__ == "__main__":
    main()