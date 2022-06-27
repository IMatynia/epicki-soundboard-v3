from src.hotkey_scanner import HotkeyScanner

if __name__ == "__main__":
    def callback(keys):
        print("Scanned keys:", [str(key) for key in keys])

    print("Key scanner activated!")
    scanner = HotkeyScanner(callback)
    scanner.start()
    scanner.await_completion()
