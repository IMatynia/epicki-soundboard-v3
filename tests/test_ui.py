from ui.dialog_add_edit_file import AddEditFileDialog
from src.audio_hotkey import AudioHotkey, AudioHotkeyList
from PySide2.QtWidgets import QApplication, QMainWindow


def test_add_edit_with_initial_hk():
    example = AudioHotkey(set(["a", "b", "shift"]), "bazinga.ogg", 1)
    ex_list = AudioHotkeyList()

    app = QApplication()
    main = QMainWindow(None)
    main.show()
    dialog = AddEditFileDialog(
        main,
        ex_list,
        1,
        set(["a", "b", "shift"]),
        "bazinga.ogg")
    dialog.show()
    
    if dialog.exec_():
        new = dialog.get_hotkey()
        assert new == example and new.get_filename() == example.get_filename()
    app.closeAllWindows()
