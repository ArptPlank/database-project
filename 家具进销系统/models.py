"""
数据模型模块
定义各种实体类和数据操作
"""
from datetime import datetime
from bson import ObjectId
from database import db_manager
import uuid

class BaseModel:
    """基础模型类"""
    
    def __init__(self, collection_name):
        self.collection = db_manager.get_collection(collection_name)
    
    def insert(self, data):
        """插入数据"""
        data['created_at'] = datetime.now()
        data['updated_at'] = datetime.now()
        result = self.collection.insert_one(data)
        return result.inserted_id
    
    def find_all(self, query=None):
        """查找所有数据"""
        if query is None:
            query = {}
        return list(self.collection.find(query))
    
    def find_one(self, query):
        """查找单条数据"""
        return self.collection.find_one(query)
    
    def update(self, query, update_data):
        """更新数据"""
        update_data['updated_at'] = datetime.now()
        return self.collection.update_one(query, {'$set': update_data})
    
    def delete(self, query):
        """删除数据"""
        return self.collection.delete_one(query)

class FurnitureType(BaseModel):
    """家具类型模型"""
    
    def __init__(self):
        super().__init__('furniture_types')
    
    def create_type(self, type_code, type_name, description=''):
        """创建家具类型"""
        data = {
            'type_code': type_code,
            'type_name': type_name,
            'description': description
        }
        return self.insert(data)
    
    def get_all_types(self):
        """获取所有家具类型"""
        return self.find_all()

class Supplier(BaseModel):
    """供应商模型"""
    
    def __init__(self):
        super().__init__('suppliers')
    
    def create_supplier(self, supplier_code, name, contact_person, phone, address, email=''):
        """创建供应商"""
        data = {
            'supplier_code': supplier_code,
            'name': name,
            'contact_person': contact_person,
            'phone': phone,
            'address': address,
            'email': email
        }
        return self.insert(data)
    
    def get_all_suppliers(self):
        """获取所有供应商"""
        return self.find_all()

class Customer(BaseModel):
    """客户模型"""
    
    def __init__(self):
        super().__init__('customers')
    
    def create_customer(self, customer_code, name, phone, address, email=''):
        """创建客户"""
        data = {
            'customer_code': customer_code,
            'name': name,
            'phone': phone,
            'address': address,
            'email': email
        }
        return self.insert(data)
    
    def get_all_customers(self):
        """获取所有客户"""
        return self.find_all()

class Furniture(BaseModel):
    """家具信息模型"""
    
    def __init__(self):
        super().__init__('furniture')
    
    def create_furniture(self, furniture_code, name, type_code, specification, unit_price, stock_quantity=0):
        """创建家具信息"""
        data = {
            'furniture_code': furniture_code,
            'name': name,
            'type_code': type_code,
            'specification': specification,
            'unit_price': float(unit_price),
            'stock_quantity': int(stock_quantity)
        }
        return self.insert(data)
    
    def update_stock(self, furniture_code, quantity_change):
        """更新库存数量"""
        furniture = self.find_one({'furniture_code': furniture_code})
        if furniture:
            new_quantity = furniture['stock_quantity'] + quantity_change
            if new_quantity < 0:
                raise ValueError("库存数量不能为负数")
            return self.update(
                {'furniture_code': furniture_code},
                {'stock_quantity': new_quantity}
            )
        return None
    
    def get_all_furniture(self):
        """获取所有家具信息"""
        return self.find_all()
    
    def get_by_code(self, furniture_code):
        """根据编码获取家具信息"""
        return self.find_one({'furniture_code': furniture_code})

class StockIn(BaseModel):
    """入库记录模型"""
    
    def __init__(self):
        super().__init__('stock_in')
    
    def create_stock_in(self, furniture_code, supplier_code, quantity, unit_price, total_amount, record_date=None):
        """创建入库记录"""
        if record_date is None:
            record_date = datetime.now()
        
        data = {
            'record_id': str(uuid.uuid4()),
            'furniture_code': furniture_code,
            'supplier_code': supplier_code,
            'quantity': int(quantity),
            'unit_price': float(unit_price),
            'total_amount': float(total_amount),
            'record_date': record_date
        }
        
        # 插入记录
        result_id = self.insert(data)
        
        # 更新库存（触发器功能）
        furniture = Furniture()
        furniture.update_stock(furniture_code, quantity)
        
        return result_id
    
    def get_stock_in_by_period(self, start_date, end_date):
        """获取指定时间段的入库记录"""
        query = {
            'record_date': {
                '$gte': start_date,
                '$lte': end_date
            }
        }
        return self.find_all(query)

class Sales(BaseModel):
    """销售记录模型"""
    
    def __init__(self):
        super().__init__('sales')
    
    def create_sale(self, furniture_code, customer_code, quantity, unit_price, total_amount, sale_date=None):
        """创建销售记录"""
        if sale_date is None:
            sale_date = datetime.now()
        
        # 检查库存
        furniture = Furniture()
        furniture_info = furniture.get_by_code(furniture_code)
        if not furniture_info:
            raise ValueError("家具不存在")
        
        if furniture_info['stock_quantity'] < quantity:
            raise ValueError("库存不足")
        
        data = {
            'sale_id': str(uuid.uuid4()),
            'furniture_code': furniture_code,
            'customer_code': customer_code,
            'quantity': int(quantity),
            'unit_price': float(unit_price),
            'total_amount': float(total_amount),
            'sale_date': sale_date,
            'payment_status': '未收款'
        }
        
        # 插入记录
        result_id = self.insert(data)
        
        # 更新库存（触发器功能）
        furniture.update_stock(furniture_code, -quantity)
        
        return result_id
    
    def get_sales_by_period(self, start_date, end_date):
        """获取指定时间段的销售记录"""
        query = {
            'sale_date': {
                '$gte': start_date,
                '$lte': end_date
            }
        }
        return self.find_all(query)
    
    def update_payment_status(self, sale_id, status):
        """更新付款状态"""
        return self.update({'sale_id': sale_id}, {'payment_status': status})

class Payment(BaseModel):
    """收款记录模型"""
    
    def __init__(self):
        super().__init__('payments')
    
    def create_payment(self, sale_id, amount, payment_method, payment_date=None):
        """创建收款记录"""
        if payment_date is None:
            payment_date = datetime.now()
        
        data = {
            'payment_id': str(uuid.uuid4()),
            'sale_id': sale_id,
            'amount': float(amount),
            'payment_method': payment_method,
            'payment_date': payment_date
        }
        
        # 插入收款记录
        result_id = self.insert(data)
        
        # 更新销售记录的付款状态
        sales = Sales()
        sales.update_payment_status(sale_id, '已收款')
        
        return result_id

class Statistics:
    """统计功能类（相当于存储过程）"""
    
    @staticmethod
    def get_inventory_statistics(start_date, end_date):
        """统计某段时间内各种商品的入库数量和销售数量"""
        
        # 入库统计
        stock_in_pipeline = [
            {
                '$match': {
                    'record_date': {
                        '$gte': start_date,
                        '$lte': end_date
                    }
                }
            },
            {
                '$group': {
                    '_id': '$furniture_code',
                    'total_stock_in': {'$sum': '$quantity'}
                }
            }
        ]
        
        # 销售统计
        sales_pipeline = [
            {
                '$match': {
                    'sale_date': {
                        '$gte': start_date,
                        '$lte': end_date
                    }
                }
            },
            {
                '$group': {
                    '_id': '$furniture_code',
                    'total_sales': {'$sum': '$quantity'}
                }
            }
        ]
        
        stock_in_collection = db_manager.get_collection('stock_in')
        sales_collection = db_manager.get_collection('sales')
        
        stock_in_stats = list(stock_in_collection.aggregate(stock_in_pipeline))
        sales_stats = list(sales_collection.aggregate(sales_pipeline))
        
        # 合并统计结果
        combined_stats = {}
        
        # 处理入库统计
        for item in stock_in_stats:
            furniture_code = item['_id']
            combined_stats[furniture_code] = {
                'furniture_code': furniture_code,
                'stock_in_quantity': item['total_stock_in'],
                'sales_quantity': 0
            }
        
        # 处理销售统计
        for item in sales_stats:
            furniture_code = item['_id']
            if furniture_code in combined_stats:
                combined_stats[furniture_code]['sales_quantity'] = item['total_sales']
            else:
                combined_stats[furniture_code] = {
                    'furniture_code': furniture_code,
                    'stock_in_quantity': 0,
                    'sales_quantity': item['total_sales']
                }
        
        return list(combined_stats.values()) 