"""
数据库连接模块
"""
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import logging

class DatabaseManager:
    def __init__(self, host='localhost', port=27017, db_name='furniture_management'):
        """
        初始化数据库连接
        """
        self.host = host
        self.port = port
        self.db_name = db_name
        self.client = None
        self.db = None
        self.connect()
        
    def connect(self):
        """
        连接到MongoDB数据库
        """
        try:
            self.client = MongoClient(self.host, self.port)
            # 测试连接
            self.client.admin.command('ping')
            self.db = self.client[self.db_name]
            print(f"成功连接到MongoDB数据库: {self.db_name}")
            
            # 创建索引
            self.create_indexes()
            
        except ConnectionFailure as e:
            print(f"连接数据库失败: {e}")
            raise
    
    def create_indexes(self):
        """
        创建必要的索引
        """
        try:
            # 家具信息索引
            self.db.furniture.create_index("furniture_code", unique=True)
            
            # 供应商索引
            self.db.suppliers.create_index("supplier_code", unique=True)
            
            # 客户索引
            self.db.customers.create_index("customer_code", unique=True)
            
            # 入库记录索引
            self.db.stock_in.create_index("record_date")
            
            # 销售记录索引
            self.db.sales.create_index("sale_date")
            
            print("数据库索引创建完成")
            
        except Exception as e:
            print(f"创建索引时出错: {e}")
    
    def get_collection(self, collection_name):
        """
        获取集合
        """
        if self.db is None:
            raise Exception("数据库未连接")
        return self.db[collection_name]
    
    def close(self):
        """
        关闭数据库连接
        """
        if self.client:
            self.client.close()
            print("数据库连接已关闭")

# 全局数据库实例
db_manager = DatabaseManager() 