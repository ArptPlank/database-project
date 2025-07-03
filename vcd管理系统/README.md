# 音像店VCD管理系统

一个功能完整的音像店VCD零售与出租管理系统，使用Flask + MongoDB开发。

## 📋 功能特性

### 核心功能
- ✅ **VCD信息管理** - 添加、编辑、删除VCD基本信息
- ✅ **库存管理** - 入库操作、库存查询、自动库存预警
- ✅ **销售管理** - VCD零售、自动库存扣减、销售记录
- ✅ **借还管理** - VCD借出、归还、租金计算
- ✅ **统计报表** - 销售统计、借还统计、图表展示
- ✅ **数据备份** - 数据备份与恢复功能

### 技术特性
- 🔄 **自动触发器** - 销售和借还时自动更新库存
- 📊 **聚合统计** - 基于MongoDB聚合管道的高效统计
- 📈 **可视化图表** - 使用Chart.js展示统计数据
- 💾 **数据安全** - 完善的数据备份恢复机制
- 📱 **响应式设计** - 支持移动端访问

## 🛠️ 技术栈

- **后端**: Python 3.9 + Flask
- **数据库**: MongoDB
- **前端**: HTML5 + CSS3 + JavaScript + Bootstrap 5
- **图表**: Chart.js
- **图标**: Font Awesome

## 📦 环境要求

- Python 3.9+
- MongoDB 4.0+
- Conda (用于环境管理)

## 🚀 快速开始

### 1. 创建开发环境

```bash
# 创建conda环境
conda create -n db python=3.9 -y

# 激活环境
conda activate db
```

### 2. 安装依赖

```bash
# 安装Python依赖包
pip install -r requirements.txt
```

### 3. 启动MongoDB

确保MongoDB服务正在运行：

```bash
# Windows
net start MongoDB

# Linux/macOS
sudo systemctl start mongod
```

### 4. 运行应用

```bash
python app.py
```

应用将在 http://localhost:5000 上运行。

## 📁 项目结构

```
数据库课设/
├── app.py                 # 主应用文件
├── requirements.txt       # Python依赖包
├── README.md             # 项目说明文档
│
├── templates/            # HTML模板文件
│   ├── base.html         # 基础模板
│   ├── index.html        # 主页仪表板
│   ├── vcds.html         # VCD信息管理
│   ├── inventory.html    # 库存管理
│   ├── sales.html        # 销售管理
│   ├── rentals.html      # 借还管理
│   ├── statistics.html   # 统计报表
│   ├── backup.html       # 数据备份
│   └── tools.html        # 工具页面
│
├── static/               # 静态文件
│   ├── css/
│   │   └── style.css     # 自定义样式
│   └── js/
│       └── main.js       # 主JavaScript文件
│
├── docs/                 # 项目文档
│   ├── 数据库课程设计报告.md        # 主报告Markdown版本
│   ├── 数据库课程设计报告.docx      # 主报告Word版本
│   ├── 完整数据库课程设计报告.docx   # 完整报告Word版本
│   ├── 第三四章-概念逻辑设计.md     # 分章节文档
│   ├── 第七章-应用系统设计与实现.md  # 分章节文档
│   ├── 第九十章-测试与总结.md       # 分章节文档
│   └── 附录-完整报告.md             # 附录文档
│
└── tools/                # 文档转换工具
    ├── convert_md_to_doc.py        # Markdown转Word工具
    ├── convert_to_word.bat         # 批处理脚本
    ├── conversion_requirements.txt  # 转换工具依赖
    └── 转换工具使用说明.md          # 工具使用说明
```

## 💡 使用说明

### VCD信息管理
1. 访问"VCD管理"页面
2. 点击"添加VCD"按钮
3. 填写VCD详细信息（名称、类型、价格等）
4. 保存后会自动创建对应的库存记录

### 库存管理
1. 在"库存管理"页面查看所有VCD的库存状态
2. 使用"入库操作"功能增加库存
3. 系统会自动显示库存预警（缺货/库存不足）

### 销售操作
1. 在"销售管理"页面点击"新增销售"
2. 选择VCD和销售数量
3. 填写客户信息（可选）
4. 确认销售后系统会自动扣减库存

### 借还操作
1. **借出VCD**：
   - 在"借还管理"页面点击"借出VCD"
   - 选择VCD、数量，填写客户信息
   - 系统会自动计算日租金并扣减现货数量

2. **归还VCD**：
   - 点击"归还VCD"按钮
   - 输入客户电话查找借出记录
   - 确认归还，系统会显示应收租金

### 统计报表
1. 在"统计报表"页面选择时间范围
2. 查看销售和借还的详细统计数据
3. 可导出CSV格式的统计报表

### 数据备份
1. 在"数据备份"页面点击"创建备份"
2. 系统会生成包含所有数据的JSON备份文件
3. 可以通过"恢复数据"功能从备份文件恢复

## 🗄️ 数据库设计

### 集合结构

#### vcds (VCD信息)
```javascript
{
  _id: ObjectId,
  name: String,          // VCD名称
  type: String,          // 类型
  director: String,      // 导演
  actors: String,        // 主演
  sale_price: Number,    // 售价
  rental_price: Number,  // 日租金
  release_year: Number,  // 发行年份
  language: String,      // 语言
  duration: Number,      // 时长
  rating: String,        // 评级
  description: String,   // 简介
  created_at: Date,
  updated_at: Date
}
```

#### inventory (库存)
```javascript
{
  _id: ObjectId,
  vcd_id: ObjectId,         // 关联VCD ID
  vcd_name: String,         // VCD名称
  total_quantity: Number,   // 总库存
  available_quantity: Number, // 现货数量
  rented_quantity: Number,  // 借出数量
  sold_quantity: Number,    // 已售数量
  last_updated: Date
}
```

#### sales (销售记录)
```javascript
{
  _id: ObjectId,
  vcd_id: ObjectId,      // 关联VCD ID
  quantity: Number,      // 销售数量
  unit_price: Number,    // 单价
  customer_name: String, // 客户姓名
  customer_phone: String,// 客户电话
  sale_date: Date,       // 销售时间
  note: String          // 备注
}
```

#### rentals (借还记录)
```javascript
{
  _id: ObjectId,
  vcd_id: ObjectId,      // 关联VCD ID
  quantity: Number,      // 借出数量
  daily_rate: Number,    // 日租金
  customer_name: String, // 客户姓名
  customer_phone: String,// 客户电话
  rent_date: Date,       // 借出时间
  return_date: Date,     // 归还时间
  status: String,        // 状态 (rented/returned)
  note: String          // 备注
}
```

## 🔧 API接口

### VCD管理
- `GET /api/vcds` - 获取VCD列表
- `POST /api/vcds` - 添加VCD
- `PUT /api/vcds/<id>` - 更新VCD信息
- `DELETE /api/vcds/<id>` - 删除VCD

### 库存管理
- `GET /api/inventory` - 获取库存信息
- `POST /api/inventory/restock` - 入库操作

### 销售管理
- `GET /api/sales` - 获取销售记录
- `POST /api/sales` - 新增销售

### 借还管理
- `GET /api/rentals` - 获取借还记录
- `POST /api/rentals` - 借出/归还操作

### 统计报表
- `GET /api/statistics/sales` - 销售统计
- `GET /api/statistics/rentals` - 借还统计

### 数据备份
- `POST /api/backup` - 创建数据备份

## 🚨 注意事项

1. **数据库连接**：确保MongoDB服务正在运行且可连接
2. **端口占用**：默认使用5000端口，如有冲突请修改app.py中的端口设置
3. **数据备份**：建议定期备份数据，备份文件包含完整的系统数据
4. **浏览器兼容性**：推荐使用Chrome、Firefox等现代浏览器

## 🤝 贡献

欢迎提交Issue和Pull Request来改善这个项目。

## 📄 许可证

本项目仅用于学习和研究目的。

## 📞 支持

如有问题或建议，请提交Issue或联系开发者。 