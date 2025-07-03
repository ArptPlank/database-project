"""
销售管理窗口
"""
import tkinter as tk
from tkinter import ttk
from datetime import datetime
from gui_utils import GUIUtils
from models import Sales, Furniture, Customer

class SalesWindow:
    """销售管理窗口"""
    
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("家具销售管理")
        self.window.grab_set()
        GUIUtils.center_window(self.window, 1400, 800)
        
        self.sales = Sales()
        self.furniture = Furniture()
        self.customer = Customer()
        self.setup_ui()
        self.load_data()
    
    def setup_ui(self):
        """设置用户界面"""
        main_frame = ttk.Frame(self.window)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.create_input_area(main_frame)
        self.create_button_area(main_frame)
        self.create_list_area(main_frame)
    
    def create_input_area(self, parent):
        """创建输入区域"""
        input_frame = ttk.LabelFrame(parent, text="销售信息", padding=10)
        input_frame.pack(fill="x", pady=(0, 10))
        
        input_frame.grid_columnconfigure(1, weight=1)
        input_frame.grid_columnconfigure(3, weight=1)
        
        # 家具下拉框
        furnitures = self.furniture.get_all_furniture()
        furniture_values = [f"{f['furniture_code']}-{f['name']}(库存:{f['stock_quantity']})" for f in furnitures]
        self.furniture_combobox = GUIUtils.create_labeled_combobox(
            input_frame, "家具:", furniture_values, 0, 0)
        self.furniture_combobox.bind("<<ComboboxSelected>>", self.on_furniture_selected)
        
        # 客户下拉框
        customers = self.customer.get_all_customers()
        customer_values = [f"{c['customer_code']}-{c['name']}" for c in customers]
        self.customer_combobox = GUIUtils.create_labeled_combobox(
            input_frame, "客户:", customer_values, 0, 2)
        
        self.quantity_entry = GUIUtils.create_labeled_entry(
            input_frame, "销售数量:", 1, 0)
        self.quantity_entry.bind("<KeyRelease>", self.calculate_total)
        
        self.unit_price_entry = GUIUtils.create_labeled_entry(
            input_frame, "单价:", 1, 2)
        self.unit_price_entry.bind("<KeyRelease>", self.calculate_total)
        
        self.total_amount_entry = GUIUtils.create_labeled_entry(
            input_frame, "总金额:", 2, 0)
        self.total_amount_entry.config(state="readonly")
        
        # 销售日期
        ttk.Label(input_frame, text="销售日期:").grid(row=2, column=2, sticky="w", padx=5, pady=5)
        self.date_entry = ttk.Entry(input_frame)
        self.date_entry.grid(row=2, column=3, sticky="ew", padx=5, pady=5)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        
        # 库存显示
        ttk.Label(input_frame, text="当前库存:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.stock_label = ttk.Label(input_frame, text="0", foreground="red")
        self.stock_label.grid(row=3, column=1, sticky="w", padx=5, pady=5)
    
    def create_button_area(self, parent):
        """创建按钮区域"""
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Button(button_frame, text="销售", command=self.add_sale).pack(side="left", padx=5)
        ttk.Button(button_frame, text="清空", command=self.clear_inputs).pack(side="left", padx=5)
        ttk.Button(button_frame, text="刷新", command=self.load_data).pack(side="left", padx=5)
    
    def create_list_area(self, parent):
        """创建列表区域"""
        columns = ("sale_id", "furniture_code", "furniture_name", "customer_code", 
                  "customer_name", "quantity", "unit_price", "total_amount", "sale_date", "payment_status")
        headings = ("销售ID", "家具编码", "家具名称", "客户编码", 
                   "客户名称", "数量", "单价", "总金额", "销售日期", "付款状态")
        
        self.tree = GUIUtils.create_treeview(parent, columns, headings)
    
    def on_furniture_selected(self, event):
        """家具选择事件"""
        if self.furniture_combobox.get():
            furniture_code = self.furniture_combobox.get().split('-')[0]
            furniture_info = self.furniture.get_by_code(furniture_code)
            if furniture_info:
                # 自动填充单价
                self.unit_price_entry.delete(0, tk.END)
                self.unit_price_entry.insert(0, str(furniture_info['unit_price']))
                
                # 显示库存
                stock_quantity = furniture_info['stock_quantity']
                self.stock_label.config(text=str(stock_quantity))
                
                if stock_quantity <= 0:
                    self.stock_label.config(foreground="red")
                elif stock_quantity <= 10:
                    self.stock_label.config(foreground="orange")
                else:
                    self.stock_label.config(foreground="green")
                
                self.calculate_total()
    
    def calculate_total(self, event=None):
        """计算总金额"""
        try:
            quantity = float(self.quantity_entry.get() or 0)
            unit_price = float(self.unit_price_entry.get() or 0)
            total = quantity * unit_price
            
            self.total_amount_entry.config(state="normal")
            self.total_amount_entry.delete(0, tk.END)
            self.total_amount_entry.insert(0, f"{total:.2f}")
            self.total_amount_entry.config(state="readonly")
        except ValueError:
            pass
    
    def add_sale(self):
        """添加销售记录"""
        if not self.furniture_combobox.get():
            GUIUtils.show_error("请选择家具")
            return
        
        if not self.customer_combobox.get():
            GUIUtils.show_error("请选择客户")
            return
        
        if not GUIUtils.validate_not_empty(
            [self.quantity_entry, self.unit_price_entry],
            ["销售数量", "单价"]):
            return
        
        if not GUIUtils.validate_number(self.quantity_entry, "销售数量"):
            return
        
        if not GUIUtils.validate_number(self.unit_price_entry, "单价"):
            return
        
        try:
            furniture_code = self.furniture_combobox.get().split('-')[0]
            customer_code = self.customer_combobox.get().split('-')[0]
            quantity = int(self.quantity_entry.get())
            unit_price = float(self.unit_price_entry.get())
            total_amount = float(self.total_amount_entry.get())
            sale_date = datetime.strptime(self.date_entry.get(), "%Y-%m-%d %H:%M:%S")
            
            if quantity <= 0:
                GUIUtils.show_error("销售数量必须大于0")
                return
            
            # 检查库存
            furniture_info = self.furniture.get_by_code(furniture_code)
            if not furniture_info:
                GUIUtils.show_error("家具不存在")
                return
            
            if furniture_info['stock_quantity'] < quantity:
                GUIUtils.show_error(f"库存不足！当前库存：{furniture_info['stock_quantity']}")
                return
            
            self.sales.create_sale(furniture_code, customer_code, quantity, 
                                 unit_price, total_amount, sale_date)
            
            GUIUtils.show_success("销售成功，库存已自动更新")
            
            self.load_data()
            self.clear_inputs()
            
        except ValueError as e:
            if "库存不足" in str(e):
                GUIUtils.show_error(str(e))
            else:
                GUIUtils.show_error(f"日期格式错误: {e}")
        except Exception as e:
            GUIUtils.show_error(f"销售失败: {e}")
    
    def clear_inputs(self):
        """清空输入框"""
        self.furniture_combobox.set("")
        self.customer_combobox.set("")
        self.quantity_entry.delete(0, tk.END)
        self.unit_price_entry.delete(0, tk.END)
        self.total_amount_entry.config(state="normal")
        self.total_amount_entry.delete(0, tk.END)
        self.total_amount_entry.config(state="readonly")
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.stock_label.config(text="0", foreground="red")
    
    def load_data(self):
        """加载数据"""
        try:
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # 获取销售记录
            sales_records = self.sales.find_all()
            
            # 获取家具和客户信息用于显示
            furnitures = {f['furniture_code']: f for f in self.furniture.get_all_furniture()}
            customers = {c['customer_code']: c for c in self.customer.get_all_customers()}
            
            for record in sales_records:
                furniture_code = record.get("furniture_code", "")
                customer_code = record.get("customer_code", "")
                
                furniture_name = furnitures.get(furniture_code, {}).get("name", "")
                customer_name = customers.get(customer_code, {}).get("name", "")
                
                values = (
                    record.get("sale_id", ""),
                    furniture_code,
                    furniture_name,
                    customer_code,
                    customer_name,
                    record.get("quantity", 0),
                    GUIUtils.format_currency(record.get("unit_price", 0)),
                    GUIUtils.format_currency(record.get("total_amount", 0)),
                    GUIUtils.format_datetime(record.get("sale_date", "")),
                    record.get("payment_status", "未收款")
                )
                self.tree.insert("", "end", values=values)
                
        except Exception as e:
            GUIUtils.show_error(f"加载数据失败: {e}") 