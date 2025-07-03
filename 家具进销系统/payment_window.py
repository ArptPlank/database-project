"""
收款管理窗口
"""
import tkinter as tk
from tkinter import ttk
from datetime import datetime
from gui_utils import GUIUtils
from models import Payment, Sales, Customer

class PaymentWindow:
    """收款管理窗口"""
    
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("收款管理")
        self.window.grab_set()
        GUIUtils.center_window(self.window, 1400, 800)
        
        self.payment = Payment()
        self.sales = Sales()
        self.customer = Customer()
        self.setup_ui()
        self.load_data()
    
    def setup_ui(self):
        """设置用户界面"""
        main_frame = ttk.Frame(self.window)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 创建选项卡
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill="both", expand=True)
        
        # 收款录入选项卡
        self.payment_frame = ttk.Frame(notebook)
        notebook.add(self.payment_frame, text="收款录入")
        
        # 未收款记录选项卡
        self.unpaid_frame = ttk.Frame(notebook)
        notebook.add(self.unpaid_frame, text="未收款记录")
        
        # 收款记录选项卡
        self.paid_frame = ttk.Frame(notebook)
        notebook.add(self.paid_frame, text="收款记录")
        
        self.create_payment_tab()
        self.create_unpaid_tab()
        self.create_paid_tab()
    
    def create_payment_tab(self):
        """创建收款录入选项卡"""
        # 输入区域
        input_frame = ttk.LabelFrame(self.payment_frame, text="收款信息", padding=10)
        input_frame.pack(fill="x", pady=(0, 10))
        
        input_frame.grid_columnconfigure(1, weight=1)
        input_frame.grid_columnconfigure(3, weight=1)
        
        # 未收款销售记录下拉框
        self.sale_combobox = ttk.Combobox(input_frame, state="readonly")
        ttk.Label(input_frame, text="销售记录:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.sale_combobox.grid(row=0, column=1, columnspan=3, sticky="ew", padx=5, pady=5)
        self.sale_combobox.bind("<<ComboboxSelected>>", self.on_sale_selected)
        
        self.amount_entry = GUIUtils.create_labeled_entry(
            input_frame, "收款金额:", 1, 0)
        
        # 收款方式
        payment_methods = ["现金", "银行转账", "支付宝", "微信支付", "刷卡"]
        self.payment_method_combobox = GUIUtils.create_labeled_combobox(
            input_frame, "收款方式:", payment_methods, 1, 2)
        
        # 收款日期
        ttk.Label(input_frame, text="收款日期:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.date_entry = ttk.Entry(input_frame)
        self.date_entry.grid(row=2, column=1, sticky="ew", padx=5, pady=5)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        
        # 销售信息显示
        info_frame = ttk.LabelFrame(input_frame, text="销售信息", padding=5)
        info_frame.grid(row=3, column=0, columnspan=4, sticky="ew", padx=5, pady=5)
        
        self.sale_info_label = ttk.Label(info_frame, text="请选择销售记录")
        self.sale_info_label.pack()
        
        # 按钮区域
        button_frame = ttk.Frame(self.payment_frame)
        button_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Button(button_frame, text="确认收款", command=self.add_payment).pack(side="left", padx=5)
        ttk.Button(button_frame, text="清空", command=self.clear_payment_inputs).pack(side="left", padx=5)
        ttk.Button(button_frame, text="刷新", command=self.load_unpaid_sales).pack(side="left", padx=5)
        
        # 加载未收款记录
        self.load_unpaid_sales()
    
    def create_unpaid_tab(self):
        """创建未收款记录选项卡"""
        columns = ("sale_id", "furniture_code", "furniture_name", "customer_code", 
                  "customer_name", "quantity", "unit_price", "total_amount", "sale_date")
        headings = ("销售ID", "家具编码", "家具名称", "客户编码", 
                   "客户名称", "数量", "单价", "总金额", "销售日期")
        
        self.unpaid_tree = GUIUtils.create_treeview(self.unpaid_frame, columns, headings)
        
        # 刷新按钮
        refresh_frame = ttk.Frame(self.unpaid_frame)
        refresh_frame.pack(fill="x", pady=5)
        ttk.Button(refresh_frame, text="刷新", command=self.load_unpaid_data).pack(side="left", padx=5)
    
    def create_paid_tab(self):
        """创建收款记录选项卡"""
        columns = ("payment_id", "sale_id", "furniture_code", "customer_code", 
                  "amount", "payment_method", "payment_date")
        headings = ("收款ID", "销售ID", "家具编码", "客户编码", 
                   "收款金额", "收款方式", "收款日期")
        
        self.paid_tree = GUIUtils.create_treeview(self.paid_frame, columns, headings)
        
        # 刷新按钮
        refresh_frame = ttk.Frame(self.paid_frame)
        refresh_frame.pack(fill="x", pady=5)
        ttk.Button(refresh_frame, text="刷新", command=self.load_paid_data).pack(side="left", padx=5)
    
    def load_unpaid_sales(self):
        """加载未收款销售记录到下拉框"""
        try:
            # 获取未收款的销售记录
            unpaid_sales = self.sales.find_all({"payment_status": "未收款"})
            
            # 获取客户信息
            customers = {c['customer_code']: c for c in self.customer.get_all_customers()}
            
            # 构造下拉框选项
            sale_options = []
            for sale in unpaid_sales:
                customer_name = customers.get(sale.get("customer_code", ""), {}).get("name", "")
                option = f"{sale.get('sale_id', '')}-{customer_name}-¥{sale.get('total_amount', 0):.2f}"
                sale_options.append(option)
            
            self.sale_combobox['values'] = sale_options
            
        except Exception as e:
            GUIUtils.show_error(f"加载未收款记录失败: {e}")
    
    def on_sale_selected(self, event):
        """销售记录选择事件"""
        if self.sale_combobox.get():
            sale_id = self.sale_combobox.get().split('-')[0]
            
            # 获取销售记录详情
            sale_record = self.sales.find_one({"sale_id": sale_id})
            if sale_record:
                # 自动填充收款金额
                self.amount_entry.delete(0, tk.END)
                self.amount_entry.insert(0, str(sale_record.get("total_amount", 0)))
                
                # 显示销售信息
                customers = {c['customer_code']: c for c in self.customer.get_all_customers()}
                customer_name = customers.get(sale_record.get("customer_code", ""), {}).get("name", "")
                
                info_text = f"""
销售ID: {sale_record.get('sale_id', '')}
客户: {customer_name}
家具编码: {sale_record.get('furniture_code', '')}
销售数量: {sale_record.get('quantity', 0)}
销售金额: ¥{sale_record.get('total_amount', 0):.2f}
销售日期: {GUIUtils.format_datetime(sale_record.get('sale_date', ''))}
                """.strip()
                
                self.sale_info_label.config(text=info_text)
    
    def add_payment(self):
        """添加收款记录"""
        if not self.sale_combobox.get():
            GUIUtils.show_error("请选择销售记录")
            return
        
        if not self.payment_method_combobox.get():
            GUIUtils.show_error("请选择收款方式")
            return
        
        if not GUIUtils.validate_not_empty(
            [self.amount_entry],
            ["收款金额"]):
            return
        
        if not GUIUtils.validate_number(self.amount_entry, "收款金额"):
            return
        
        try:
            sale_id = self.sale_combobox.get().split('-')[0]
            amount = float(self.amount_entry.get())
            payment_method = self.payment_method_combobox.get()
            payment_date = datetime.strptime(self.date_entry.get(), "%Y-%m-%d %H:%M:%S")
            
            if amount <= 0:
                GUIUtils.show_error("收款金额必须大于0")
                return
            
            # 获取销售记录验证金额
            sale_record = self.sales.find_one({"sale_id": sale_id})
            if not sale_record:
                GUIUtils.show_error("销售记录不存在")
                return
            
            if amount > sale_record.get("total_amount", 0):
                GUIUtils.show_error("收款金额不能超过销售金额")
                return
            
            self.payment.create_payment(sale_id, amount, payment_method, payment_date)
            
            GUIUtils.show_success("收款成功")
            
            self.load_data()
            self.clear_payment_inputs()
            self.load_unpaid_sales()
            
        except ValueError as e:
            GUIUtils.show_error(f"日期格式错误: {e}")
        except Exception as e:
            GUIUtils.show_error(f"收款失败: {e}")
    
    def clear_payment_inputs(self):
        """清空收款输入框"""
        self.sale_combobox.set("")
        self.amount_entry.delete(0, tk.END)
        self.payment_method_combobox.set("")
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.sale_info_label.config(text="请选择销售记录")
    
    def load_data(self):
        """加载所有数据"""
        self.load_unpaid_data()
        self.load_paid_data()
    
    def load_unpaid_data(self):
        """加载未收款数据"""
        try:
            for item in self.unpaid_tree.get_children():
                self.unpaid_tree.delete(item)
            
            # 获取未收款销售记录
            unpaid_sales = self.sales.find_all({"payment_status": "未收款"})
            
            # 获取客户信息
            customers = {c['customer_code']: c for c in self.customer.get_all_customers()}
            
            for record in unpaid_sales:
                customer_code = record.get("customer_code", "")
                customer_name = customers.get(customer_code, {}).get("name", "")
                
                values = (
                    record.get("sale_id", ""),
                    record.get("furniture_code", ""),
                    "",  # 家具名称需要从家具表获取
                    customer_code,
                    customer_name,
                    record.get("quantity", 0),
                    GUIUtils.format_currency(record.get("unit_price", 0)),
                    GUIUtils.format_currency(record.get("total_amount", 0)),
                    GUIUtils.format_datetime(record.get("sale_date", ""))
                )
                self.unpaid_tree.insert("", "end", values=values)
                
        except Exception as e:
            GUIUtils.show_error(f"加载未收款数据失败: {e}")
    
    def load_paid_data(self):
        """加载收款记录数据"""
        try:
            for item in self.paid_tree.get_children():
                self.paid_tree.delete(item)
            
            # 获取收款记录
            payments = self.payment.find_all()
            
            for record in payments:
                values = (
                    record.get("payment_id", ""),
                    record.get("sale_id", ""),
                    "",  # 家具编码需要从销售表获取
                    "",  # 客户编码需要从销售表获取
                    GUIUtils.format_currency(record.get("amount", 0)),
                    record.get("payment_method", ""),
                    GUIUtils.format_datetime(record.get("payment_date", ""))
                )
                self.paid_tree.insert("", "end", values=values)
                
        except Exception as e:
            GUIUtils.show_error(f"加载收款记录失败: {e}") 