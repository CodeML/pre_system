import http.server
import socketserver
import os
import sys

# 设置文档目录
DOC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "api")
PORT = 8080

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DOC_DIR, **kwargs)

def run_server():
    if not os.path.exists(DOC_DIR):
        print(f"错误: 找不到目录 {DOC_DIR}")
        return

    handler_object = MyHttpRequestHandler

    print("-" * 50)
    print(f"PRE 系统 API 文档本地服务已启动!")
    print(f"请在浏览器中访问: http://localhost:{PORT}")
    print(f"主索引文件: http://localhost:{PORT}/API_DOCUMENTATION_INDEX.md")
    print("-" * 50)
    print("\n提示: 如果你的浏览器不能直接渲染 Markdown，建议安装 'Markdown Viewer' 插件")
    print("或者运行后端服务后访问 Swagger UI: http://localhost:8000/docs")
    print("-" * 50)

    try:
        with socketserver.TCPServer(("", PORT), handler_object) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n服务已停止。")
        sys.exit(0)
    except Exception as e:
        print(f"启动失败: {e}")

if __name__ == "__main__":
    run_server()
