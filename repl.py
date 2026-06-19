from interpreter import Interpreter

def start_repl():
    interp = Interpreter()
    print("May（五月）v0.1")
    while True:
        try:
            line = input(">>> ")
            if line.strip() == "exit":
                break
            interp.run(line)
        except Exception as e:
            print("错误:", e)