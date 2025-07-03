from flask import Flask, render_template, request, jsonify, redirect, url_for, send_from_directory
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime, timedelta
import json

app = Flask(__name__)
CORS(app)

# 禁用缓存的装饰器
@app.after_request
def after_request(response):
    """禁用所有API响应的缓存"""
    if request.path.startswith('/api/'):
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
    return response

# MongoDB连接配置
client = MongoClient('mongodb://localhost:27017/')
db = client['vcd_store']

# 集合引用
vcds = db.vcds              # VCD信息集合
inventory = db.inventory    # 库存集合
sales = db.sales           # 销售记录集合
rentals = db.rentals       # 借还记录集合
customers = db.customers   # 客户信息集合
operation_logs = db.operation_logs  # 操作日志集合

@app.route('/')
def index():
    """主页"""
    return render_template('index.html')

@app.route('/vcds')
def vcd_management():
    """VCD管理页面"""
    return render_template('vcds.html')

@app.route('/inventory')
def inventory_management():
    """库存管理页面"""
    return render_template('inventory.html')

@app.route('/sales')
def sales_management():
    """销售管理页面"""
    return render_template('sales.html')

@app.route('/rentals')
def rental_management():
    """借还管理页面"""
    return render_template('rentals.html')

@app.route('/statistics')
def statistics():
    """统计报表页面"""
    return render_template('statistics.html')

@app.route('/backup')
def backup_management():
    """数据备份页面"""
    return render_template('backup.html')

@app.route('/tools')
def system_tools():
    """系统工具页面"""
    return render_template('tools.html')

@app.route('/debug')
def debug_sales():
    """调试页面"""
    return send_from_directory('.', 'debug_sales.html')

# API路由
@app.route('/api/vcds', methods=['GET', 'POST'])
def api_vcds():
    """VCD信息API"""
    if request.method == 'GET':
        vcd_list = list(vcds.find())
        for vcd in vcd_list:
            vcd['_id'] = str(vcd['_id'])
        return jsonify(vcd_list)
    
    elif request.method == 'POST':
        vcd_data = request.json
        vcd_data['created_at'] = datetime.now()
        vcd_data['updated_at'] = datetime.now()
        
        # 插入VCD信息
        result = vcds.insert_one(vcd_data)
        
        # 初始化库存信息
        inventory_data = {
            'vcd_id': result.inserted_id,
            'vcd_name': vcd_data['name'],
            'total_quantity': 0,
            'available_quantity': 0,
            'rented_quantity': 0,
            'sold_quantity': 0,
            'last_updated': datetime.now()
        }
        inventory.insert_one(inventory_data)
        
        return jsonify({'success': True, 'id': str(result.inserted_id)})

@app.route('/api/vcds/<vcd_id>', methods=['PUT', 'DELETE'])
def api_vcd_detail(vcd_id):
    """VCD详情API"""
    if request.method == 'PUT':
        vcd_data = request.json
        vcd_data['updated_at'] = datetime.now()
        
        result = vcds.update_one(
            {'_id': ObjectId(vcd_id)}, 
            {'$set': vcd_data}
        )
        
        return jsonify({'success': result.modified_count > 0})
    
    elif request.method == 'DELETE':
        # 删除VCD及相关库存信息
        vcds.delete_one({'_id': ObjectId(vcd_id)})
        inventory.delete_one({'vcd_id': ObjectId(vcd_id)})
        
        return jsonify({'success': True})

@app.route('/api/inventory', methods=['GET'])
def api_inventory():
    """库存查询API"""
    # 使用聚合管道实现库存视图
    pipeline = [
        {
            '$lookup': {
                'from': 'vcds',
                'localField': 'vcd_id',
                'foreignField': '_id',
                'as': 'vcd_info'
            }
        },
        {
            '$unwind': '$vcd_info'
        },
        {
            '$project': {
                'vcd_id': 1,
                'vcd_name': 1,
                'vcd_type': '$vcd_info.type',
                'total_quantity': 1,
                'available_quantity': 1,
                'rented_quantity': 1,
                'sold_quantity': 1,
                'last_updated': 1
            }
        }
    ]
    
    inventory_list = list(inventory.aggregate(pipeline))
    for item in inventory_list:
        item['_id'] = str(item['_id'])
        item['vcd_id'] = str(item['vcd_id'])  # 将vcd_id也转换为字符串
    
    return jsonify(inventory_list)

@app.route('/api/inventory/restock', methods=['POST'])
def api_restock():
    """入库API"""
    data = request.json
    vcd_id = data['vcd_id']
    quantity = int(data['quantity'])
    
    # 更新库存
    result = inventory.update_one(
        {'vcd_id': ObjectId(vcd_id)},
        {
            '$inc': {
                'total_quantity': quantity,
                'available_quantity': quantity
            },
            '$set': {'last_updated': datetime.now()}
        }
    )
    
    return jsonify({'success': result.modified_count > 0})

@app.route('/api/inventory/fix', methods=['POST'])
def api_fix_inventory():
    """修复库存数据 - 重新计算总库存"""
    try:
        # 获取所有库存记录
        inventories = list(inventory.find())
        fixed_count = 0
        
        for inv in inventories:
            # 重新计算正确的总库存：现货 + 借出（不包括已售）
            correct_total = inv['available_quantity'] + inv['rented_quantity']
            
            if inv['total_quantity'] != correct_total:
                # 更新总库存
                inventory.update_one(
                    {'_id': inv['_id']},
                    {
                        '$set': {
                            'total_quantity': correct_total,
                            'last_updated': datetime.now()
                        }
                    }
                )
                fixed_count += 1
        
        return jsonify({
            'success': True, 
            'message': f'成功修复 {fixed_count} 条库存记录',
            'fixed_count': fixed_count
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'修复失败: {str(e)}'})

@app.route('/api/rentals/clean', methods=['POST'])
def api_clean_rentals():
    """清理无效的租借记录"""
    try:
        # 删除无效记录（没有客户名称或VCD ID的记录）
        result = rentals.delete_many({
            '$or': [
                {'customer_name': {'$in': [None, '', 'undefined']}},
                {'vcd_id': {'$in': [None, '']}},
                {'rent_date': None}
            ]
        })
        
        return jsonify({
            'success': True, 
            'message': f'已清理 {result.deleted_count} 条无效记录'
        })
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/data/fix-all', methods=['POST'])
def api_fix_all_data():
    """全面修复数据一致性"""
    try:
        fixed_items = []
        
        # 1. 清理无效的租借记录
        invalid_rentals = rentals.delete_many({
            '$or': [
                {'customer_name': {'$in': [None, '', 'undefined']}},
                {'vcd_id': {'$in': [None, '']}},
                {'rent_date': None}
            ]
        })
        fixed_items.append(f'清理了 {invalid_rentals.deleted_count} 条无效租借记录')
        
        # 2. 重新计算所有库存数量（从入库记录开始）
        inventory_items = inventory.find()
        
        for item in inventory_items:
            vcd_id = item['vcd_id']
            
            # 统计实际入库总量（从入库记录重新计算）
            # 注意：total_quantity 应该是累积的入库数量，不受销售影响
            # 如果没有单独的入库记录表，我们需要重新设计逻辑
            
            # 暂时使用现有的逻辑，但需要确保至少满足基本约束
            current_available = item.get('available_quantity', 0)
            current_total = item.get('total_quantity', 0)
            
            # 统计当前未归还的租借数量
            current_rented = rentals.count_documents({
                'vcd_id': vcd_id,
                '$or': [
                    {'status': {'$ne': 'returned'}},
                    {'status': {'$exists': False}}
                ]
            })
            
            # 获取已销售的数量
            sold_quantity = sales.aggregate([
                {'$match': {'vcd_id': vcd_id}},
                {'$group': {'_id': None, 'total': {'$sum': '$quantity'}}}
            ])
            sold_quantity = list(sold_quantity)
            total_sold = sold_quantity[0]['total'] if sold_quantity else 0
            
            # 重新计算正确的总库存和可用库存
            # 逻辑：总库存 = 可用库存 + 借出库存 + 已销售库存
            # 如果当前数据不一致，我们需要调整总库存
            
            required_total = current_available + current_rented + total_sold
            
            # 如果当前总库存小于需要的总库存，说明总库存记录有误
            if current_total < required_total:
                # 调整总库存为实际需要的数量
                correct_total = required_total
                correct_available = current_available
            else:
                # 如果总库存足够，重新计算可用库存
                correct_total = current_total
                correct_available = max(0, correct_total - current_rented - total_sold)
            
            # 更新库存记录
            inventory.update_one(
                {'_id': item['_id']},
                {
                    '$set': {
                        'total_quantity': correct_total,
                        'available_quantity': correct_available,
                        'rented_quantity': current_rented,
                        'last_updated': datetime.now()
                    }
                }
            )
            
        fixed_items.append('重新计算了所有VCD的库存数量')
        
        # 3. 修复所有租借记录的状态
        rentals_without_status = rentals.find({'status': {'$exists': False}})
        updated_rentals = 0
        
        for rental in rentals_without_status:
            # 如果有归还日期但没有状态，标记为已归还
            if rental.get('return_date'):
                rentals.update_one(
                    {'_id': rental['_id']},
                    {'$set': {'status': 'returned'}}
                )
                updated_rentals += 1
            else:
                # 没有归还日期的标记为借出中
                rentals.update_one(
                    {'_id': rental['_id']},
                    {'$set': {'status': 'rented'}}
                )
                updated_rentals += 1
                
        if updated_rentals > 0:
            fixed_items.append(f'修复了 {updated_rentals} 条租借记录的状态')
        
        # 4. 验证数据一致性
        validation_errors = []
        all_inventory = inventory.find()
        
        for item in all_inventory:
            vcd_id = item['vcd_id']
            
            # 检查数量是否合理
            if item.get('available_quantity', 0) < 0:
                validation_errors.append(f'VCD {vcd_id} 的可用数量为负数')
            
            if item.get('rented_quantity', 0) < 0:
                validation_errors.append(f'VCD {vcd_id} 的租借数量为负数')
                
            total = item.get('total_quantity', 0)
            available = item.get('available_quantity', 0)
            rented = item.get('rented_quantity', 0)
            
            # 检查总数是否一致（考虑销售）
            sold_quantity = sales.aggregate([
                {'$match': {'vcd_id': vcd_id}},
                {'$group': {'_id': None, 'total': {'$sum': '$quantity'}}}
            ])
            sold_quantity = list(sold_quantity)
            total_sold = sold_quantity[0]['total'] if sold_quantity else 0
            
            expected_total = available + rented + total_sold
            if abs(expected_total - total) > 0:
                inventory.update_one(
                    {'_id': item['_id']},
                    {'$set': {'total_quantity': available + rented + total_sold}}
                )
                fixed_items.append(f'修复了VCD {vcd_id} 的总库存数量')
        
        return jsonify({
            'success': True,
            'message': '数据修复完成',
            'details': fixed_items,
            'validation_errors': validation_errors
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'修复过程中出错: {str(e)}'})

@app.route('/api/data/reset-all', methods=['POST'])
def api_reset_all_business_data():
    """重置所有业务数据（保留VCD信息）"""
    try:
        reset_items = []
        
        # 1. 清空所有销售记录
        sales_result = sales.delete_many({})
        reset_items.append(f'清空了 {sales_result.deleted_count} 条销售记录')
        
        # 2. 清空所有租借记录
        rentals_result = rentals.delete_many({})
        reset_items.append(f'清空了 {rentals_result.deleted_count} 条租借记录')
        
        # 3. 清空所有客户记录（可选）
        customers_result = customers.delete_many({})
        reset_items.append(f'清空了 {customers_result.deleted_count} 条客户记录')
        
        # 4. 重置所有库存为合理的默认值
        # 获取所有VCD
        all_vcds = list(vcds.find())
        
        # 清空现有库存记录
        inventory.delete_many({})
        reset_items.append('清空了所有库存记录')
        
        # 为每个VCD创建新的库存记录，设置合理的默认值
        for vcd in all_vcds:
            default_quantity = 10  # 默认每个VCD有10个库存
            
            inventory.insert_one({
                'vcd_id': vcd['_id'],
                'total_quantity': default_quantity,
                'available_quantity': default_quantity,
                'rented_quantity': 0,
                'sold_quantity': 0,
                'last_updated': datetime.now()
            })
        
        reset_items.append(f'为 {len(all_vcds)} 个VCD重新创建了库存记录，每个默认库存10个')
        
        return jsonify({
            'success': True,
            'message': '所有业务数据已重置',
            'details': reset_items
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'重置过程中出错: {str(e)}'})

@app.route('/api/sales', methods=['GET', 'POST'])
def api_sales():
    """销售API"""
    if request.method == 'GET':
        # 使用聚合管道获取销售记录和VCD信息
        pipeline = [
            {
                '$lookup': {
                    'from': 'vcds',
                    'localField': 'vcd_id',
                    'foreignField': '_id',
                    'as': 'vcd_info'
                }
            },
            {
                '$unwind': '$vcd_info'
            },
            {
                '$project': {
                    'vcd_id': 1,
                    'vcd_name': '$vcd_info.name',
                    'quantity': 1,
                    'unit_price': 1,
                    'customer_name': 1,
                    'customer_phone': 1,
                    'note': 1,
                    'sale_date': 1
                }
            },
            {
                '$sort': {'sale_date': -1}
            }
        ]
        
        sales_list = list(sales.aggregate(pipeline))
        for sale in sales_list:
            sale['_id'] = str(sale['_id'])
            sale['vcd_id'] = str(sale['vcd_id'])
        return jsonify(sales_list)
    
    elif request.method == 'POST':
        sale_data = request.json
        vcd_id = ObjectId(sale_data['vcd_id'])
        sale_data['vcd_id'] = vcd_id
        sale_data['sale_date'] = datetime.now()
        
        # 获取VCD信息
        vcd_info = vcds.find_one({'_id': vcd_id})
        if not vcd_info:
            return jsonify({'success': False, 'message': 'VCD不存在'})
        
        sale_data['vcd_name'] = vcd_info['name']
        
        # 检查库存
        inv = inventory.find_one({'vcd_id': vcd_id})
        if not inv or inv['available_quantity'] < sale_data['quantity']:
            return jsonify({'success': False, 'message': '库存不足'})
        
        # 插入销售记录
        sales.insert_one(sale_data)
        
        # 更新库存 (触发器功能)
        inventory.update_one(
            {'vcd_id': vcd_id},
            {
                '$inc': {
                    'total_quantity': -sale_data['quantity'],  # 销售后总库存也要减少
                    'available_quantity': -sale_data['quantity'],
                    'sold_quantity': sale_data['quantity']
                },
                '$set': {'last_updated': datetime.now()}
            }
        )
        
        return jsonify({'success': True})

@app.route('/api/rentals', methods=['GET', 'POST'])
def api_rentals():
    """借还API"""
    if request.method == 'GET':
        # 使用聚合管道获取租借记录和VCD信息
        pipeline = [
            {
                '$lookup': {
                    'from': 'vcds',
                    'localField': 'vcd_id',
                    'foreignField': '_id',
                    'as': 'vcd_info'
                }
            },
            {
                '$unwind': '$vcd_info'
            },
            {
                '$project': {
                    'vcd_id': 1,
                    'vcd_name': '$vcd_info.name',
                    'quantity': 1,
                    'daily_rate': 1,
                    'customer_name': 1,
                    'customer_phone': 1,
                    'rent_date': 1,
                    'return_date': 1,
                    'status': 1,
                    'action': 1,
                    'note': 1
                }
            },
            {
                '$sort': {'rent_date': -1}
            }
        ]
        
        rentals_list = list(rentals.aggregate(pipeline))
        for rental in rentals_list:
            rental['_id'] = str(rental['_id'])
            rental['vcd_id'] = str(rental['vcd_id'])
        return jsonify(rentals_list)
    
    elif request.method == 'POST':
        rental_data = request.json
        vcd_id = ObjectId(rental_data['vcd_id'])
        rental_data['vcd_id'] = vcd_id
        
        # 获取VCD信息
        vcd_info = vcds.find_one({'_id': vcd_id})
        if not vcd_info:
            return jsonify({'success': False, 'message': 'VCD不存在'})
        
        rental_data['vcd_name'] = vcd_info['name']
        
        if rental_data['action'] == 'rent':
            # 借出
            rental_data['rent_date'] = datetime.now()
            rental_data['return_date'] = None
            rental_data['status'] = 'rented'
            
            # 检查库存
            inv = inventory.find_one({'vcd_id': vcd_id})
            if not inv or inv['available_quantity'] < rental_data['quantity']:
                return jsonify({'success': False, 'message': '库存不足'})
            
            # 更新库存
            inventory.update_one(
                {'vcd_id': vcd_id},
                {
                    '$inc': {
                        'available_quantity': -rental_data['quantity'],
                        'rented_quantity': rental_data['quantity']
                    },
                    '$set': {'last_updated': datetime.now()}
                }
            )
            
        elif rental_data['action'] == 'return':
            # 归还 - 更新原有的借出记录而不是创建新记录
            rental_id = rental_data.get('rental_id')
            if not rental_id:
                return jsonify({'success': False, 'message': '缺少租借记录ID'})
            
            # 查找原始借出记录
            original_rental = rentals.find_one({'_id': ObjectId(rental_id)})
            if not original_rental:
                return jsonify({'success': False, 'message': '未找到对应的借出记录'})
            
            # 检查记录状态
            if original_rental.get('status') == 'returned':
                return jsonify({'success': False, 'message': '该记录已经归还'})
            
            # 更新借出记录的状态和归还时间
            rentals.update_one(
                {'_id': ObjectId(rental_id)},
                {
                    '$set': {
                        'return_date': datetime.now(),
                        'status': 'returned'
                    }
                }
            )
            
            # 更新库存
            inventory.update_one(
                {'vcd_id': vcd_id},
                {
                    '$inc': {
                        'available_quantity': rental_data['quantity'],
                        'rented_quantity': -rental_data['quantity']
                    },
                    '$set': {'last_updated': datetime.now()}
                }
            )
            
            return jsonify({'success': True})
        
        # 只有借出操作才创建新记录
        rentals.insert_one(rental_data)
        return jsonify({'success': True})

@app.route('/api/statistics/sales')
def api_sales_statistics():
    """销售统计API (存储过程功能)"""
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    if start_date and end_date:
        start_date = datetime.fromisoformat(start_date)
        # 将end_date设置为当天的23:59:59，确保包含当天所有记录
        end_date = datetime.fromisoformat(end_date).replace(hour=23, minute=59, second=59, microsecond=999999)
    else:
        # 默认统计最近30天
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
    
    # 聚合管道统计销售数据
    pipeline = [
        {
            '$match': {
                'sale_date': {
                    '$gte': start_date,
                    '$lte': end_date
                }
            }
        },
        {
            '$lookup': {
                'from': 'vcds',
                'localField': 'vcd_id',
                'foreignField': '_id',
                'as': 'vcd_info'
            }
        },
        {
            '$unwind': '$vcd_info'
        },
        {
            '$group': {
                '_id': '$vcd_id',
                'vcd_name': {'$first': '$vcd_info.name'},
                'vcd_type': {'$first': '$vcd_info.type'},
                'total_sold': {'$sum': '$quantity'},
                'total_revenue': {'$sum': {'$multiply': ['$quantity', '$unit_price']}}
            }
        },
        {
            '$sort': {'total_sold': -1}
        }
    ]
    
    result = list(sales.aggregate(pipeline))
    for item in result:
        item['_id'] = str(item['_id'])
    
    return jsonify(result)

@app.route('/api/statistics/rentals')
def api_rental_statistics():
    """借还统计API"""
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    if start_date and end_date:
        start_date = datetime.fromisoformat(start_date)
        # 将end_date设置为当天的23:59:59，确保包含当天所有记录
        end_date = datetime.fromisoformat(end_date).replace(hour=23, minute=59, second=59, microsecond=999999)
    else:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
    
    pipeline = [
        {
            '$match': {
                'rent_date': {
                    '$gte': start_date,
                    '$lte': end_date
                }
            }
        },
        {
            '$lookup': {
                'from': 'vcds',
                'localField': 'vcd_id',
                'foreignField': '_id',
                'as': 'vcd_info'
            }
        },
        {
            '$unwind': '$vcd_info'
        },
        {
            '$group': {
                '_id': '$vcd_id',
                'vcd_name': {'$first': '$vcd_info.name'},
                'vcd_type': {'$first': '$vcd_info.type'},
                'total_rented': {'$sum': '$quantity'},
                'total_rental_income': {'$sum': {'$multiply': ['$quantity', '$daily_rate']}}
            }
        },
        {
            '$sort': {'total_rented': -1}
        }
    ]
    
    result = list(rentals.aggregate(pipeline))
    for item in result:
        item['_id'] = str(item['_id'])
    
    return jsonify(result)

@app.route('/api/backup', methods=['POST'])
def api_backup():
    """数据备份API"""
    try:
        backup_data = {
            'backup_date': datetime.now(),
            'vcds': list(vcds.find()),
            'inventory': list(inventory.find()),
            'sales': list(sales.find()),
            'rentals': list(rentals.find()),
            'customers': list(customers.find())
        }
        
        # 将备份数据保存到文件
        filename = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        # 转换ObjectId为字符串以便JSON序列化
        def convert_objectid(obj):
            if isinstance(obj, ObjectId):
                return str(obj)
            elif isinstance(obj, dict):
                return {k: convert_objectid(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert_objectid(item) for item in obj]
            return obj
        
        backup_data = convert_objectid(backup_data)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(backup_data, f, ensure_ascii=False, indent=2, default=str)
        
        return jsonify({'success': True, 'filename': filename})
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

# =================================
# 新增实用功能 API
# =================================

@app.route('/api/search/advanced', methods=['POST'])
def api_advanced_search():
    """高级搜索API"""
    try:
        search_params = request.json
        
        # 构建搜索条件
        query = {}
        
        # 名称搜索
        if search_params.get('name'):
            query['name'] = {'$regex': search_params['name'], '$options': 'i'}
        
        # 类型过滤
        if search_params.get('type'):
            query['type'] = search_params['type']
        
        # 价格范围
        if search_params.get('min_price') or search_params.get('max_price'):
            price_query = {}
            if search_params.get('min_price'):
                price_query['$gte'] = float(search_params['min_price'])
            if search_params.get('max_price'):
                price_query['$lte'] = float(search_params['max_price'])
            query['price'] = price_query
        
        # 导演搜索
        if search_params.get('director'):
            query['director'] = {'$regex': search_params['director'], '$options': 'i'}
        
        # 发行年份
        if search_params.get('release_year'):
            query['release_year'] = int(search_params['release_year'])
        
        # 执行搜索
        results = list(vcds.find(query))
        
        # 获取库存信息
        for vcd in results:
            vcd['_id'] = str(vcd['_id'])
            vcd_inventory = inventory.find_one({'vcd_id': str(vcd['_id'])})
            if vcd_inventory:
                vcd['stock_status'] = {
                    'total_quantity': vcd_inventory.get('total_quantity', 0),
                    'available_quantity': vcd_inventory.get('available_quantity', 0),
                    'rented_quantity': vcd_inventory.get('rented_quantity', 0),
                    'status': 'available' if vcd_inventory.get('available_quantity', 0) > 5 else 
                             'low_stock' if vcd_inventory.get('available_quantity', 0) > 0 else 'out_of_stock'
                }
            else:
                vcd['stock_status'] = {
                    'total_quantity': 0,
                    'available_quantity': 0, 
                    'rented_quantity': 0,
                    'status': 'out_of_stock'
                }
        
        # 记录搜索日志
        log_operation('高级搜索', f"搜索条件: {search_params}, 结果数量: {len(results)}")
        
        return jsonify({'success': True, 'results': results, 'count': len(results)})
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/inventory/alerts')
def api_inventory_alerts():
    """库存预警API"""
    try:
        alerts = []
        
        # 获取所有库存记录
        inventory_records = list(inventory.find())
        
        for record in inventory_records:
            vcd_info = vcds.find_one({'_id': ObjectId(record['vcd_id'])})
            if not vcd_info:
                continue
                
            available = record.get('available_quantity', 0)
            total = record.get('total_quantity', 0)
            
            alert = {
                'vcd_id': str(record['vcd_id']),
                'vcd_name': vcd_info.get('name', '未知'),
                'vcd_type': vcd_info.get('type', '未知'),
                'available_quantity': available,
                'total_quantity': total,
                'alert_type': '',
                'alert_message': '',
                'priority': 0
            }
            
            # 缺货警报
            if available == 0:
                alert['alert_type'] = 'out_of_stock'
                alert['alert_message'] = '已售罄，需要补货'
                alert['priority'] = 3
                alerts.append(alert)
            # 低库存警报
            elif available <= 3:
                alert['alert_type'] = 'low_stock'
                alert['alert_message'] = f'库存不足，仅剩{available}件'
                alert['priority'] = 2
                alerts.append(alert)
            # 库存过多警报
            elif available > total * 0.8 and total > 20:
                alert['alert_type'] = 'overstocked'
                alert['alert_message'] = f'库存过多，可能滞销'
                alert['priority'] = 1
                alerts.append(alert)
        
        # 按优先级排序
        alerts.sort(key=lambda x: x['priority'], reverse=True)
        
        return jsonify({
            'success': True, 
            'alerts': alerts,
            'summary': {
                'total_alerts': len(alerts),
                'out_of_stock': len([a for a in alerts if a['alert_type'] == 'out_of_stock']),
                'low_stock': len([a for a in alerts if a['alert_type'] == 'low_stock']),
                'overstocked': len([a for a in alerts if a['alert_type'] == 'overstocked'])
            }
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/logs')
def api_operation_logs():
    """操作日志API"""
    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 50))
        skip = (page - 1) * limit
        
        # 获取日志记录
        logs = list(operation_logs.find().sort('timestamp', -1).skip(skip).limit(limit))
        total_logs = operation_logs.count_documents({})
        
        for log in logs:
            log['_id'] = str(log['_id'])
            log['timestamp'] = log['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
        
        return jsonify({
            'success': True,
            'logs': logs,
            'pagination': {
                'current_page': page,
                'total_pages': (total_logs + limit - 1) // limit,
                'total_records': total_logs,
                'has_next': skip + limit < total_logs,
                'has_prev': page > 1
            }
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/batch/price-update', methods=['POST'])
def api_batch_price_update():
    """批量价格更新API"""
    try:
        data = request.json
        update_type = data.get('update_type')  # 'percentage', 'fixed', 'specific'
        value = data.get('value')
        vcd_ids = data.get('vcd_ids', [])
        
        if not update_type or value is None:
            return jsonify({'success': False, 'message': '缺少必要参数'})
        
        updated_count = 0
        
        if update_type == 'percentage':
            # 按百分比调整
            multiplier = 1 + (float(value) / 100)
            for vcd_id in vcd_ids:
                result = vcds.update_one(
                    {'_id': ObjectId(vcd_id)},
                    {'$mul': {'price': multiplier}}
                )
                if result.modified_count > 0:
                    updated_count += 1
                    
        elif update_type == 'fixed':
            # 固定金额调整
            for vcd_id in vcd_ids:
                result = vcds.update_one(
                    {'_id': ObjectId(vcd_id)},
                    {'$inc': {'price': float(value)}}
                )
                if result.modified_count > 0:
                    updated_count += 1
                    
        elif update_type == 'specific':
            # 设置为特定价格
            for vcd_id in vcd_ids:
                result = vcds.update_one(
                    {'_id': ObjectId(vcd_id)},
                    {'$set': {'price': float(value)}}
                )
                if result.modified_count > 0:
                    updated_count += 1
        
        # 记录操作日志
        log_operation('批量价格更新', f"更新类型: {update_type}, 调整值: {value}, 影响VCD数量: {updated_count}")
        
        return jsonify({
            'success': True,
            'message': f'成功更新了{updated_count}个VCD的价格',
            'updated_count': updated_count
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/recommendations')
def api_recommendations():
    """VCD推荐API"""
    try:
        # 热销推荐 - 基于销售数据
        hot_sales = list(sales.aggregate([
            {
                '$group': {
                    '_id': '$vcd_id',
                    'total_sold': {'$sum': '$quantity'},
                    'total_revenue': {'$sum': {'$multiply': ['$quantity', '$unit_price']}}
                }
            },
            {
                '$sort': {'total_sold': -1}
            },
            {
                '$limit': 5
            }
        ]))
        
        hot_recommendations = []
        for item in hot_sales:
            vcd_info = vcds.find_one({'_id': ObjectId(item['_id'])})
            if vcd_info:
                hot_recommendations.append({
                    'vcd_id': str(item['_id']),
                    'name': vcd_info['name'],
                    'type': vcd_info['type'],
                    'price': vcd_info['price'],
                    'total_sold': item['total_sold'],
                    'reason': f'热销商品，已售出{item["total_sold"]}件'
                })
        
        # 高利润推荐
        high_profit = list(vcds.find().sort('price', -1).limit(5))
        profit_recommendations = []
        for vcd in high_profit:
            # 检查库存
            stock_info = inventory.find_one({'vcd_id': str(vcd['_id'])})
            if stock_info and stock_info.get('available_quantity', 0) > 0:
                profit_recommendations.append({
                    'vcd_id': str(vcd['_id']),
                    'name': vcd['name'],
                    'type': vcd['type'],
                    'price': vcd['price'],
                    'available_quantity': stock_info.get('available_quantity', 0),
                    'reason': f'高价值商品，单价¥{vcd["price"]}'
                })
        
        # 滞销提醒 - 库存多但销售少的商品
        slow_moving = []
        all_inventory = list(inventory.find())
        for stock in all_inventory:
            if stock.get('available_quantity', 0) > 10:  # 库存大于10的商品
                # 检查最近销售情况
                recent_sales = sales.count_documents({
                    'vcd_id': stock['vcd_id'],
                    'sale_date': {'$gte': datetime.now() - timedelta(days=30)}
                })
                
                if recent_sales == 0:  # 30天内无销售
                    vcd_info = vcds.find_one({'_id': ObjectId(stock['vcd_id'])})
                    if vcd_info:
                        slow_moving.append({
                            'vcd_id': str(stock['vcd_id']),
                            'name': vcd_info['name'],
                            'type': vcd_info['type'],
                            'price': vcd_info['price'],
                            'available_quantity': stock.get('available_quantity', 0),
                            'reason': '滞销商品，建议促销'
                        })
        
        return jsonify({
            'success': True,
            'recommendations': {
                'hot_sales': hot_recommendations,
                'high_profit': profit_recommendations[:3],
                'slow_moving': slow_moving[:5]
            }
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/export/enhanced', methods=['POST'])
def api_enhanced_export():
    """增强的数据导出API"""
    try:
        export_type = request.json.get('export_type')
        date_range = request.json.get('date_range', {})
        
        export_data = {}
        
        if export_type == 'complete_report':
            # 完整报表
            export_data = {
                'vcds': list(vcds.find()),
                'inventory': list(inventory.find()),
                'sales': list(sales.find()),
                'rentals': list(rentals.find()),
                'generated_at': datetime.now().isoformat()
            }
            
        elif export_type == 'sales_analysis':
            # 销售分析报表
            start_date = datetime.fromisoformat(date_range.get('start_date', datetime.now().strftime('%Y-%m-%d')))
            end_date = datetime.fromisoformat(date_range.get('end_date', datetime.now().strftime('%Y-%m-%d')))
            
            sales_data = list(sales.aggregate([
                {
                    '$match': {
                        'sale_date': {'$gte': start_date, '$lte': end_date}
                    }
                },
                {
                    '$lookup': {
                        'from': 'vcds',
                        'localField': 'vcd_id',
                        'foreignField': '_id',
                        'as': 'vcd_info'
                    }
                },
                {
                    '$unwind': '$vcd_info'
                }
            ]))
            
            export_data = {
                'sales_analysis': sales_data,
                'date_range': {'start': start_date.isoformat(), 'end': end_date.isoformat()},
                'generated_at': datetime.now().isoformat()
            }
            
        elif export_type == 'inventory_report':
            # 库存报表
            inventory_data = list(inventory.aggregate([
                {
                    '$lookup': {
                        'from': 'vcds',
                        'localField': 'vcd_id',
                        'foreignField': '_id',
                        'as': 'vcd_info'
                    }
                },
                {
                    '$unwind': '$vcd_info'
                }
            ]))
            
            export_data = {
                'inventory_report': inventory_data,
                'generated_at': datetime.now().isoformat()
            }
        
        # 转换ObjectId为字符串
        def convert_objectid(obj):
            if isinstance(obj, ObjectId):
                return str(obj)
            elif isinstance(obj, dict):
                return {k: convert_objectid(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert_objectid(item) for item in obj]
            return obj
        
        export_data = convert_objectid(export_data)
        
        # 记录导出日志
        log_operation('数据导出', f"导出类型: {export_type}")
        
        return jsonify({
            'success': True,
            'data': export_data,
            'filename': f'{export_type}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

# 辅助函数：记录操作日志
def log_operation(operation_type, description, user_id='system'):
    """记录操作日志"""
    try:
        log_entry = {
            'operation_type': operation_type,
            'description': description,
            'user_id': user_id,
            'timestamp': datetime.now(),
            'ip_address': request.remote_addr if request else 'localhost'
        }
        operation_logs.insert_one(log_entry)
    except Exception as e:
        print(f"日志记录失败: {e}")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 