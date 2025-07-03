"""
主窗口模块 - 现代化版本
"""
import tkinter as tk
from tkinter import ttk, messagebox
from gui_utils import GUIUtils
from furniture_type_window import FurnitureTypeWindow
from supplier_window import SupplierWindow
from customer_window import CustomerWindow
from furniture_window import FurnitureWindow
from stock_in_window import StockInWindow
from sales_window import SalesWindow
from payment_window import PaymentWindow
from statistics_window import StatisticsWindow

class MainWindow:
    """现代化主窗口类"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🏪 家具城进销存管理系统")
        self.root.configure(bg=GUIUtils.COLORS['background'])
        self.root.state('zoomed')  # 最大化窗口
        
        # 设置现代化样式
        self.style = GUIUtils.setup_modern_style()
        
        self.setup_ui()
    
    def setup_ui(self):
        """设置现代化用户界面"""
        # 创建主容器
        main_container = tk.Frame(self.root, bg=GUIUtils.COLORS['background'])
        main_container.pack(fill="both", expand=True)
        
        # 创建顶部标题区域
        self.create_header(main_container)
        
        # 创建菜单栏
        self.create_menu()
        
        # 创建主内容区域
        content_frame = tk.Frame(main_container, bg=GUIUtils.COLORS['background'])
        content_frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        # 创建功能区域
        self.create_function_areas(content_frame)
        
        # 创建底部状态栏
        self.create_status_bar()
    
    def create_header(self, parent):
        """创建高颜值渐变头部区域"""
        # 创建渐变背景
        header_canvas = tk.Canvas(parent, height=120, highlightthickness=0)
        header_canvas.pack(fill="x", pady=(0, 30))
        
        def draw_gradient():
            header_canvas.delete("gradient")
            width = header_canvas.winfo_width()
            if width > 1:
                # 创建紫色渐变
                for i in range(width):
                    ratio = i / width
                    # 从 #667EEA 到 #764BA2
                    r1, g1, b1 = 0x66, 0x7E, 0xEA
                    r2, g2, b2 = 0x76, 0x4B, 0xA2
                    
                    r = int(r1 + (r2 - r1) * ratio)
                    g = int(g1 + (g2 - g1) * ratio)
                    b = int(b1 + (b2 - b1) * ratio)
                    
                    color = f"#{r:02x}{g:02x}{b:02x}"
                    header_canvas.create_line(i, 0, i, 120, fill=color, tags="gradient")
                
                # 添加标题文字
                header_canvas.create_text(width//2, 50, 
                                        text="🏪 家具城进销存管理系统",
                                        font=('Microsoft YaHei UI', 32, 'bold'),
                                        fill='white', tags="title")
                header_canvas.create_text(width//2, 85,
                                        text="✨ 高颜值现代化家具管理解决方案 ✨",
                                        font=('Microsoft YaHei UI', 16),
                                        fill='white', tags="subtitle")
        
        header_canvas.bind('<Configure>', lambda e: draw_gradient())
        header_canvas.after(1, draw_gradient)
    
    def create_menu(self):
        """创建现代化菜单栏"""
        menubar = tk.Menu(self.root, bg=GUIUtils.COLORS['surface'], 
                         fg=GUIUtils.COLORS['text'], 
                         activebackground=GUIUtils.COLORS['primary'],
                         activeforeground='white')
        self.root.config(menu=menubar)
        
        # 基础数据菜单
        basic_menu = tk.Menu(menubar, tearoff=0, 
                            bg=GUIUtils.COLORS['surface'], 
                            fg=GUIUtils.COLORS['text'])
        menubar.add_cascade(label="📊 基础数据", menu=basic_menu)
        basic_menu.add_command(label="🗂️ 家具类型管理", command=self.open_furniture_type_window)
        basic_menu.add_command(label="🏢 供应商管理", command=self.open_supplier_window)
        basic_menu.add_command(label="👥 客户管理", command=self.open_customer_window)
        basic_menu.add_command(label="🪑 家具信息管理", command=self.open_furniture_window)
        
        # 业务操作菜单
        business_menu = tk.Menu(menubar, tearoff=0,
                               bg=GUIUtils.COLORS['surface'], 
                               fg=GUIUtils.COLORS['text'])
        menubar.add_cascade(label="💼 业务操作", menu=business_menu)
        business_menu.add_command(label="📦 家具入库", command=self.open_stock_in_window)
        business_menu.add_command(label="🛒 家具销售", command=self.open_sales_window)
        business_menu.add_command(label="💰 收款管理", command=self.open_payment_window)
        
        # 统计查询菜单
        statistics_menu = tk.Menu(menubar, tearoff=0,
                                 bg=GUIUtils.COLORS['surface'], 
                                 fg=GUIUtils.COLORS['text'])
        menubar.add_cascade(label="📈 统计查询", menu=statistics_menu)
        statistics_menu.add_command(label="📊 进销存统计", command=self.open_statistics_window)
        statistics_menu.add_separator()
        statistics_menu.add_command(label="💾 数据备份", command=self.backup_data)
        statistics_menu.add_command(label="🔄 数据恢复", command=self.restore_data)
        
        # 帮助菜单
        help_menu = tk.Menu(menubar, tearoff=0,
                           bg=GUIUtils.COLORS['surface'], 
                           fg=GUIUtils.COLORS['text'])
        menubar.add_cascade(label="❓ 帮助", menu=help_menu)
        help_menu.add_command(label="ℹ️ 关于系统", command=self.show_about)
    
    def create_function_areas(self, parent):
        """创建现代化功能区域"""
        # 创建卡片容器 - 使用水平布局
        cards_container = tk.Frame(parent, bg=GUIUtils.COLORS['background'])
        cards_container.pack(expand=True, fill="both", pady=20)
        
        # 基础数据管理卡片
        basic_card_frame = tk.Frame(cards_container, bg=GUIUtils.COLORS['background'])
        basic_card_frame.pack(side="left", fill="both", expand=True, padx=15)
        
        basic_card = self.create_function_card(basic_card_frame, "📊 基础数据管理", 
                                              "管理家具类型、供应商、客户等基础信息")
        
        basic_buttons = [
            ("🗂️ 家具类型", self.open_furniture_type_window, "primary"),
            ("🏢 供应商管理", self.open_supplier_window, "primary"),
            ("👥 客户管理", self.open_customer_window, "primary"),
            ("🪑 家具信息", self.open_furniture_window, "primary")
        ]
        
        self.add_buttons_to_card(basic_card, basic_buttons)
        
        # 业务操作卡片
        business_card_frame = tk.Frame(cards_container, bg=GUIUtils.COLORS['background'])
        business_card_frame.pack(side="left", fill="both", expand=True, padx=15)
        
        business_card = self.create_function_card(business_card_frame, "💼 业务操作",
                                                 "处理日常进销存业务操作")
        
        business_buttons = [
            ("📦 家具入库", self.open_stock_in_window, "success"),
            ("🛒 家具销售", self.open_sales_window, "warning"),
            ("💰 收款管理", self.open_payment_window, "success")
        ]
        
        self.add_buttons_to_card(business_card, business_buttons)
        
        # 统计分析卡片
        stats_card_frame = tk.Frame(cards_container, bg=GUIUtils.COLORS['background'])
        stats_card_frame.pack(side="left", fill="both", expand=True, padx=15)
        
        stats_card = self.create_function_card(stats_card_frame, "📈 统计分析",
                                              "查看各类统计报表和数据分析")
        
        stats_buttons = [
            ("📊 进销存统计", self.open_statistics_window, "info"),
            ("💾 数据备份", self.backup_data, "warning"),
            ("🔄 数据恢复", self.restore_data, "success")
        ]
        
        self.add_buttons_to_card(stats_card, stats_buttons)
    
    def create_function_card(self, parent, title, description):
        """创建高颜值功能卡片"""
        # 卡片主体 - 简化版本，确保显示
        card_frame = tk.Frame(parent, bg=GUIUtils.COLORS['surface'], 
                             relief='raised', bd=2, padx=20, pady=20)
        card_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 卡片头部 - 使用简单的背景色
        header_frame = tk.Frame(card_frame, bg=GUIUtils.COLORS['primary'], height=60)
        header_frame.pack(fill="x", pady=(0, 15))
        header_frame.pack_propagate(False)
        
        # 标题
        title_label = tk.Label(header_frame, text=title,
                              font=('Microsoft YaHei UI', 16, 'bold'),
                              fg='white', bg=GUIUtils.COLORS['primary'])
        title_label.pack(expand=True)
        
        # 描述区域
        desc_label = tk.Label(card_frame, text=description,
                             font=('Microsoft YaHei UI', 11),
                             fg=GUIUtils.COLORS['text_secondary'],
                             bg=GUIUtils.COLORS['surface'],
                             wraplength=250,
                             justify='center')
        desc_label.pack(pady=(0, 20))
        
        # 分隔线
        separator = tk.Frame(card_frame, height=1, bg=GUIUtils.COLORS['border'])
        separator.pack(fill="x", pady=(0, 20))
        
        # 按钮容器
        button_frame = tk.Frame(card_frame, bg=GUIUtils.COLORS['surface'])
        button_frame.pack(fill="both", expand=True)
        
        return button_frame
    
    def add_buttons_to_card(self, card_frame, buttons):
        """向卡片添加高颜值按钮"""
        for i, (text, command, style_type) in enumerate(buttons):
            btn = GUIUtils.create_modern_button(card_frame, text, command, 
                                               style_type, width=22)
            btn.pack(pady=10, fill="x", ipady=5)
    
    def create_status_bar(self):
        """创建现代化状态栏"""
        status_frame = tk.Frame(self.root, bg=GUIUtils.COLORS['surface'], 
                               relief='solid', bd=1, height=30)
        status_frame.pack(side="bottom", fill="x")
        status_frame.pack_propagate(False)
        
        # 状态信息
        self.status_label = tk.Label(status_frame, text="✅ 系统就绪",
                                   font=('Microsoft YaHei UI', 9),
                                   fg=GUIUtils.COLORS['text'],
                                   bg=GUIUtils.COLORS['surface'])
        self.status_label.pack(side="left", padx=10)
        
        # 时间信息
        from datetime import datetime
        time_text = f"当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        time_label = tk.Label(status_frame, text=time_text,
                             font=('Microsoft YaHei UI', 9),
                             fg=GUIUtils.COLORS['text_secondary'],
                             bg=GUIUtils.COLORS['surface'])
        time_label.pack(side="right", padx=10)
    
    def set_status(self, message):
        """设置状态栏消息"""
        self.status_label.config(text=message)
    
    # 窗口打开方法
    def open_furniture_type_window(self):
        """打开家具类型管理窗口"""
        self.set_status("📂 正在打开家具类型管理...")
        FurnitureTypeWindow(self.root)
        self.set_status("✅ 家具类型管理窗口已打开")
    
    def open_supplier_window(self):
        """打开供应商管理窗口"""
        self.set_status("📂 正在打开供应商管理...")
        SupplierWindow(self.root)
        self.set_status("✅ 供应商管理窗口已打开")
    
    def open_customer_window(self):
        """打开客户管理窗口"""
        self.set_status("📂 正在打开客户管理...")
        CustomerWindow(self.root)
        self.set_status("✅ 客户管理窗口已打开")
    
    def open_furniture_window(self):
        """打开家具信息管理窗口"""
        self.set_status("📂 正在打开家具信息管理...")
        FurnitureWindow(self.root)
        self.set_status("✅ 家具信息管理窗口已打开")
    
    def open_stock_in_window(self):
        """打开入库管理窗口"""
        self.set_status("📂 正在打开入库管理...")
        StockInWindow(self.root)
        self.set_status("✅ 入库管理窗口已打开")
    
    def open_sales_window(self):
        """打开销售管理窗口"""
        self.set_status("📂 正在打开销售管理...")
        SalesWindow(self.root)
        self.set_status("✅ 销售管理窗口已打开")
    
    def open_payment_window(self):
        """打开收款管理窗口"""
        self.set_status("📂 正在打开收款管理...")
        PaymentWindow(self.root)
        self.set_status("✅ 收款管理窗口已打开")
    
    def open_statistics_window(self):
        """打开统计查询窗口"""
        self.set_status("📂 正在打开统计查询...")
        StatisticsWindow(self.root)
        self.set_status("✅ 统计查询窗口已打开")
    
    def backup_data(self):
        """数据备份功能"""
        try:
            from tkinter import filedialog
            import json
            from datetime import datetime
            
            # 选择备份文件保存位置
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            default_filename = f"furniture_backup_{timestamp}.json"
            
            file_path = filedialog.asksaveasfilename(
                title="选择备份文件保存位置",
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                initialfile=default_filename
            )
            
            if not file_path:
                return
            
            # 从数据库获取所有数据
            from database import db_manager
            db = db_manager.get_database()
            backup_data = {}
            
            # 获取所有集合的数据
            collections = ['furniture_types', 'suppliers', 'customers', 'furniture', 'stock_in', 'sales', 'payments']
            
            total_records = 0
            for collection_name in collections:
                collection = db[collection_name]
                data = list(collection.find({}))
                
                # 转换ObjectId为字符串
                for item in data:
                    if '_id' in item:
                        item['_id'] = str(item['_id'])
                        # 转换其他可能的ObjectId字段
                        for key, value in item.items():
                            if hasattr(value, '__class__') and value.__class__.__name__ == 'ObjectId':
                                item[key] = str(value)
                
                backup_data[collection_name] = data
                total_records += len(data)
            
            # 添加备份信息
            backup_data['backup_info'] = {
                'timestamp': datetime.now().isoformat(),
                'version': '1.0',
                'total_records': total_records
            }
            
            # 保存到文件
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(backup_data, f, ensure_ascii=False, indent=2, default=str)
            
            self.set_status("✅ 数据备份完成")
            GUIUtils.show_success(f"数据备份成功！\n备份文件：{file_path}\n总记录数：{total_records}")
            
        except Exception as e:
            self.set_status("❌ 数据备份失败")
            GUIUtils.show_error(f"数据备份失败：{str(e)}")
    
    def restore_data(self):
        """数据恢复功能"""
        try:
            from tkinter import filedialog
            import json
            
            # 警告用户
            if not GUIUtils.confirm("数据恢复将覆盖当前所有数据，是否继续？\n建议先备份当前数据！"):
                return
            
            # 选择备份文件
            file_path = filedialog.askopenfilename(
                title="选择备份文件",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            
            if not file_path:
                return
            
            # 读取备份文件
            with open(file_path, 'r', encoding='utf-8') as f:
                backup_data = json.load(f)
            
            # 验证备份文件格式
            if 'backup_info' not in backup_data:
                GUIUtils.show_error("无效的备份文件格式！")
                return
            
            # 显示备份信息
            backup_info = backup_data['backup_info']
            if not GUIUtils.confirm(f"备份文件信息：\n"
                                  f"时间：{backup_info.get('timestamp', '未知')}\n"
                                  f"版本：{backup_info.get('version', '未知')}\n"
                                  f"记录数：{backup_info.get('total_records', 0)}\n\n"
                                  f"确定要恢复此备份吗？"):
                return
            
            # 清空现有数据并恢复
            from database import db_manager
            from bson import ObjectId
            db = db_manager.get_database()
            
            collections = ['furniture_types', 'suppliers', 'customers', 'furniture', 'stock_in', 'sales', 'payments']
            restored_count = 0
            
            for collection_name in collections:
                if collection_name in backup_data and isinstance(backup_data[collection_name], list):
                    collection = db[collection_name]
                    
                    # 清空现有数据
                    collection.delete_many({})
                    
                    # 插入备份数据
                    if backup_data[collection_name]:
                        # 转换字符串ID回ObjectId
                        for item in backup_data[collection_name]:
                            if '_id' in item and isinstance(item['_id'], str):
                                try:
                                    item['_id'] = ObjectId(item['_id'])
                                except:
                                    # 如果转换失败，删除_id让MongoDB自动生成
                                    del item['_id']
                        
                        collection.insert_many(backup_data[collection_name])
                        restored_count += len(backup_data[collection_name])
            
            self.set_status("✅ 数据恢复完成")
            GUIUtils.show_success(f"数据恢复成功！\n恢复记录数：{restored_count}")
            
        except Exception as e:
            self.set_status("❌ 数据恢复失败")
            GUIUtils.show_error(f"数据恢复失败：{str(e)}")
    
    def show_about(self):
        """显示关于信息"""
        about_text = """
🏪 家具城进销存管理系统 v2.0

🎯 功能特性：
• 🗂️ 家具类型、供应商、客户信息管理
• 🪑 家具信息管理
• 📦 入库和销售管理
• 💰 收款管理
• 🔄 自动库存更新
• 📊 进销存统计分析

🛠️ 技术栈：
• Python 3.x + Tkinter GUI
• MongoDB 数据库
• 现代化UI设计

📅 更新日期：2024年12月
🏢 版权所有：家具城管理系统
        """
        messagebox.showinfo("ℹ️ 关于系统", about_text)
    
    def run(self):
        """运行应用程序"""
        try:
            self.root.mainloop()
        except Exception as e:
            GUIUtils.show_error(f"应用程序运行错误: {e}")
        finally:
            # 关闭数据库连接
            from database import db_manager
            db_manager.close() 