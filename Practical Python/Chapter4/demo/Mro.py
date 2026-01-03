# 旧式MRO DFS算法
def old_mro(cls,order):
    order.append(cls)
    for base in cls.__bases__:
        old_mro(base,order)
    return order

def improve_mro(cls,order):
    mro=old_mro(cls,order)
    dmro=[]
    dmro.append(mro[-1])
    mro.reverse()
    for item in mro:
        if item in dmro:
            continue
        dmro.append(item)
    dmro.reverse()
    return dmro

# C3 线性化算法
def merge(seq):
    result=[]
    while True:
        # 把空列表去掉
        seq=[seqs for seqs in seq if seqs]
        # 如果seq序列空了,也就是没有问题完全输出了
        if not seq:
            return result
        for seqs in seq:
            flag=seqs[0]
            if not any(flag in item[1:] for item in seq):
                break
        else:
            raise  TypeError("Inconsistent hierarchy, no C3 MRO possible")
        result.append(flag)
        # 在序列里面把他删掉
        for item in seq:
            if item and item[0] == flag:
                item.pop(0)
def C3Mro(cls):
    # 父类序列
    Base=cls.__bases__
    # 父类线性化
    BaseLinearSeq=[list(C3Mro(base)) for base in Base]
    BaseLinearSeq.append(list(Base))
    return [cls]+merge(BaseLinearSeq)