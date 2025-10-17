from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel,
    QSpinBox, QMessageBox, QHBoxLayout, QProgressDialog
)
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QIcon
import subprocess
from pathlib import Path
import sys

class SimpleAIGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tetris AI")

        self.setWindowIcon(QIcon("tetris.ico"))
        self.resize(360, 180)

        # store selected training level (default 0)
        self.training_level = 0

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.show_main_menu()

    def show_main_menu(self):
        self.clear_layout(self.main_layout)

        btn1 = QPushButton("1. Train your AI")
        btn2 = QPushButton("2. Watch your AI play")
        btn3 = QPushButton("3. Play on your own")

        note_label = QLabel("(Note: Buttons 2 and 3 may take a couple of seconds to load)")
        note_label.setAlignment(Qt.AlignCenter)

        btn1.clicked.connect(self.on_train_clicked)
        btn2.clicked.connect(self.on_watch_clicked)
        btn3.clicked.connect(self.on_play_clicked)

        self.main_layout.addStretch()
        self.main_layout.addWidget(btn1)
        self.main_layout.addWidget(btn2)
        self.main_layout.addWidget(btn3)
        self.main_layout.addWidget(note_label)
        self.main_layout.addStretch()

    def on_train_clicked(self):
        self.clear_layout(self.main_layout)

        label = QLabel("Select a level to train your AI to (between 0 and 15): ")
        spin = QSpinBox()
        spin.setRange(0, 15)
        spin.setValue(self.training_level)

        start_btn = QPushButton("Start training")
        back_btn = QPushButton("Back")

        start_btn.clicked.connect(lambda: self._start_training(spin.value()))
        back_btn.clicked.connect(self.show_main_menu)

        controls = QHBoxLayout()
        controls.addWidget(spin)
        controls.addWidget(start_btn)
        controls.addWidget(back_btn)

        self.main_layout.addStretch()
        self.main_layout.addWidget(label)
        self.main_layout.addLayout(controls)
        self.main_layout.addStretch()

    def _start_training(self, value):
        self.training_level = int(value)

        if self.training_level == 0:
            duration_sec = float(.75) / 2.0
        else:    
            duration_sec = float(self.training_level) / 2.0
        interval_ms = 50
        total_steps = max(1, int(duration_sec * 1000 / interval_ms))

        progress = QProgressDialog("Training...", None, 0, total_steps, self)
        progress.setWindowTitle("Training")
        progress.setCancelButton(None)
        progress.setWindowModality(Qt.WindowModal)
        progress.setAutoClose(True)
        progress.setValue(0)
        progress.show()

        timer = QTimer(self)
        state = {"step": 0}

        def _tick():
            state["step"] += 1
            progress.setValue(state["step"])
            secs_left = max(0.0, duration_sec * (1 - state["step"] / total_steps))
            progress.setLabelText(f"Training... ({secs_left:.1f}s remaining)")
            if state["step"] >= total_steps:
                timer.stop()
                progress.close()
                QMessageBox.information(self, "Training complete", "Training complete!")
                self.show_main_menu()

        timer.timeout.connect(_tick)
        timer.start(interval_ms)

    def on_watch_clicked(self):
        self.watch_ai_play(self.training_level)

    def on_play_clicked(self):
        self.play_user()

    def watch_ai_play(self, training_level):
        try:
            if training_level < 3:
                out_start = training_level
            elif training_level >= 3 and training_level <= 7:
                out_start = 3 if training_level < 5 else 4
            elif training_level > 7 and training_level < 10:
                out_start = 5
            elif training_level == 10:
                out_start = 6
            elif training_level == 11 or training_level == 12:
                out_start == 7
            elif training_level == 13 or training_level == 14:
                out_start == 8
            else:
                out_start == 9

            self.launch_tetris_ai(mode="ai_player_watching", out_start=out_start)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to start AI watching: {e}")

    def launch_tetris_ai(self, mode="human_player", out_start=0, outer_max=0):
        script_path = Path(__file__).resolve().parent / "tetris_ai.py"
        if not script_path.exists():
            raise FileNotFoundError(f"{script_path} not found")
        if outer_max > 0:
            cmd = [
                sys.executable,
                str(script_path),
                "--mode", mode,
                "--out_start", str(int(out_start)),
                "--outer_max", str(int(outer_max))
            ]
        else:
            cmd = [
                sys.executable,
                str(script_path),
                "--mode", mode,
                "--out_start", str(int(out_start)),
            ]
        subprocess.Popen(cmd, cwd=str(script_path.parent))

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
            else:
                child_layout = item.layout()
                if child_layout is not None:
                    self.clear_layout(child_layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = SimpleAIGUI()
    win.show()
    sys.exit(app.exec())