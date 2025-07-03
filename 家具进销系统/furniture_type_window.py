"""
家具类型管理窗口
"""
import tkinter as tk
from tkinter import ttk
from gui_utils import GUIUtils
from models import FurnitureType

class FurnitureTypeWindow:
    """现代化家具类型管理窗口"""
    
    def __init__(self, parent):
        self.parent = parent
        self.furniture_type = FurnitureType()
        
        # 创建现代化窗口
        self.window = GUIUtils.create_modern_window("🗂️ 家具类型管理", 1100, 750)
        self.window.grab_set()  # 模态窗口
        
        # 设置现代化样式
        GUIUtils.setup_modern_style()
        
        self.setup_ui()
        self.load_data()
    
    def setup_ui(self):
        """设置现代化用户界面"""
        # 主容器
        main_container = tk.Frame(self.window, bg=GUIUtils.COLORS['background'])
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # 标题区域
        self.create_header(main_container)
        
        # 内容区域
        content_frame = tk.Frame(main_container, bg=GUIUtils.COLORS['background'])
        content_frame.pack(fill="both", expand=True, pady=20)
        
        # 左侧：表单区域
        form_frame = GUIUtils.create_modern_frame(content_frame, "✏️ 类型信息", 20)
        form_frame.pack(side="left", fill="y", padx=(0, 15))
        
        self.create_form(form_frame)
        
        # 右侧：数据展示区域  
        data_frame = GUIUtils.create_modern_frame(content_frame, "📋 类型列表", 20)
        data_frame.pack(side="right", fill="both", expand=True)
        
        self.create_data_area(data_frame)
    
    def create_header(self, parent):
        """创建标题区域"""
        header_frame = tk.Frame(parent, bg=GUIUtils.COLORS['info'], height=80)
        header_frame.pack(fill="x", pady=(0, 20))
        header_frame.pack_propagate(False)
        
        # 主标题
        title_label = tk.Label(header_frame,
                              text="🗂️ 家具类型管理",
                              font=('Microsoft YaHei UI', 24, 'bold'),
                              fg='white',
                              bg=GUIUtils.COLORS['info'])
        title_label.pack(expand=True)
        
        # 副标题
        subtitle_label = tk.Label(header_frame,
                                 text="管理系统中的家具类型分类信息",
                                 font=('Microsoft YaHei UI', 12),
                                 fg='white',
                                 bg=GUIUtils.COLORS['info'])
        subtitle_label.pack()
    
    def create_form(self, parent):
        """创建现代化表单"""
        # 表单字段
        form_container = tk.Frame(parent, bg=GUIUtils.COLORS['surface'])
        form_container.pack(fill="both", expand=True)
        
        # 类型编码
        self.type_code_entry = GUIUtils.create_labeled_entry(
            form_container, "类型编码*:", 0, width=25)
        
        # 类型名称
        self.type_name_entry = GUIUtils.create_labeled_entry(
            form_container, "类型名称*:", 1, width=25)
        
        # 描述
        desc_label = tk.Label(form_container, text="类型描述:",
                             font=('Microsoft YaHei UI', 10),
                             bg=GUIUtils.COLORS['surface'])
        desc_label.grid(row=2, column=0, sticky="nw", padx=5, pady=8)
        
        self.description_text = tk.Text(form_container, width=28, height=4,
                                       font=('Microsoft YaHei UI', 10),
                                       bg='white', relief='solid', bd=1)
        self.description_text.grid(row=2, column=1, padx=5, pady=8, sticky="ew")
        
        # 按钮区域
        button_frame = tk.Frame(form_container, bg=GUIUtils.COLORS['surface'])
        button_frame.grid(row=3, column=0, columnspan=2, pady=20, sticky="ew")
        
        # 操作按钮
        btn_add = GUIUtils.create_modern_button(button_frame, "➕ 添加", 
                                               self.add_type, "success", 12)
        btn_add.pack(side="top", pady=5, fill="x")
        
        btn_update = GUIUtils.create_modern_button(button_frame, "✏️ 修改", 
                                                  self.update_type, "warning", 12)
        btn_update.pack(side="top", pady=5, fill="x")
        
        btn_delete = GUIUtils.create_modern_button(button_frame, "🗑️ 删除", 
                                                  self.delete_type, "danger", 12)
        btn_delete.pack(side="top", pady=5, fill="x")
        
        btn_clear = GUIUtils.create_modern_button(button_frame, "🔄 清空", 
                                                 self.clear_inputs, "primary", 12)
        btn_clear.pack(side="top", pady=5, fill="x")
        
        # 配置网格权重
        form_container.grid_columnconfigure(1, weight=1)
    
    def create_data_area(self, parent):
        """创建数据展示区域"""
        # 搜索区域
        search_frame, self.search_var = GUIUtils.create_search_frame(parent, self.search_data)
        search_frame.pack(fill="x", pady=(0, 15))
        
        # 数据表格
        columns = ("type_code", "type_name", "description", "created_at")
        headings = ("类型编码", "类型名称", "描述", "创建时间")
        
        tree_frame, self.tree = GUIUtils.create_modern_treeview(parent, columns, headings, 15)
        tree_frame.pack(fill="both", expand=True)
        
        # 绑定选择事件
        self.tree.bind("<<TreeviewSelect>>", self.on_item_select)
        
        # 导出按钮和统计信息
        bottom_frame = tk.Frame(parent, bg=GUIUtils.COLORS['surface'])
        bottom_frame.pack(fill="x", pady=(15, 0))
        
        # 统计信息
        self.stats_label = tk.Label(bottom_frame, text="",
                                   font=('Microsoft YaHei UI', 10),
                                   fg=GUIUtils.COLORS['text_secondary'],
                                   bg=GUIUtils.COLORS['surface'])
        self.stats_label.pack(side="left")
        
        # 导出按钮
        btn_export = GUIUtils.create_modern_button(bottom_frame, "📤 导出Excel", 
                                                  self.export_data, "success", 15)
        btn_export.pack(side="right")
    
    def search_data(self, keyword=""):
        """搜索数据"""
        try:
            # 清空表格
            GUIUtils.clear_treeview(self.tree)
            
            # 获取数据
            if keyword.strip():
                # 搜索包含关键词的记录
                types = []
                all_types = self.furniture_type.get_all_types()
                for t in all_types:
                    if (keyword.lower() in t.get("type_code", "").lower() or 
                        keyword.lower() in t.get("type_name", "").lower() or
                        keyword.lower() in t.get("description", "").lower()):
                        types.append(t)
            else:
                types = self.furniture_type.get_all_types()
            
            # 插入数据
            for furniture_type in types:
                self.tree.insert("", "end", values=(
                    furniture_type.get("type_code", ""),
                    furniture_type.get("type_name", ""),
                    furniture_type.get("description", "")[:30] + "..." if len(str(furniture_type.get("description", ""))) > 30 else furniture_type.get("description", ""),
                    GUIUtils.format_datetime(furniture_type.get("created_at", ""))
                ))
            
            # 更新统计信息
            search_text = f" (搜索: {keyword})" if keyword.strip() else ""
            self.update_stats(len(types), search_text)
            
        except Exception as e:
            GUIUtils.show_error(f"搜索失败: {e}")
    
    def update_stats(self, count, extra_text=""):
        """更新统计信息"""
        stats_text = f"📊 共 {count} 条记录{extra_text}"
        self.stats_label.config(text=stats_text)
    
    def export_data(self):
        """导出数据"""
        try:
            # 获取所有数据
            types = self.furniture_type.get_all_types()
            
            if not types:
                GUIUtils.show_warning("没有数据可导出")
                return
            
            # 准备导出数据
            headers = ["类型编码", "类型名称", "描述", "创建时间"]
            data = []
            
            for furniture_type in types:
                data.append([
                    furniture_type.get("type_code", ""),
                    furniture_type.get("type_name", ""),
                    furniture_type.get("description", ""),
                    GUIUtils.format_datetime(furniture_type.get("created_at", ""))
                ])
            
            # 导出到CSV
            if GUIUtils.export_to_csv(data, headers, "家具类型"):
                self.load_data()  # 刷新界面
                
        except Exception as e:
            GUIUtils.show_error(f"导出失败: {e}")
    
    def add_type(self):
        """添加家具类型"""
        # 验证输入
        if not GUIUtils.validate_not_empty(
            [self.type_code_entry, self.type_name_entry],
            ["类型编码", "类型名称"]):
            return
        
        try:
            # 获取输入值
            type_code = self.type_code_entry.get().strip()
            type_name = self.type_name_entry.get().strip()
            description = self.description_text.get(1.0, tk.END).strip()
            
            # 检查编码是否已存在
            if self.furniture_type.find_one({"type_code": type_code}):
                GUIUtils.show_error("类型编码已存在")
                return
            
            # 添加类型
            self.furniture_type.create_type(type_code, type_name, description)
            GUIUtils.show_success("家具类型添加成功")
            
            # 刷新列表
            self.load_data()
            self.clear_inputs()
            
        except Exception as e:
            GUIUtils.show_error(f"添加失败: {e}")
    
    def update_type(self):
        """修改家具类型"""
        selected_item = self.tree.selection()
        if not selected_item:
            GUIUtils.show_warning("请选择要修改的家具类型")
            return
        
        # 验证输入
        if not GUIUtils.validate_not_empty(
            [self.type_code_entry, self.type_name_entry],
            ["类型编码", "类型名称"]):
            return
        
        try:
            # 获取选中项的原始编码
            original_code = self.tree.item(selected_item[0])["values"][0]
            
            # 获取输入值
            type_code = self.type_code_entry.get().strip()
            type_name = self.type_name_entry.get().strip()
            description = self.description_text.get(1.0, tk.END).strip()
            
            # 如果编码有变化，检查新编码是否已存在
            if type_code != original_code:
                if self.furniture_type.find_one({"type_code": type_code}):
                    GUIUtils.show_error("新的类型编码已存在")
                    return
            
            # 更新类型
            update_data = {
                "type_code": type_code,
                "type_name": type_name,
                "description": description
            }
            self.furniture_type.update({"type_code": original_code}, update_data)
            GUIUtils.show_success("家具类型修改成功")
            
            # 刷新列表
            self.load_data()
            self.clear_inputs()
            
        except Exception as e:
            GUIUtils.show_error(f"修改失败: {e}")
    
    def delete_type(self):
        """删除家具类型"""
        selected_item = self.tree.selection()
        if not selected_item:
            GUIUtils.show_warning("请选择要删除的家具类型")
            return
        
        if not GUIUtils.confirm("确定要删除选中的家具类型吗？"):
            return
        
        try:
            # 获取选中项的编码
            type_code = self.tree.item(selected_item[0])["values"][0]
            
            # 删除类型
            self.furniture_type.delete({"type_code": type_code})
            GUIUtils.show_success("家具类型删除成功")
            
            # 刷新列表
            self.load_data()
            self.clear_inputs()
            
        except Exception as e:
            GUIUtils.show_error(f"删除失败: {e}")
    
    def clear_inputs(self):
        """清空输入框"""
        self.type_code_entry.delete(0, tk.END)
        self.type_name_entry.delete(0, tk.END)
        self.description_text.delete(1.0, tk.END)
        
        # 清空搜索框
        if hasattr(self, 'search_var'):
            self.search_var.set("")
    
    def load_data(self):
        """加载数据到列表"""
        try:
            # 清空现有数据
            GUIUtils.clear_treeview(self.tree)
            
            # 获取所有家具类型
            types = self.furniture_type.get_all_types()
            
            # 添加到列表
            for type_info in types:
                values = (
                    type_info.get("type_code", ""),
                    type_info.get("type_name", ""),
                    type_info.get("description", "")[:30] + "..." if len(str(type_info.get("description", ""))) > 30 else type_info.get("description", ""),
                    GUIUtils.format_datetime(type_info.get("created_at", ""))
                )
                self.tree.insert("", "end", values=values)
            
            # 更新统计信息
            if hasattr(self, 'update_stats'):
                self.update_stats(len(types))
                
        except Exception as e:
            GUIUtils.show_error(f"加载数据失败: {e}")
    
    def on_item_select(self, event):
        """列表项选择事件"""
        selected_item = self.tree.selection()
        if selected_item:
            values = self.tree.item(selected_item[0])["values"]
            
            # 清空并填充输入框
            self.type_code_entry.delete(0, tk.END)
            self.type_name_entry.delete(0, tk.END)
            self.description_text.delete(1.0, tk.END)
            
            self.type_code_entry.insert(0, values[0])
            self.type_name_entry.insert(0, values[1])
            
            # 获取完整描述信息（因为表格中可能被截断）
            try:
                full_data = self.furniture_type.find_one({"type_code": values[0]})
                if full_data:
                    self.description_text.insert(1.0, full_data.get("description", ""))
                else:
                    self.description_text.insert(1.0, values[2])
            except Exception:
                self.description_text.insert(1.0, values[2]) 