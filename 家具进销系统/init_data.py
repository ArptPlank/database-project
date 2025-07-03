"""
初始化演示数据脚本
用于创建一些基础数据以便测试和演示系统功能
"""
from datetime import datetime, timedelta
from models import FurnitureType, Supplier, Customer, Furniture, StockIn, Sales
from gui_utils import GUIUtils

def init_furniture_types():
    """初始化家具类型数据"""
    print("正在初始化家具类型数据...")
    furniture_type = FurnitureType()
    
    types_data = [
        ("ST01", "沙发", "各种款式的沙发"),
        ("TB01", "餐桌", "餐厅用餐桌"),
        ("BD01", "床", "卧室用床"),
        ("CH01", "椅子", "各种椅子"),
        ("CB01", "柜子", "储物柜、衣柜等"),
        ("DK01", "书桌", "学习办公用桌"),
    ]
    
    for type_code, type_name, description in types_data:
        try:
            # 检查是否已存在
            if not furniture_type.find_one({"type_code": type_code}):
                furniture_type.create_type(type_code, type_name, description)
                print(f"  ✓ 添加家具类型: {type_code} - {type_name}")
            else:
                print(f"  - 家具类型已存在: {type_code} - {type_name}")
        except Exception as e:
            print(f"  ✗ 添加家具类型失败: {type_code} - {e}")

def init_suppliers():
    """初始化供应商数据"""
    print("正在初始化供应商数据...")
    supplier = Supplier()
    
    suppliers_data = [
        ("SUP001", "美家家具有限公司", "张经理", "138-0000-1111", "北京市朝阳区家具街1号", "meijia@example.com"),
        ("SUP002", "舒适家居制造厂", "李总", "139-0000-2222", "广东省佛山市家具城2号", "shushi@example.com"),
        ("SUP003", "现代风格家具", "王主任", "137-0000-3333", "上海市浦东新区工业园3号", "xiandai@example.com"),
        ("SUP004", "经典家具工厂", "赵厂长", "136-0000-4444", "江苏省苏州市家具区4号", "jingdian@example.com"),
        ("SUP005", "时尚家居供应商", "钱总监", "135-0000-5555", "浙江省杭州市家具市场5号", "shishang@example.com"),
    ]
    
    for supplier_code, name, contact_person, phone, address, email in suppliers_data:
        try:
            if not supplier.find_one({"supplier_code": supplier_code}):
                supplier.create_supplier(supplier_code, name, contact_person, phone, address, email)
                print(f"  ✓ 添加供应商: {supplier_code} - {name}")
            else:
                print(f"  - 供应商已存在: {supplier_code} - {name}")
        except Exception as e:
            print(f"  ✗ 添加供应商失败: {supplier_code} - {e}")

def init_customers():
    """初始化客户数据"""
    print("正在初始化客户数据...")
    customer = Customer()
    
    customers_data = [
        ("CUS001", "刘先生", "186-1111-0001", "北京市海淀区中关村1号", "liu@example.com"),
        ("CUS002", "陈女士", "187-1111-0002", "上海市静安区南京路2号", "chen@example.com"),
        ("CUS003", "张总", "188-1111-0003", "广州市天河区珠江路3号", "zhang@example.com"),
        ("CUS004", "李经理", "189-1111-0004", "深圳市南山区科技园4号", "li@example.com"),
        ("CUS005", "王主任", "185-1111-0005", "杭州市西湖区文三路5号", "wang@example.com"),
        ("CUS006", "赵老师", "183-1111-0006", "南京市玄武区中山路6号", "zhao@example.com"),
        ("CUS007", "钱医生", "182-1111-0007", "成都市锦江区春熙路7号", "qian@example.com"),
        ("CUS008", "孙工程师", "181-1111-0008", "武汉市武昌区中南路8号", "sun@example.com"),
    ]
    
    for customer_code, name, phone, address, email in customers_data:
        try:
            if not customer.find_one({"customer_code": customer_code}):
                customer.create_customer(customer_code, name, phone, address, email)
                print(f"  ✓ 添加客户: {customer_code} - {name}")
            else:
                print(f"  - 客户已存在: {customer_code} - {name}")
        except Exception as e:
            print(f"  ✗ 添加客户失败: {customer_code} - {e}")

def init_furniture():
    """初始化家具信息数据"""
    print("正在初始化家具信息数据...")
    furniture = Furniture()
    
    furniture_data = [
        # 沙发类
        ("F001", "三人位真皮沙发", "ST01", "200x90x85cm，真皮材质", 3500.00, 15),
        ("F002", "L型布艺沙发", "ST01", "280x180x85cm，布艺材质", 2800.00, 12),
        ("F003", "单人休闲沙发", "ST01", "80x85x90cm，皮质+布艺", 1200.00, 20),
        
        # 餐桌类
        ("F004", "实木六人餐桌", "TB01", "160x90x75cm，橡木材质", 2200.00, 8),
        ("F005", "大理石四人餐桌", "TB01", "120x80x75cm，大理石台面", 3200.00, 5),
        ("F006", "折叠小餐桌", "TB01", "80x80x75cm，可折叠设计", 680.00, 25),
        
        # 床类
        ("F007", "1.8米双人床", "BD01", "180x200x40cm，实木床架", 1800.00, 10),
        ("F008", "1.5米单人床", "BD01", "150x200x40cm，金属床架", 1200.00, 15),
        ("F009", "儿童上下铺", "BD01", "90x190x150cm，环保材质", 2500.00, 6),
        
        # 椅子类
        ("F010", "办公转椅", "CH01", "60x60x110cm，可升降", 450.00, 30),
        ("F011", "实木餐椅", "CH01", "45x50x85cm，橡木材质", 320.00, 40),
        ("F012", "休闲摇椅", "CH01", "70x90x100cm，藤编材质", 580.00, 12),
        
        # 柜子类
        ("F013", "四门衣柜", "CB01", "200x60x220cm，实木材质", 2800.00, 8),
        ("F014", "电视柜", "CB01", "150x40x50cm，现代简约", 680.00, 18),
        ("F015", "书柜", "CB01", "120x30x180cm，多层设计", 980.00, 12),
        
        # 书桌类
        ("F016", "学生书桌", "DK01", "120x60x75cm，带抽屉", 580.00, 22),
        ("F017", "办公桌", "DK01", "140x70x75cm，现代风格", 850.00, 15),
        ("F018", "电脑桌", "DK01", "100x50x75cm，紧凑设计", 380.00, 28),
    ]
    
    for furniture_code, name, type_code, specification, unit_price, stock_quantity in furniture_data:
        try:
            if not furniture.find_one({"furniture_code": furniture_code}):
                furniture.create_furniture(furniture_code, name, type_code, specification, unit_price, stock_quantity)
                print(f"  ✓ 添加家具: {furniture_code} - {name}")
            else:
                print(f"  - 家具已存在: {furniture_code} - {name}")
        except Exception as e:
            print(f"  ✗ 添加家具失败: {furniture_code} - {e}")

def init_stock_in_records():
    """初始化入库记录数据"""
    print("正在初始化入库记录数据...")
    stock_in = StockIn()
    
    # 生成最近30天的入库记录
    base_date = datetime.now() - timedelta(days=30)
    
    stock_in_data = [
        # (家具编码, 供应商编码, 数量, 单价, 日期偏移)
        ("F001", "SUP001", 10, 2800.00, 1),
        ("F002", "SUP001", 8, 2200.00, 2),
        ("F003", "SUP002", 15, 950.00, 3),
        ("F004", "SUP003", 5, 1800.00, 5),
        ("F005", "SUP003", 3, 2500.00, 6),
        ("F006", "SUP004", 20, 550.00, 8),
        ("F007", "SUP002", 8, 1400.00, 10),
        ("F008", "SUP002", 12, 950.00, 12),
        ("F009", "SUP005", 4, 2000.00, 14),
        ("F010", "SUP004", 25, 350.00, 15),
        ("F011", "SUP003", 30, 250.00, 16),
        ("F012", "SUP005", 10, 450.00, 18),
        ("F013", "SUP001", 6, 2200.00, 20),
        ("F014", "SUP004", 15, 550.00, 22),
        ("F015", "SUP003", 10, 780.00, 24),
        ("F016", "SUP005", 18, 450.00, 25),
        ("F017", "SUP004", 12, 680.00, 26),
        ("F018", "SUP002", 25, 300.00, 28),
    ]
    
    for furniture_code, supplier_code, quantity, unit_price, day_offset in stock_in_data:
        try:
            record_date = base_date + timedelta(days=day_offset)
            total_amount = quantity * unit_price
            
            # 检查是否已有相似记录（避免重复初始化）
            existing = stock_in.find_one({
                "furniture_code": furniture_code,
                "supplier_code": supplier_code,
                "record_date": {"$gte": record_date.replace(hour=0, minute=0, second=0),
                               "$lt": record_date.replace(hour=23, minute=59, second=59)}
            })
            
            if not existing:
                stock_in.create_stock_in(furniture_code, supplier_code, quantity, unit_price, total_amount, record_date)
                print(f"  ✓ 添加入库记录: {furniture_code} - 数量:{quantity}")
            else:
                print(f"  - 入库记录已存在: {furniture_code} - {record_date.strftime('%Y-%m-%d')}")
        except Exception as e:
            print(f"  ✗ 添加入库记录失败: {furniture_code} - {e}")

def init_sales_records():
    """初始化销售记录数据"""
    print("正在初始化销售记录数据...")
    sales = Sales()
    
    # 生成最近20天的销售记录
    base_date = datetime.now() - timedelta(days=20)
    
    sales_data = [
        # (家具编码, 客户编码, 数量, 单价, 日期偏移)
        ("F001", "CUS001", 2, 3500.00, 2),
        ("F003", "CUS002", 3, 1200.00, 3),
        ("F006", "CUS003", 4, 680.00, 4),
        ("F010", "CUS004", 5, 450.00, 5),
        ("F011", "CUS005", 8, 320.00, 6),
        ("F007", "CUS001", 1, 1800.00, 8),
        ("F014", "CUS006", 2, 680.00, 9),
        ("F016", "CUS007", 3, 580.00, 10),
        ("F018", "CUS008", 4, 380.00, 11),
        ("F002", "CUS002", 1, 2800.00, 12),
        ("F012", "CUS003", 2, 580.00, 13),
        ("F015", "CUS004", 1, 980.00, 14),
        ("F004", "CUS005", 1, 2200.00, 15),
        ("F008", "CUS006", 2, 1200.00, 16),
        ("F017", "CUS007", 1, 850.00, 17),
        ("F005", "CUS008", 1, 3200.00, 18),
    ]
    
    for furniture_code, customer_code, quantity, unit_price, day_offset in sales_data:
        try:
            sale_date = base_date + timedelta(days=day_offset)
            total_amount = quantity * unit_price
            
            # 检查是否已有相似记录
            existing = sales.find_one({
                "furniture_code": furniture_code,
                "customer_code": customer_code,
                "sale_date": {"$gte": sale_date.replace(hour=0, minute=0, second=0),
                             "$lt": sale_date.replace(hour=23, minute=59, second=59)}
            })
            
            if not existing:
                sales.create_sale(furniture_code, customer_code, quantity, unit_price, total_amount, sale_date)
                print(f"  ✓ 添加销售记录: {furniture_code} - 数量:{quantity}")
            else:
                print(f"  - 销售记录已存在: {furniture_code} - {sale_date.strftime('%Y-%m-%d')}")
        except Exception as e:
            print(f"  ✗ 添加销售记录失败: {furniture_code} - {e}")

def main():
    """主函数"""
    print("=" * 50)
    print("家具城进销存管理系统 - 初始化演示数据")
    print("=" * 50)
    
    try:
        # 按顺序初始化数据（注意依赖关系）
        init_furniture_types()
        print()
        
        init_suppliers()
        print()
        
        init_customers()
        print()
        
        init_furniture()
        print()
        
        init_stock_in_records()
        print()
        
        init_sales_records()
        print()
        
        print("=" * 50)
        print("✓ 演示数据初始化完成！")
        print("现在可以运行 python main.py 启动系统")
        print("=" * 50)
        
    except Exception as e:
        print(f"初始化过程中出现错误: {e}")
        print("请检查MongoDB是否正常运行")

if __name__ == "__main__":
    main() 