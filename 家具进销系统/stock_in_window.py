"""
入库管理窗口
"""
import tkinter as tk
from tkinter import ttk
from datetime import datetime
from gui_utils import GUIUtils
from models import StockIn, Furniture, Supplier

class StockInWindow:
    """入库管理窗口"""
    
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("家具入库管理")
        self.window.grab_set()
        GUIUtils.center_window(self.window, 1400, 800)
        
        self.stock_in = StockIn()
        self.furniture = Furniture()
        self.supplier = Supplier()
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
        input_frame = ttk.LabelFrame(parent, text="入库信息", padding=10)
        input_frame.pack(fill="x", pady=(0, 10))
        
        input_frame.grid_columnconfigure(1, weight=1)
        input_frame.grid_columnconfigure(3, weight=1)
        
        # 家具下拉框
        furnitures = self.furniture.get_all_furniture()
        furniture_values = [f"{f['furniture_code']}-{f['name']}" for f in furnitures]
        self.furniture_combobox = GUIUtils.create_labeled_combobox(
            input_frame, "家具:", furniture_values, 0, 0)
        self.furniture_combobox.bind("<<ComboboxSelected>>", self.on_furniture_selected)
        
        # 供应商下拉框
        suppliers = self.supplier.get_all_suppliers()
        supplier_values = [f"{s['supplier_code']}-{s['name']}" for s in suppliers]
        self.supplier_combobox = GUIUtils.create_labeled_combobox(
            input_frame, "供应商:", supplier_values, 0, 2)
        
        self.quantity_entry = GUIUtils.create_labeled_entry(
            input_frame, "入库数量:", 1, 0)
        self.quantity_entry.bind("<KeyRelease>", self.calculate_total)
        
        self.unit_price_entry = GUIUtils.create_labeled_entry(
            input_frame, "单价:", 1, 2)
        self.unit_price_entry.bind("<KeyRelease>", self.calculate_total)
        
        self.total_amount_entry = GUIUtils.create_labeled_entry(
            input_frame, "总金额:", 2, 0)
        self.total_amount_entry.config(state="readonly")
        
        # 入库日期
        ttk.Label(input_frame, text="入库日期:").grid(row=2, column=2, sticky="w", padx=5, pady=5)
        self.date_entry = ttk.Entry(input_frame)
        self.date_entry.grid(row=2, column=3, sticky="ew", padx=5, pady=5)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    def create_button_area(self, parent):
        """创建按钮区域"""
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Button(button_frame, text="入库", command=self.add_stock_in).pack(side="left", padx=5)
        ttk.Button(button_frame, text="清空", command=self.clear_inputs).pack(side="left", padx=5)
        ttk.Button(button_frame, text="刷新", command=self.load_data).pack(side="left", padx=5)
    
    def create_list_area(self, parent):
        """创建列表区域"""
        columns = ("record_id", "furniture_code", "furniture_name", "supplier_code", 
                  "supplier_name", "quantity", "unit_price", "total_amount", "record_date")
        headings = ("记录ID", "家具编码", "家具名称", "供应商编码", 
                   "供应商名称", "数量", "单价", "总金额", "入库日期")
        
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
    
    def add_stock_in(self):
        """添加入库记录"""
        if not self.furniture_combobox.get():
            GUIUtils.show_error("请选择家具")
            return
        
        if not self.supplier_combobox.get():
            GUIUtils.show_error("请选择供应商")
            return
        
        if not GUIUtils.validate_not_empty(
            [self.quantity_entry, self.unit_price_entry],
            ["入库数量", "单价"]):
            return
        
        if not GUIUtils.validate_number(self.quantity_entry, "入库数量"):
            return
        
        if not GUIUtils.validate_number(self.unit_price_entry, "单价"):
            return
        
        try:
            furniture_code = self.furniture_combobox.get().split('-')[0]
            supplier_code = self.supplier_combobox.get().split('-')[0]
            quantity = int(self.quantity_entry.get())
            unit_price = float(self.unit_price_entry.get())
            total_amount = float(self.total_amount_entry.get())
            record_date = datetime.strptime(self.date_entry.get(), "%Y-%m-%d %H:%M:%S")
            
            if quantity <= 0:
                GUIUtils.show_error("入库数量必须大于0")
                return
            
            self.stock_in.create_stock_in(furniture_code, supplier_code, quantity, 
                                        unit_price, total_amount, record_date)
            
            GUIUtils.show_success("入库成功，库存已自动更新")
            
            self.load_data()
            self.clear_inputs()
            
        except ValueError as e:
            GUIUtils.show_error(f"日期格式错误: {e}")
        except Exception as e:
            GUIUtils.show_error(f"入库失败: {e}")
    
    def clear_inputs(self):
        """清空输入框"""
        self.furniture_combobox.set("")
        self.supplier_combobox.set("")
        self.quantity_entry.delete(0, tk.END)
        self.unit_price_entry.delete(0, tk.END)
        self.total_amount_entry.config(state="normal")
        self.total_amount_entry.delete(0, tk.END)
        self.total_amount_entry.config(state="readonly")
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    def load_data(self):
        """加载数据"""
        try:
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # 获取入库记录
            stock_ins = self.stock_in.find_all()
            
            # 获取家具和供应商信息用于显示
            furnitures = {f['furniture_code']: f for f in self.furniture.get_all_furniture()}
            suppliers = {s['supplier_code']: s for s in self.supplier.get_all_suppliers()}
            
            for record in stock_ins:
                furniture_code = record.get("furniture_code", "")
                supplier_code = record.get("supplier_code", "")
                
                furniture_name = furnitures.get(furniture_code, {}).get("name", "")
                supplier_name = suppliers.get(supplier_code, {}).get("name", "")
                
                values = (
                    record.get("record_id", ""),
                    furniture_code,
                    furniture_name,
                    supplier_code,
                    supplier_name,
                    record.get("quantity", 0),
                    GUIUtils.format_currency(record.get("unit_price", 0)),
                    GUIUtils.format_currency(record.get("total_amount", 0)),
                    GUIUtils.format_datetime(record.get("record_date", ""))
                )
                self.tree.insert("", "end", values=values)
                
        except Exception as e:
            GUIUtils.show_error(f"加载数据失败: {e}") 