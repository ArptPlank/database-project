@echo off
chcp 65001 > nul
echo 📄 Markdown到Word转换工具
echo ================================

REM 激活conda环境
if exist "D:\ANACONDA\Scripts\activate.bat" (
    call "D:\ANACONDA\Scripts\activate.bat" db
) else (
    echo ⚠️  未找到conda环境，使用系统Python
)

REM 检查Python是否可用
python --version > nul 2>&1
if errorlevel 1 (
    echo ❌ Python未安装或未在PATH中
    pause
    exit /b 1
)

echo 🔍 检查依赖包...
pip show python-docx > nul 2>&1
if errorlevel 1 (
    echo 📦 安装python-docx...
    pip install python-docx
)

pip show markdown > nul 2>&1
if errorlevel 1 (
    echo 📦 安装markdown...
    pip install markdown
)

echo.
echo 🚀 开始转换...
python convert_md_to_doc.py

echo.
echo ✅ 转换完成！
echo 生成的文件：完整数据库课程设计报告.docx
echo.
pause 