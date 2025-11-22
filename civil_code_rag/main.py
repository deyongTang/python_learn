from graph import build_graph
import sys

def main():
    print("正在初始化民法典问答助手...")
    try:
        app = build_graph()
    except Exception as e:
        print(f"初始化失败: {e}")
        print("请检查是否已正确配置 .env 文件及 API 密钥。")
        return

    print("\n初始化完成！您可以开始提问了。")
    print("输入 'q' 或 'quit' 退出程序。\n")

    while True:
        try:
            question = input("请输入您的问题: ")
            if question.lower() in ["q", "quit", "exit"]:
                print("再见！")
                break
            
            if not question.strip():
                continue

            print("\n正在思考中...\n")
            
            # Invoke the graph
            inputs = {"question": question}
            result = app.invoke(inputs)
            
            print("-" * 50)
            print(f"回答: {result['generation']}")
            print("-" * 50)
            print("\n")
            
        except KeyboardInterrupt:
            print("\n再见！")
            break
        except Exception as e:
            print(f"\n发生错误: {e}")

if __name__ == "__main__":
    main()
