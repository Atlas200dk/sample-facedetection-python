#! /usr/bin/env python
#coding=utf-8

class Head(object):
    def __init__(self):
        self.left = None
        self.right = None

class Node(object):
    def __init__(self, value):
        self.value = value
        self.next = None

class Queue(object):
    def __init__(self):
        #初始化节点
        self.head = Head()

    def put(self, value):
        #插入一个元素
        newnode = Node(value)
        p = self.head
        if p.right:
            #如果head节点的右边不为None
            #说明队列中已经有元素了
            #就执行下列的操作
            temp = p.right
            p.right = newnode
            temp.next = newnode
        else:
            #这说明队列为空，插入第一个元素
            p.right = newnode
            p.left = newnode

    def get(self):
        #取出一个元素
        p = self.head
        if p.left and (p.left == p.right):
            #说明队列中已经有元素
            #但是这是最后一个元素
            temp = p.left
            p.left = p.right = None
            return temp.value
        elif p.left and (p.left != p.right):
            #说明队列中有元素，而且不止一个
            temp = p.left
            p.left = temp.next
            return temp.value

        else:
            #说明队列为空
            #抛出查询错误
            raise LookupError('queue is empty!')

    def is_empty(self):
        if self.head.left:
            return False
        else:
            return True

    def top(self):
        #查询目前队列中最早入队的元素
        if self.head.left:
            return self.head.left.value
        else:
            raise LookupError('queue is empty!')