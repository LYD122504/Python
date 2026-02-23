class TaskError(Exception):
    """自定义任务异常"""
    pass
def process_data(data):
    """底层处理函数"""
    if not data:
        raise ValueError("数据不能为空")
    return data.upper()
def run_task(data):
    """上层任务函数"""
    try:
        result = process_data(data)
        return result
    except Exception as e:
        # 保留原始异常信息，创建新的异常链
        raise TaskError('It failed') from e
# 测试
try:
    run_task("")
except TaskError as e:
    print(f"捕获到: {e}")
    print(f"原始异常: {e.__cause__}")

import reader

port = reader.read_csv_as_dicts('../Data/missing.csv', types=[str, int, float])
print(len(port))