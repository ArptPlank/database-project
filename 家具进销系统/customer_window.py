"""
客户管理窗口
"""
import tkinter as tk
from tkinter import ttk
from gui_utils import GUIUtils
from models import Customer

class CustomerWindow:
    """客户管理窗口"""
    
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("客户管理")
        self.window.grab_set()
        GUIUtils.center_window(self.window, 1000, 700)
        
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
        input_frame = ttk.LabelFrame(parent, text="客户信息", padding=10)
        input_frame.pack(fill="x", pady=(0, 10))
        
        input_frame.grid_columnconfigure(1, weight=1)
        input_frame.grid_columnconfigure(3, weight=1)
        
        self.customer_code_entry = GUIUtils.create_labeled_entry(
            input_frame, "客户编码:", 0, 0)
        self.name_entry = GUIUtils.create_labeled_entry(
            input_frame, "客户姓名:", 0, 2)
        self.phone_entry = GUIUtils.create_labeled_entry(
            input_frame, "联系电话:", 1, 0)
        self.address_entry = GUIUtils.create_labeled_entry(
            input_frame, "地址:", 1, 2)
        self.email_entry = GUIUtils.create_labeled_entry(
            input_frame, "邮箱:", 2, 0, 3)
    
    def create_button_area(self, parent):
        """创建按钮区域"""
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Button(button_frame, text="添加", command=self.add_customer).pack(side="left", padx=5)
        ttk.Button(button_frame, text="修改", command=self.update_customer).pack(side="left", padx=5)
        ttk.Button(button_frame, text="删除", command=self.delete_customer).pack(side="left", padx=5)
        ttk.Button(button_frame, text="清空", command=self.clear_inputs).pack(side="left", padx=5)
        ttk.Button(button_frame, text="刷新", command=self.load_data).pack(side="left", padx=5)
    
    def create_list_area(self, parent):
        """创建列表区域"""
        columns = ("customer_code", "name", "phone", "address", "email", "created_at")
        headings = ("客户编码", "客户姓名", "联系电话", "地址", "邮箱", "创建时间")
        
        self.tree = GUIUtils.create_treeview(parent, columns, headings)
        self.tree.bind("<<TreeviewSelect>>", self.on_item_select)
    
    def add_customer(self):
        """添加客户"""
        if not GUIUtils.validate_not_empty(
            [self.customer_code_entry, self.name_entry, self.phone_entry],
            ["客户编码", "客户姓名", "联系电话"]):
            return
        
        try:
            customer_code = self.customer_code_entry.get().strip()
            name = self.name_entry.get().strip()
            phone = self.phone_entry.get().strip()
            address = self.address_entry.get().strip()
            email = self.email_entry.get().strip()
            
            if self.customer.find_one({"customer_code": customer_code}):
                GUIUtils.show_error("客户编码已存在")
                return
            
            self.customer.create_customer(customer_code, name, phone, address, email)
            GUIUtils.show_success("客户添加成功")
            
            self.load_data()
            self.clear_inputs()
            
        except Exception as e:
            GUIUtils.show_error(f"添加失败: {e}")
    
    def update_customer(self):
        """修改客户"""
        selected_item = self.tree.selection()
        if not selected_item:
            GUIUtils.show_warning("请选择要修改的客户")
            return
        
        if not GUIUtils.validate_not_empty(
            [self.customer_code_entry, self.name_entry, self.phone_entry],
            ["客户编码", "客户姓名", "联系电话"]):
            return
        
        try:
            original_code = self.tree.item(selected_item[0])["values"][0]
            
            customer_code = self.customer_code_entry.get().strip()
            name = self.name_entry.get().strip()
            phone = self.phone_entry.get().strip()
            address = self.address_entry.get().strip()
            email = self.email_entry.get().strip()
            
            if customer_code != original_code:
                if self.customer.find_one({"customer_code": customer_code}):
                    GUIUtils.show_error("新的客户编码已存在")
                    return
            
            update_data = {
                "customer_code": customer_code,
                "name": name,
                "phone": phone,
                "address": address,
                "email": email
            }
            self.customer.update({"customer_code": original_code}, update_data)
            GUIUtils.show_success("客户修改成功")
            
            self.load_data()
            self.clear_inputs()
            
        except Exception as e:
            GUIUtils.show_error(f"修改失败: {e}")
    
    def delete_customer(self):
        """删除客户"""
        selected_item = self.tree.selection()
        if not selected_item:
            GUIUtils.show_warning("请选择要删除的客户")
            return
        
        if not GUIUtils.confirm("确定要删除选中的客户吗？"):
            return
        
        try:
            customer_code = self.tree.item(selected_item[0])["values"][0]
            self.customer.delete({"customer_code": customer_code})
            GUIUtils.show_success("客户删除成功")
            
            self.load_data()
            self.clear_inputs()
            
        except Exception as e:
            GUIUtils.show_error(f"删除失败: {e}")
    
    def clear_inputs(self):
        """清空输入框"""
        self.customer_code_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.address_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
    
    def load_data(self):
        """加载数据"""
        try:
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            customers = self.customer.get_all_customers()
            
            for customer_info in customers:
                values = (
                    customer_info.get("customer_code", ""),
                    customer_info.get("name", ""),
                    customer_info.get("phone", ""),
                    customer_info.get("address", ""),
                    customer_info.get("email", ""),
                    GUIUtils.format_datetime(customer_info.get("created_at", ""))
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
            self.customer_code_entry.insert(0, values[0])
            self.name_entry.insert(0, values[1])
            self.phone_entry.insert(0, values[2])
            self.address_entry.insert(0, values[3])
            self.email_entry.insert(0, values[4]) 