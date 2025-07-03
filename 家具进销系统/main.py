"""
家具城进销存管理系统主入口
"""
import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

print("正在启动家具城进销存管理系统...")
print("正在导入模块...")

try:
    from main_window import MainWindow
    print("✓ 模块导入成功")
except ImportError as e:
    print(f"导入模块失败: {e}")
    print("请确保已安装所有必要的依赖包")
    print("运行: pip install -r requirements.txt")
    input("按回车键退出...")
    sys.exit(1)
except Exception as e:
    print(f"导入时发生未知错误: {e}")
    import traceback
    traceback.print_exc()
    input("按回车键退出...")
    sys.exit(1)

def main():
    """主函数"""
    try:
        print("正在创建主窗口...")
        # 创建并运行主窗口
        app = MainWindow()
        print("✓ 主窗口创建成功")
        print("正在启动GUI界面...")
        app.run()
        print("GUI界面已关闭")
    except Exception as e:
        print(f"程序运行出错: {e}")
        import traceback
        traceback.print_exc()
        input("按回车键退出...")

if __name__ == "__main__":
    main() 