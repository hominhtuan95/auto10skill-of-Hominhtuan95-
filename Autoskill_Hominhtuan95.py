        self.refresh()

    def toggle_f1(self, event=None):
        if self.closing:
            return 'break'
        if self.running:
            self.stop()
        else:
            self.start()
        return 'break'

    def refresh(self):
        previous = self.hwnd
        found = []
        callback_type = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)

        @callback_type
        def callback(hwnd, _):
            if user32.IsWindowVisible(hwnd):
                n = user32.GetWindowTextLengthW(hwnd)
                if n > 0:
                    buf = ctypes.create_unicode_buffer(n + 1)
                    user32.GetWindowTextW(hwnd, buf, n + 1)
                    title = buf.value
                    if 'chien quoc' in title.casefold() or 'chiến quốc' in title.casefold():
                        found.append((int(hwnd), title))
            return True

        user32.EnumWindows(callback, None)
        self.hwnds = found
        self.selector['values'] = [f'{hwnd} | {title[:32]}' for hwnd, title in found]
        if found:
            chosen = next((i for i, item in enumerate(found) if item[0] == previous), 0)
            self.selector.current(chosen)
        else:
            self.choice.set('Không thấy cửa sổ Chiến Quốc')

    def start(self):
        if self.running or self.closing:
            return
        idx = self.selector.current()
        if idx < 0 or idx >= len(self.hwnds):
            messagebox.showwarning('Chưa chọn game', 'Mở game và nhấn nút làm mới.', parent=self.root)
            return
        try:
            values = [int(v.get().strip()) for v in self.ms]
            if any(not MIN_DELAY_MS <= v <= MAX_DELAY_MS for v in values):
                raise ValueError
        except ValueError:
            messagebox.showerror('Sai thời gian', 'Nhập thời gian 50–180000 ms.', parent=self.root)
            return
        enabled = [v.get() for v in self.vars]
        if not any(enabled):
            messagebox.showwarning('Chưa chọn phím', 'Hãy bật ít nhất một phím.', parent=self.root)
            return
        hwnd = self.hwnds[idx][0]
        if not user32.IsWindow(hwnd):
            messagebox.showwarning('Cửa sổ không tồn tại', 'Làm mới danh sách game.', parent=self.root)
            return
        self.hwnd = hwnd
        self.stop_event = threading.Event()
        self.running = True
        self.status.set(f'Đang chạy | HWND {hwnd}')
        threading.Thread(target=self.worker,
                         args=(hwnd, [v / 1000 for v in values], enabled, self.stop_event),
                         daemon=True).start()

    def stop(self):
        if self.stop_event is not None:
            self.stop_event.set()
        self.running = False
        if not self.closing:
            self.status.set('Dừng | F1 khi chọn cửa sổ Auto')

    def worker(self, hwnd, delays, enabled, stop_event):
        due = [time.monotonic() + i * 0.04 for i in range(len(VKS))]
        while not stop_event.is_set():
            if not user32.IsWindow(hwnd):
                self.root.after(0, self.window_closed, stop_event)
                return
            now = time.monotonic()
            for i, vk in enumerate(VKS):
                if stop_event.is_set():
                    return
                if enabled[i] and now >= due[i]:
                    # Best effort: games using DirectInput/raw input may ignore PostMessage.
                    user32.PostMessageW(hwnd, WM_KEYDOWN, vk, 0)
                    if stop_event.wait(0.025):
                        user32.PostMessageW(hwnd, WM_KEYUP, vk, 0)
                        return
                    user32.PostMessageW(hwnd, WM_KEYUP, vk, 0)
                    due[i] = time.monotonic() + delays[i]
            stop_event.wait(0.02)

    def window_closed(self, stop_event):
        if self.closing or self.stop_event is not stop_event:
            return
        self.stop()
        self.status.set('Cửa sổ game đã đóng')

    def close(self):
        self.closing = True
        self.stop()
        self.root.destroy()


def main():
    root = tk.Tk()
    root.withdraw()
    if not licensed(root):
        root.destroy()
        return
    root.deiconify()
    AutoSkill(root)
    root.mainloop()


if __name__ == '__main__':
    main()
