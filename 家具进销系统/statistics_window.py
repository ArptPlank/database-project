"""
统计查询窗口
"""
import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
from gui_utils import GUIUtils
from models import Statistics, Furniture

class StatisticsWindow:
    """统计查询窗口"""
    
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("进销存统计查询")
        self.window.grab_set()
        GUIUtils.center_window(self.window, 1200, 700)
        
        self.statistics = Statistics()
        self.furniture = Furniture()
        self.setup_ui()
    
    def setup_ui(self):
        """设置用户界面"""
        main_frame = ttk.Frame(self.window)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.create_query_area(main_frame)
        self.create_result_area(main_frame)
    
    def create_query_area(self, parent):
        """创建查询区域"""
        query_frame = ttk.LabelFrame(parent, text="查询条件", padding=10)
        query_frame.pack(fill="x", pady=(0, 10))
        
        query_frame.grid_columnconfigure(1, weight=1)
        query_frame.grid_columnconfigure(3, weight=1)
        
        # 日期范围
        ttk.Label(query_frame, text="开始日期:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.start_date_entry = ttk.Entry(query_frame)
        self.start_date_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        # 默认为一个月前
        default_start = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        self.start_date_entry.insert(0, default_start)
        
        ttk.Label(query_frame, text="结束日期:").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.end_date_entry = ttk.Entry(query_frame)
        self.end_date_entry.grid(row=0, column=3, sticky="ew", padx=5, pady=5)
        # 默认为今天
        default_end = datetime.now().strftime("%Y-%m-%d")
        self.end_date_entry.insert(0, default_end)
        
        # 按钮
        button_frame = ttk.Frame(query_frame)
        button_frame.grid(row=1, column=0, columnspan=4, pady=10)
        
        ttk.Button(button_frame, text="查询统计", command=self.query_statistics).pack(side="left", padx=5)
        ttk.Button(button_frame, text="导出数据", command=self.export_data).pack(side="left", padx=5)
        ttk.Button(button_frame, text="清空结果", command=self.clear_results).pack(side="left", padx=5)
    
    def create_result_area(self, parent):
        """创建结果显示区域"""
        # 创建选项卡
        notebook = ttk.Notebook(parent)
        notebook.pack(fill="both", expand=True)
        
        # 详细统计选项卡
        detail_frame = ttk.Frame(notebook)
        notebook.add(detail_frame, text="详细统计")
        
        # 汇总统计选项卡
        summary_frame = ttk.Frame(notebook)
        notebook.add(summary_frame, text="汇总统计")
        
        self.create_detail_tab(detail_frame)
        self.create_summary_tab(summary_frame)
    
    def create_detail_tab(self, parent):
        """创建详细统计选项卡"""
        columns = ("furniture_code", "furniture_name", "type_code", "stock_in_quantity", 
                  "sales_quantity", "net_change", "unit_price", "stock_in_amount", "sales_amount")
        headings = ("家具编码", "家具名称", "类型编码", "入库数量", 
                   "销售数量", "净变化", "单价", "入库金额", "销售金额")
        
        self.detail_tree = GUIUtils.create_treeview(parent, columns, headings)
    
    def create_summary_tab(self, parent):
        """创建汇总统计选项卡"""
        # 统计信息显示
        info_frame = ttk.LabelFrame(parent, text="统计汇总", padding=10)
        info_frame.pack(fill="x", pady=(0, 10))
        
        # 创建汇总标签
        self.total_stock_in_label = ttk.Label(info_frame, text="总入库数量: 0")
        self.total_stock_in_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)
        
        self.total_sales_label = ttk.Label(info_frame, text="总销售数量: 0")
        self.total_sales_label.grid(row=0, column=1, sticky="w", padx=10, pady=5)
        
        self.total_stock_in_amount_label = ttk.Label(info_frame, text="总入库金额: ¥0.00")
        self.total_stock_in_amount_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)
        
        self.total_sales_amount_label = ttk.Label(info_frame, text="总销售金额: ¥0.00")
        self.total_sales_amount_label.grid(row=1, column=1, sticky="w", padx=10, pady=5)
        
        self.profit_label = ttk.Label(info_frame, text="毛利润: ¥0.00")
        self.profit_label.grid(row=2, column=0, sticky="w", padx=10, pady=5)
        
        # 按类型统计
        type_frame = ttk.LabelFrame(parent, text="按类型统计", padding=10)
        type_frame.pack(fill="both", expand=True)
        
        type_columns = ("type_code", "type_name", "stock_in_quantity", "sales_quantity", 
                       "stock_in_amount", "sales_amount")
        type_headings = ("类型编码", "类型名称", "入库数量", "销售数量", "入库金额", "销售金额")
        
        self.type_tree = GUIUtils.create_treeview(type_frame, type_columns, type_headings)
    
    def query_statistics(self):
        """查询统计信息"""
        try:
            # 验证日期格式
            start_date_str = self.start_date_entry.get().strip()
            end_date_str = self.end_date_entry.get().strip()
            
            if not start_date_str or not end_date_str:
                GUIUtils.show_error("请输入开始日期和结束日期")
                return
            
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
            
            if start_date > end_date:
                GUIUtils.show_error("开始日期不能晚于结束日期")
                return
            
            # 设置结束日期为当天的23:59:59
            end_date = end_date.replace(hour=23, minute=59, second=59)
            
            # 获取统计数据
            stats_data = self.statistics.get_inventory_statistics(start_date, end_date)
            
            # 获取家具信息用于显示
            furnitures = {f['furniture_code']: f for f in self.furniture.get_all_furniture()}
            
            # 清空现有数据
            self.clear_results()
            
            # 统计汇总变量
            total_stock_in_quantity = 0
            total_sales_quantity = 0
            total_stock_in_amount = 0
            total_sales_amount = 0
            type_stats = {}
            
            # 填充详细统计
            for stat in stats_data:
                furniture_code = stat['furniture_code']
                furniture_info = furnitures.get(furniture_code, {})
                
                furniture_name = furniture_info.get('name', '')
                type_code = furniture_info.get('type_code', '')
                unit_price = furniture_info.get('unit_price', 0)
                
                stock_in_quantity = stat['stock_in_quantity']
                sales_quantity = stat['sales_quantity']
                net_change = stock_in_quantity - sales_quantity
                
                stock_in_amount = stock_in_quantity * unit_price
                sales_amount = sales_quantity * unit_price
                
                # 累计汇总数据
                total_stock_in_quantity += stock_in_quantity
                total_sales_quantity += sales_quantity
                total_stock_in_amount += stock_in_amount
                total_sales_amount += sales_amount
                
                # 按类型统计
                if type_code not in type_stats:
                    type_stats[type_code] = {
                        'stock_in_quantity': 0,
                        'sales_quantity': 0,
                        'stock_in_amount': 0,
                        'sales_amount': 0
                    }
                
                type_stats[type_code]['stock_in_quantity'] += stock_in_quantity
                type_stats[type_code]['sales_quantity'] += sales_quantity
                type_stats[type_code]['stock_in_amount'] += stock_in_amount
                type_stats[type_code]['sales_amount'] += sales_amount
                
                # 插入详细统计数据
                values = (
                    furniture_code,
                    furniture_name,
                    type_code,
                    stock_in_quantity,
                    sales_quantity,
                    net_change,
                    GUIUtils.format_currency(unit_price),
                    GUIUtils.format_currency(stock_in_amount),
                    GUIUtils.format_currency(sales_amount)
                )
                self.detail_tree.insert("", "end", values=values)
            
            # 更新汇总信息
            self.update_summary_info(total_stock_in_quantity, total_sales_quantity,
                                   total_stock_in_amount, total_sales_amount)
            
            # 填充按类型统计
            self.fill_type_statistics(type_stats)
            
            GUIUtils.show_success(f"查询完成，共找到 {len(stats_data)} 条记录")
            
        except ValueError as e:
            GUIUtils.show_error(f"日期格式错误，请使用 YYYY-MM-DD 格式: {e}")
        except Exception as e:
            GUIUtils.show_error(f"查询失败: {e}")
    
    def update_summary_info(self, stock_in_qty, sales_qty, stock_in_amt, sales_amt):
        """更新汇总信息"""
        self.total_stock_in_label.config(text=f"总入库数量: {stock_in_qty}")
        self.total_sales_label.config(text=f"总销售数量: {sales_qty}")
        self.total_stock_in_amount_label.config(text=f"总入库金额: {GUIUtils.format_currency(stock_in_amt)}")
        self.total_sales_amount_label.config(text=f"总销售金额: {GUIUtils.format_currency(sales_amt)}")
        
        profit = sales_amt - stock_in_amt
        self.profit_label.config(text=f"毛利润: {GUIUtils.format_currency(profit)}")
    
    def fill_type_statistics(self, type_stats):
        """填充按类型统计"""
        # 获取家具类型信息
        from models import FurnitureType
        furniture_type = FurnitureType()
        types = {t['type_code']: t for t in furniture_type.get_all_types()}
        
        for type_code, stats in type_stats.items():
            type_name = types.get(type_code, {}).get('type_name', '')
            
            values = (
                type_code,
                type_name,
                stats['stock_in_quantity'],
                stats['sales_quantity'],
                GUIUtils.format_currency(stats['stock_in_amount']),
                GUIUtils.format_currency(stats['sales_amount'])
            )
            self.type_tree.insert("", "end", values=values)
    
    def clear_results(self):
        """清空结果"""
        # 清空详细统计
        for item in self.detail_tree.get_children():
            self.detail_tree.delete(item)
        
        # 清空按类型统计
        for item in self.type_tree.get_children():
            self.type_tree.delete(item)
        
        # 重置汇总信息
        self.total_stock_in_label.config(text="总入库数量: 0")
        self.total_sales_label.config(text="总销售数量: 0")
        self.total_stock_in_amount_label.config(text="总入库金额: ¥0.00")
        self.total_sales_amount_label.config(text="总销售金额: ¥0.00")
        self.profit_label.config(text="毛利润: ¥0.00")
    
    def export_data(self):
        """导出数据"""
        try:
            from tkinter import filedialog
            
            # 选择保存文件
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                title="导出统计数据"
            )
            
            if filename:
                # 获取详细统计数据
                data = []
                for child in self.detail_tree.get_children():
                    values = self.detail_tree.item(child)['values']
                    data.append(values)
                
                if not data:
                    GUIUtils.show_warning("没有数据可以导出")
                    return
                
                # 写入CSV文件
                import csv
                with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
                    writer = csv.writer(csvfile)
                    
                    # 写入标题
                    headers = ["家具编码", "家具名称", "类型编码", "入库数量", 
                              "销售数量", "净变化", "单价", "入库金额", "销售金额"]
                    writer.writerow(headers)
                    
                    # 写入数据
                    writer.writerows(data)
                
                GUIUtils.show_success(f"数据已导出到: {filename}")
                
        except Exception as e:
            GUIUtils.show_error(f"导出失败: {e}") 