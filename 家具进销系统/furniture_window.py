"""
家具信息管理窗口
"""
import tkinter as tk
from tkinter import ttk
from gui_utils import GUIUtils
from models import Furniture, FurnitureType

class FurnitureWindow:
    """家具信息管理窗口"""
    
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("家具信息管理")
        self.window.grab_set()
        GUIUtils.center_window(self.window, 1200, 800)
        
        self.furniture = Furniture()
        self.furniture_type = FurnitureType()
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
        input_frame = ttk.LabelFrame(parent, text="家具信息", padding=10)
        input_frame.pack(fill="x", pady=(0, 10))
        
        input_frame.grid_columnconfigure(1, weight=1)
        input_frame.grid_columnconfigure(3, weight=1)
        
        self.furniture_code_entry = GUIUtils.create_labeled_entry(
            input_frame, "家具编码:", 0, 0)
        self.name_entry = GUIUtils.create_labeled_entry(
            input_frame, "家具名称:", 0, 2)
        
        # 家具类型下拉框
        types = self.furniture_type.get_all_types()
        type_values = [f"{t['type_code']}-{t['type_name']}" for t in types]
        self.type_combobox = GUIUtils.create_labeled_combobox(
            input_frame, "家具类型:", type_values, 1, 0)
        
        self.specification_entry = GUIUtils.create_labeled_entry(
            input_frame, "规格:", 1, 2)
        self.unit_price_entry = GUIUtils.create_labeled_entry(
            input_frame, "单价:", 2, 0)
        self.stock_quantity_entry = GUIUtils.create_labeled_entry(
            input_frame, "库存数量:", 2, 2)
    
    def create_button_area(self, parent):
        """创建按钮区域"""
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Button(button_frame, text="添加", command=self.add_furniture).pack(side="left", padx=5)
        ttk.Button(button_frame, text="修改", command=self.update_furniture).pack(side="left", padx=5)
        ttk.Button(button_frame, text="删除", command=self.delete_furniture).pack(side="left", padx=5)
        ttk.Button(button_frame, text="清空", command=self.clear_inputs).pack(side="left", padx=5)
        ttk.Button(button_frame, text="刷新", command=self.load_data).pack(side="left", padx=5)
    
    def create_list_area(self, parent):
        """创建列表区域"""
        columns = ("furniture_code", "name", "type_code", "specification", "unit_price", "stock_quantity", "created_at")
        headings = ("家具编码", "家具名称", "类型编码", "规格", "单价", "库存数量", "创建时间")
        
        self.tree = GUIUtils.create_treeview(parent, columns, headings)
        self.tree.bind("<<TreeviewSelect>>", self.on_item_select)
    
    def add_furniture(self):
        """添加家具"""
        if not GUIUtils.validate_not_empty(
            [self.furniture_code_entry, self.name_entry, self.specification_entry, self.unit_price_entry],
            ["家具编码", "家具名称", "规格", "单价"]):
            return
        
        if not self.type_combobox.get():
            GUIUtils.show_error("请选择家具类型")
            return
        
        if not GUIUtils.validate_number(self.unit_price_entry, "单价"):
            return
        
        try:
            furniture_code = self.furniture_code_entry.get().strip()
            name = self.name_entry.get().strip()
            type_code = self.type_combobox.get().split('-')[0]
            specification = self.specification_entry.get().strip()
            unit_price = float(self.unit_price_entry.get())
            stock_quantity = int(self.stock_quantity_entry.get() or 0)
            
            if self.furniture.find_one({"furniture_code": furniture_code}):
                GUIUtils.show_error("家具编码已存在")
                return
            
            self.furniture.create_furniture(furniture_code, name, type_code, specification, unit_price, stock_quantity)
            GUIUtils.show_success("家具信息添加成功")
            
            self.load_data()
            self.clear_inputs()
            
        except Exception as e:
            GUIUtils.show_error(f"添加失败: {e}")
    
    def update_furniture(self):
        """修改家具"""
        selected_item = self.tree.selection()
        if not selected_item:
            GUIUtils.show_warning("请选择要修改的家具")
            return
        
        if not GUIUtils.validate_not_empty(
            [self.furniture_code_entry, self.name_entry, self.specification_entry, self.unit_price_entry],
            ["家具编码", "家具名称", "规格", "单价"]):
            return
        
        if not self.type_combobox.get():
            GUIUtils.show_error("请选择家具类型")
            return
        
        if not GUIUtils.validate_number(self.unit_price_entry, "单价"):
            return
        
        try:
            original_code = self.tree.item(selected_item[0])["values"][0]
            
            furniture_code = self.furniture_code_entry.get().strip()
            name = self.name_entry.get().strip()
            type_code = self.type_combobox.get().split('-')[0]
            specification = self.specification_entry.get().strip()
            unit_price = float(self.unit_price_entry.get())
            stock_quantity = int(self.stock_quantity_entry.get() or 0)
            
            if furniture_code != original_code:
                if self.furniture.find_one({"furniture_code": furniture_code}):
                    GUIUtils.show_error("新的家具编码已存在")
                    return
            
            update_data = {
                "furniture_code": furniture_code,
                "name": name,
                "type_code": type_code,
                "specification": specification,
                "unit_price": unit_price,
                "stock_quantity": stock_quantity
            }
            self.furniture.update({"furniture_code": original_code}, update_data)
            GUIUtils.show_success("家具信息修改成功")
            
            self.load_data()
            self.clear_inputs()
            
        except Exception as e:
            GUIUtils.show_error(f"修改失败: {e}")
    
    def delete_furniture(self):
        """删除家具"""
        selected_item = self.tree.selection()
        if not selected_item:
            GUIUtils.show_warning("请选择要删除的家具")
            return
        
        if not GUIUtils.confirm("确定要删除选中的家具吗？"):
            return
        
        try:
            furniture_code = self.tree.item(selected_item[0])["values"][0]
            self.furniture.delete({"furniture_code": furniture_code})
            GUIUtils.show_success("家具删除成功")
            
            self.load_data()
            self.clear_inputs()
            
        except Exception as e:
            GUIUtils.show_error(f"删除失败: {e}")
    
    def clear_inputs(self):
        """清空输入框"""
        self.furniture_code_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.type_combobox.set("")
        self.specification_entry.delete(0, tk.END)
        self.unit_price_entry.delete(0, tk.END)
        self.stock_quantity_entry.delete(0, tk.END)
    
    def load_data(self):
        """加载数据"""
        try:
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            furnitures = self.furniture.get_all_furniture()
            
            for furniture_info in furnitures:
                values = (
                    furniture_info.get("furniture_code", ""),
                    furniture_info.get("name", ""),
                    furniture_info.get("type_code", ""),
                    furniture_info.get("specification", ""),
                    GUIUtils.format_currency(furniture_info.get("unit_price", 0)),
                    furniture_info.get("stock_quantity", 0),
                    GUIUtils.format_datetime(furniture_info.get("created_at", ""))
                )
                self.tree.insert("", "end", values=values)
                
        except Exception as e:
            GUIUtils.show_error(f"加载数据失败: {e}")
    
    def on_item_select(self, event):
        """列表项选择事件"""
        selected_item = self.tree.selection()
        if selected_item:
            values = self.tree.item(selected_item[0])["values"]
            
            self.clear_inputs()
            self.furniture_code_entry.insert(0, values[0])
            self.name_entry.insert(0, values[1])
            
            # 设置类型下拉框
            type_code = values[2]
            for option in self.type_combobox['values']:
                if option.startswith(f"{type_code}-"):
                    self.type_combobox.set(option)
                    break
            
            self.specification_entry.insert(0, values[3])
            # 移除货币符号
            unit_price = str(values[4]).replace('¥', '')
            self.unit_price_entry.insert(0, unit_price)
            self.stock_quantity_entry.insert(0, str(values[5])) 