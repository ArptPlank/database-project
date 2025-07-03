# 家具城进销存管理系统

## 项目简介

本项目是一个基于Python和MongoDB的家具城进销存管理系统，提供完整的家具进销存业务流程管理功能。

## 功能特性

### 基础数据管理
- **家具类型管理**: 管理家具分类信息
- **供应商管理**: 管理供应商基本信息和联系方式
- **客户管理**: 管理客户信息和联系方式
- **家具信息管理**: 管理家具基本信息、规格和价格

### 业务操作
- **家具入库管理**: 记录家具入库信息，自动更新库存
- **家具销售管理**: 处理销售订单，自动检查库存并更新
- **收款管理**: 管理销售收款记录和状态

### 统计查询
- **进销存统计**: 按时间段统计各类家具的入库和销售情况
- **数据导出**: 支持将统计数据导出为CSV格式

### 技术特性
- **自动库存管理**: 入库和销售时自动更新库存数量（触发器功能）
- **数据完整性**: 通过MongoDB索引和应用层验证确保数据完整性
- **聚合统计**: 使用MongoDB聚合管道实现复杂统计查询（存储过程功能）

## 技术栈

- **编程语言**: Python 3.x
- **数据库**: MongoDB
- **GUI框架**: Tkinter
- **数据库驱动**: PyMongo

## 环境要求

### 软件环境
- Python 3.7 或更高版本
- MongoDB 4.0 或更高版本
- Conda（推荐使用db环境）

### Python依赖包
- pymongo==4.6.0
- tkinter（Python标准库）
- datetime（Python标准库）
- bson（pymongo依赖）

## 安装和运行

### 1. 环境准备

```bash
# 创建conda环境（如果没有db环境）
conda create -n db python=3.9
conda activate db

# 或者激活现有的db环境
conda activate db
```

### 2. 安装依赖

```bash
# 安装Python依赖
pip install -r requirements.txt
```

### 3. 启动MongoDB

确保MongoDB服务正在运行：

```bash
# Windows
net start MongoDB

# Linux/macOS
sudo systemctl start mongod
# 或
mongod
```

### 4. 运行程序

```bash
# 在db环境中运行
python main.py
```

## 项目结构

```
家具进销管理系统/
├── main.py                 # 主入口程序
├── requirements.txt        # 依赖包列表
├── README.md              # 项目说明文档
├── database.py            # 数据库连接模块
├── models.py              # 数据模型定义
├── gui_utils.py           # GUI工具类
├── main_window.py         # 主窗口
├── furniture_type_window.py    # 家具类型管理窗口
├── supplier_window.py     # 供应商管理窗口
├── customer_window.py     # 客户管理窗口
├── furniture_window.py    # 家具信息管理窗口
├── stock_in_window.py     # 入库管理窗口
├── sales_window.py        # 销售管理窗口
├── payment_window.py      # 收款管理窗口
└── statistics_window.py   # 统计查询窗口
```

## 数据库设计

### 集合（Collections）

1. **furniture_types** - 家具类型
   - type_code: 类型编码（唯一索引）
   - type_name: 类型名称
   - description: 描述

2. **suppliers** - 供应商
   - supplier_code: 供应商编码（唯一索引）
   - name: 供应商名称
   - contact_person: 联系人
   - phone: 电话
   - address: 地址
   - email: 邮箱

3. **customers** - 客户
   - customer_code: 客户编码（唯一索引）
   - name: 客户名称
   - phone: 电话
   - address: 地址
   - email: 邮箱

4. **furniture** - 家具信息
   - furniture_code: 家具编码（唯一索引）
   - name: 家具名称
   - type_code: 类型编码
   - specification: 规格
   - unit_price: 单价
   - stock_quantity: 库存数量

5. **stock_in** - 入库记录
   - record_id: 记录ID
   - furniture_code: 家具编码
   - supplier_code: 供应商编码
   - quantity: 入库数量
   - unit_price: 单价
   - total_amount: 总金额
   - record_date: 入库日期（索引）

6. **sales** - 销售记录
   - sale_id: 销售ID
   - furniture_code: 家具编码
   - customer_code: 客户编码
   - quantity: 销售数量
   - unit_price: 单价
   - total_amount: 总金额
   - sale_date: 销售日期（索引）
   - payment_status: 付款状态

7. **payments** - 收款记录
   - payment_id: 收款ID
   - sale_id: 销售ID
   - amount: 收款金额
   - payment_method: 收款方式
   - payment_date: 收款日期

## 使用说明

### 1. 初始数据设置
- 首先添加家具类型
- 然后添加供应商和客户信息
- 最后添加家具基本信息

### 2. 业务操作流程
- **入库**: 选择家具和供应商，输入数量和单价，系统自动更新库存
- **销售**: 选择家具和客户，输入数量，系统检查库存并自动更新
- **收款**: 选择未收款的销售记录，录入收款信息

### 3. 统计查询
- 设置查询时间范围
- 查看详细的进销存统计
- 可导出统计数据为CSV文件

## 注意事项

1. **数据库连接**: 确保MongoDB服务正常运行，默认连接localhost:27017
2. **数据备份**: 建议定期备份MongoDB数据
3. **权限管理**: 实际部署时建议配置MongoDB认证
4. **性能优化**: 大数据量时可考虑添加更多索引

## 故障排除

### 常见问题

1. **连接数据库失败**
   - 检查MongoDB服务是否启动
   - 确认连接地址和端口是否正确

2. **模块导入错误**
   - 确保已安装所有依赖包
   - 检查Python环境是否正确

3. **界面显示问题**
   - 确保系统支持Tkinter
   - 检查屏幕分辨率设置

## 开发计划

- [ ] 添加用户权限管理
- [ ] 支持数据导入功能
- [ ] 添加报表打印功能
- [ ] 实现Web版本
- [ ] 添加移动端支持

## 许可证

本项目采用MIT许可证，详情请参阅LICENSE文件。

## 联系方式

如有问题或建议，请通过以下方式联系：
- 项目Issues: [GitHub Issues](链接)
- 邮箱: your-email@example.com 