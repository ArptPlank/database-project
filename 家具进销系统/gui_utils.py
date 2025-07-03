"""
GUI工具类 - 现代化版本
包含通用的界面组件和美化功能
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
from datetime import datetime

class GUIUtils:
    """现代化GUI工具类"""
    
    # 高颜值现代化配色方案
    COLORS = {
        'primary': '#6366F1',        # 现代紫色 - 主色调
        'primary_dark': '#4F46E5',   # 深紫色
        'primary_light': '#8B5CF6',  # 浅紫色
        'secondary': '#06B6D4',      # 青色 - 次要色
        'success': '#10B981',        # 现代绿色
        'warning': '#F59E0B',        # 现代橙色
        'danger': '#EF4444',         # 现代红色
        'info': '#3B82F6',           # 现代蓝色
        'background': '#F8FAFC',     # 极浅灰背景
        'surface': '#FFFFFF',        # 纯白表面
        'surface_hover': '#F1F5F9',  # 悬停表面色
        'text': '#1E293B',           # 深灰文字
        'text_secondary': '#64748B', # 中灰文字
        'text_light': '#94A3B8',     # 浅灰文字
        'border': '#E2E8F0',         # 浅边框
        'border_focus': '#6366F1',   # 聚焦边框
        'shadow': 'rgba(0,0,0,0.1)', # 阴影色
        'gradient_start': '#667EEA',  # 渐变起始色
        'gradient_end': '#764BA2'     # 渐变结束色
    }
    
    @staticmethod
    def setup_modern_style():
        """设置现代化主题样式"""
        style = ttk.Style()
        
        # 使用clam主题作为基础
        style.theme_use('clam')
        
        # 现代化主按钮样式
        style.configure('Modern.TButton',
                       background=GUIUtils.COLORS['primary'],
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       padding=(25, 15),
                       font=('Microsoft YaHei UI', 11, 'bold'),
                       relief='flat')
        
        style.map('Modern.TButton',
                 background=[('active', GUIUtils.COLORS['primary_dark']),
                           ('pressed', GUIUtils.COLORS['primary_light'])])
        
        # 成功按钮样式 - 绿色系
        style.configure('Success.TButton',
                       background=GUIUtils.COLORS['success'],
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       padding=(20, 12),
                       font=('Microsoft YaHei UI', 10, 'bold'),
                       relief='flat')
        
        style.map('Success.TButton',
                 background=[('active', '#059669'),
                           ('pressed', '#047857')])
        
        # 警告按钮样式 - 橙色系
        style.configure('Warning.TButton',
                       background=GUIUtils.COLORS['warning'],
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       padding=(20, 12),
                       font=('Microsoft YaHei UI', 10, 'bold'),
                       relief='flat')
        
        style.map('Warning.TButton',
                 background=[('active', '#D97706'),
                           ('pressed', '#B45309')])
        
        # 危险按钮样式 - 红色系
        style.configure('Danger.TButton',
                       background=GUIUtils.COLORS['danger'],
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       padding=(20, 12),
                       font=('Microsoft YaHei UI', 10, 'bold'),
                       relief='flat')
        
        style.map('Danger.TButton',
                 background=[('active', '#DC2626'),
                           ('pressed', '#B91C1C')])
        
        # 信息按钮样式 - 蓝色系
        style.configure('Info.TButton',
                       background=GUIUtils.COLORS['info'],
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       padding=(20, 12),
                       font=('Microsoft YaHei UI', 10, 'bold'),
                       relief='flat')
        
        style.map('Info.TButton',
                 background=[('active', '#2563EB'),
                           ('pressed', '#1D4ED8')])
        
        # 次要按钮样式 - 边框按钮
        style.configure('Secondary.TButton',
                       background=GUIUtils.COLORS['surface'],
                       foreground=GUIUtils.COLORS['primary'],
                       borderwidth=2,
                       focuscolor='none',
                       padding=(20, 12),
                       font=('Microsoft YaHei UI', 10, 'bold'),
                       relief='solid',
                       bordercolor=GUIUtils.COLORS['primary'])
        
        style.map('Secondary.TButton',
                 background=[('active', GUIUtils.COLORS['surface_hover']),
                           ('pressed', GUIUtils.COLORS['border'])])
        
        # 标签框样式
        style.configure('Modern.TLabelframe',
                       background=GUIUtils.COLORS['surface'],
                       borderwidth=1,
                       relief='solid',
                       bordercolor=GUIUtils.COLORS['border'])
        
        style.configure('Modern.TLabelframe.Label',
                       background=GUIUtils.COLORS['surface'],
                       foreground=GUIUtils.COLORS['primary'],
                       font=('Microsoft YaHei UI', 12, 'bold'))
        
        # 高颜值表格样式
        style.configure('Modern.Treeview',
                       background=GUIUtils.COLORS['surface'],
                       foreground=GUIUtils.COLORS['text'],
                       rowheight=40,
                       fieldbackground=GUIUtils.COLORS['surface'],
                       font=('Microsoft YaHei UI', 10),
                       borderwidth=1,
                       relief='solid',
                       bordercolor=GUIUtils.COLORS['border'])
        
        style.configure('Modern.Treeview.Heading',
                       background=GUIUtils.COLORS['primary'],
                       foreground='white',
                       font=('Microsoft YaHei UI', 11, 'bold'),
                       relief='flat',
                       borderwidth=0,
                       padding=(10, 15))
        
        style.map('Modern.Treeview',
                 background=[('selected', GUIUtils.COLORS['primary_light'])],
                 foreground=[('selected', 'white')])
        
        style.map('Modern.Treeview.Heading',
                 background=[('active', GUIUtils.COLORS['primary_dark'])])
        
        # 现代化输入框样式
        style.configure('Modern.TEntry',
                       borderwidth=2,
                       relief='solid',
                       bordercolor=GUIUtils.COLORS['border'],
                       padding=(15, 12),
                       font=('Microsoft YaHei UI', 11),
                       insertcolor=GUIUtils.COLORS['primary'])
        
        style.map('Modern.TEntry',
                 bordercolor=[('focus', GUIUtils.COLORS['border_focus'])])
        
        # 现代化下拉框样式
        style.configure('Modern.TCombobox',
                       borderwidth=2,
                       relief='solid',
                       bordercolor=GUIUtils.COLORS['border'],
                       padding=(15, 12),
                       font=('Microsoft YaHei UI', 11))
        
        style.map('Modern.TCombobox',
                 bordercolor=[('focus', GUIUtils.COLORS['border_focus'])])
        
        return style
    
    @staticmethod
    def create_modern_window(title, width=1000, height=700):
        """创建现代化窗口"""
        window = tk.Toplevel()
        window.title(title)
        window.configure(bg=GUIUtils.COLORS['background'])
        GUIUtils.center_window(window, width, height)
        
        # 设置图标和样式
        window.resizable(True, True)
        window.minsize(800, 600)
        
        return window
    
    @staticmethod
    def create_modern_frame(parent, title="", padding=20):
        """创建现代化框架"""
        if title:
            frame = ttk.LabelFrame(parent, text=title, style='Modern.TLabelframe', padding=padding)
        else:
            frame = ttk.Frame(parent, padding=padding)
            frame.configure(style='Modern.TFrame')
        return frame
    
    @staticmethod
    def create_modern_button(parent, text, command=None, style_type="primary", width=15):
        """创建现代化按钮"""
        style_map = {
            "primary": 'Modern.TButton',
            "success": 'Success.TButton',
            "warning": 'Warning.TButton', 
            "danger": 'Danger.TButton',
            "info": 'Info.TButton',
            "secondary": 'Secondary.TButton'
        }
        
        style = style_map.get(style_type, 'Modern.TButton')
        return ttk.Button(parent, text=text, command=command, 
                         style=style, width=width)
    
    @staticmethod
    def create_title_label(parent, text, size=20):
        """创建现代化标题标签"""
        return tk.Label(parent, text=text, 
                       font=('Microsoft YaHei UI', size, 'bold'),
                       fg=GUIUtils.COLORS['text'],
                       bg=GUIUtils.COLORS['background'])
    
    @staticmethod
    def create_subtitle_label(parent, text, size=14):
        """创建副标题标签"""
        return tk.Label(parent, text=text, 
                       font=('Microsoft YaHei UI', size),
                       fg=GUIUtils.COLORS['text_secondary'],
                       bg=GUIUtils.COLORS['background'])
    
    @staticmethod
    def create_modern_treeview(parent, columns, headings, height=12):
        """创建现代化表格"""
        # 创建框架
        frame = ttk.Frame(parent)
        
        # 创建表格
        tree = ttk.Treeview(frame, columns=columns, show="headings", 
                           height=height, style='Modern.Treeview')
        
        # 设置列标题和宽度
        for col, heading in zip(columns, headings):
            tree.heading(col, text=heading)
            tree.column(col, width=120, anchor="center")
        
        # 创建滚动条
        v_scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        h_scrollbar = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # 布局
        tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns") 
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        
        return frame, tree
    
    @staticmethod
    def create_labeled_entry(parent, label_text, row, col=0, colspan=1, sticky="ew", width=None):
        """创建现代化标签输入框"""
        label = ttk.Label(parent, text=label_text, 
                         font=('Microsoft YaHei UI', 10))
        label.grid(row=row, column=col, sticky="w", padx=5, pady=8)
        
        entry = ttk.Entry(parent, style='Modern.TEntry', width=width)
        entry.grid(row=row, column=col+1, columnspan=colspan, sticky=sticky, padx=5, pady=8)
        
        return entry
    
    @staticmethod
    def create_labeled_combobox(parent, label_text, values, row, col=0, colspan=1, sticky="ew"):
        """创建现代化标签下拉框"""
        label = ttk.Label(parent, text=label_text,
                         font=('Microsoft YaHei UI', 10))
        label.grid(row=row, column=col, sticky="w", padx=5, pady=8)
        
        combobox = ttk.Combobox(parent, values=values, state="readonly", 
                               style='Modern.TCombobox')
        combobox.grid(row=row, column=col+1, columnspan=colspan, sticky=sticky, padx=5, pady=8)
        
        return combobox
    
    @staticmethod
    def create_search_frame(parent, search_callback):
        """创建现代化搜索框架"""
        search_frame = ttk.Frame(parent)
        
        # 搜索标签
        search_label = ttk.Label(search_frame, text="🔍 搜索:", 
                                font=('Microsoft YaHei UI', 10))
        search_label.pack(side="left", padx=(0, 10))
        
        # 搜索输入框
        search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=search_var, 
                                style='Modern.TEntry', width=25)
        search_entry.pack(side="left", padx=(0, 10))
        
        # 搜索按钮
        search_btn = GUIUtils.create_modern_button(search_frame, "搜索", 
                                                  lambda: search_callback(search_var.get()), 
                                                  width=10)
        search_btn.pack(side="left", padx=(0, 5))
        
        # 清空按钮
        clear_btn = GUIUtils.create_modern_button(search_frame, "清空", 
                                                 lambda: [search_var.set(""), search_callback("")], 
                                                 style_type="warning", width=8)
        clear_btn.pack(side="left")
        
        return search_frame, search_var
    
    @staticmethod
    def center_window(window, width, height):
        """居中显示窗口"""
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        window.geometry(f"{width}x{height}+{x}+{y}")
    
    @staticmethod
    def show_success(message, title="✅ 成功"):
        """显示成功消息"""
        messagebox.showinfo(title, message)
    
    @staticmethod
    def show_error(message, title="❌ 错误"):
        """显示错误消息"""
        messagebox.showerror(title, message)
    
    @staticmethod
    def show_warning(message, title="⚠️ 警告"):
        """显示警告消息"""
        messagebox.showwarning(title, message)
    
    @staticmethod
    def show_info(message, title="ℹ️ 信息"):
        """显示信息消息"""
        messagebox.showinfo(title, message)
    
    @staticmethod
    def confirm(message, title="❓ 确认"):
        """确认对话框"""
        return messagebox.askyesno(title, message)
    
    @staticmethod
    def validate_not_empty(entries, labels):
        """验证输入框不为空"""
        for entry, label in zip(entries, labels):
            if not entry.get().strip():
                GUIUtils.show_error(f"{label}不能为空")
                entry.focus()
                return False
        return True
    
    @staticmethod
    def validate_number(entry, label):
        """验证数字输入"""
        try:
            float(entry.get())
            return True
        except ValueError:
            GUIUtils.show_error(f"{label}必须是数字")
            entry.focus()
            return False
    
    @staticmethod
    def export_to_csv(data, headers, filename_prefix="export"):
        """导出数据到CSV文件"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{filename_prefix}_{timestamp}.csv"
            
            filepath = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv")],
                initialfile=filename
            )
            
            if filepath:
                with open(filepath, 'w', newline='', encoding='utf-8-sig') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(headers)
                    writer.writerows(data)
                
                GUIUtils.show_success(f"数据已成功导出到:\n{filepath}")
                return True
            return False
        except Exception as e:
            GUIUtils.show_error(f"导出失败: {e}")
            return False
    
    @staticmethod
    def format_datetime(dt):
        """格式化日期时间"""
        if isinstance(dt, datetime):
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        return str(dt)
    
    @staticmethod
    def format_currency(amount):
        """格式化货币"""
        return f"¥{amount:,.2f}"
    
    @staticmethod
    def clear_treeview(treeview):
        """清空表格"""
        for item in treeview.get_children():
            treeview.delete(item)
    
    @staticmethod
    def create_treeview(parent, columns, headings, height=12):
        """创建表格"""
        # 创建表格控件
        tree = ttk.Treeview(parent, columns=columns, show="headings", 
                           height=height, style='Modern.Treeview')
        
        # 设置列标题和宽度
        for col, heading in zip(columns, headings):
            tree.heading(col, text=heading)
            tree.column(col, width=120, anchor="center")
        
        # 创建垂直滚动条
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        # 布局
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        return tree 