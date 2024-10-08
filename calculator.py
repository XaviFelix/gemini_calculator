from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QGridLayout,
    QPushButton,
    QLabel
)
import google.generativeai as genai

class Calculator(QWidget):
    def __init__(self):
        super().__init__()

        # Store api key in a constant
        SECRET = "AISUPER_FAKE_UnSA5-Fake_KEY-wAZ8PmaS"

        # The prompt sent to gemin AI
        self.gen_prompt = """
            Evaluate the following mathematical expression.
            Provide only numerical answers.
            If not a whole number then do not exceed 4 decimal places.
            Here's the format of what I want to see:
            Steps:
            Answer:
            """
        
        # Configure and instantiate the AI using my api key and model
        genai.configure(api_key=SECRET)
        self.model = genai.GenerativeModel("gemini-1.5-flash")

        # Window title and fixed sizing 
        self.setWindowTitle("Calculator")
        self.setFixedSize(QSize(450, 350))

        # Vbox (MAIN LAYOUT)
        self.vbox_main = QVBoxLayout()

        # GridBox (layout for Calculator buttons)
        self.gridbox = QGridLayout()

        # Display string
        self.expression_display = QLabel("")
        self.display = QLabel("")
        self.display.setStyleSheet("font-size: 40px;")

        # List of calculator buttons
        buttons = [
            'e', 'C', '(', ')', '^',
            'sin', '7', '8', '9', '/',
            'cos', '4', '5', '6', '*',
            'tan', '1', '2', '3', '-',
            'log', '.', '0', '=', '+'
        ]

        # Calculating button positions for my gridlaoyt using list comprehension
        btn_positions = [(i, j) for i in range(5) for j in range(5)]

        # Adding buttons to the grid layout and connect each button to the update_display function
        for position, button_text in zip(btn_positions, buttons):
            btn = QPushButton(button_text)
            btn.clicked.connect(lambda checked, text=button_text: self.update_display(text))
            self.gridbox.addWidget(btn, *position, alignment=Qt.AlignmentFlag.AlignBaseline)

        # Add both my gridlayout and display to the VBox main
        self.vbox_main.addWidget(self.expression_display, alignment=Qt.AlignmentFlag.AlignRight)
        self.vbox_main.addWidget(self.display, alignment=Qt.AlignmentFlag.AlignRight)
        self.vbox_main.addLayout(self.gridbox)

        self.setLayout(self.vbox_main)

    # String manipulation to extract answer
    def extract_answer(self, ai_response):
        answer = ai_response.split('\n')[-1]
        answer = answer.split(" ")[-1]
        return answer

    # For every button press, update the display
    def update_display(self, text):
        # Clear display if 'C' is pressed
        if text == 'C':
            self.display.setText("")
            self.expression_display.setText("")

        # Sends mathematical expression to ai model
        elif text == '=':
            expression = self.display.text()
            self.expression_display.setText(expression)
            response = self.model.generate_content(self.gen_prompt + self.display.text())
            answer = self.extract_answer(response.text.strip())
            
            self.display.setText(answer)

        # button dosn't fit my calculator layout (discontinued)
        '''
        elif text == 'back':
            current_text = self.display.text()
            backspace_text = current_text[:-1]
            self.display.setText(backspace_text)
        '''

        # Append the pressed button's text to the display
        else:
            current_text = self.display.text()
            self.display.setText(current_text + text)

# Show app
if __name__ == "__main__":
    app = QApplication([])
    calculator = Calculator()
    calculator.show()
    app.exec()
