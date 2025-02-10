import flet as ft
import random


class TypingTrainer:
    def __init__(self):
        self.current_text = ""
        self.user_input = ""
        self.words = ["привет", "мир", "программирование", "компьютер", "клавиатура",
                      "разработка", "python", "тренировка", "печать", "практика"]

    def generate_text(self):
        return " ".join(random.sample(self.words, 3))


def main(page: ft.Page):
    page.title = "Тренажер слепой печати"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    trainer = TypingTrainer()

    # Создаем полную раскладку клавиатуры
    keyboard_layout = [
        "ёйцукенгшщзхъ",
        "фывапролджэ",
        "ячсмитьбю.",
        "    "  # пробел
    ]

    def create_keyboard():
        keyboard = ft.Column(spacing=5, alignment=ft.MainAxisAlignment.CENTER)
        for row in keyboard_layout:
            key_row = ft.Row(spacing=2, alignment=ft.MainAxisAlignment.CENTER)
            for key in row:
                if key == " ":
                    # Создаем широкую клавишу пробела
                    key_button = ft.Container(
                        content=ft.Text("ПРОБЕЛ", size=16),
                        width=200,
                        height=40,
                        alignment=ft.alignment.center,
                        bgcolor=ft.colors.BLUE_GREY_100,
                        border_radius=5,
                        border=ft.border.all(1, ft.colors.BLUE_GREY_300),
                    )
                else:
                    key_button = ft.Container(
                        content=ft.Text(key, size=20),
                        width=45,
                        height=45,
                        alignment=ft.alignment.center,
                        bgcolor=ft.colors.BLUE_GREY_100,
                        border_radius=5,
                        border=ft.border.all(1, ft.colors.BLUE_GREY_300),
                    )
                key_row.controls.append(key_button)
            keyboard.controls.append(key_row)
        return keyboard

    keyboard = create_keyboard()

    def update_keyboard(pressed_char=None, error_char=None):
        for row in keyboard.controls:
            for key_container in row.controls:
                key = key_container.content.value.lower()
                if key == "пробел":
                    key = " "

                if error_char and key == error_char.lower():
                    key_container.bgcolor = ft.colors.RED_200
                elif pressed_char and key == pressed_char.lower():
                    key_container.bgcolor = ft.colors.GREEN_200
                else:
                    key_container.bgcolor = ft.colors.BLUE_GREY_100
        page.update()

    def create_text_spans(text, input_text):
        spans = []
        for i, char in enumerate(text):
            if i < len(input_text):
                if input_text[i] == char:
                    spans.append(ft.TextSpan(
                        text=char,
                        style=ft.TextStyle(color=ft.colors.GREEN, size=24)
                    ))
                else:
                    spans.append(ft.TextSpan(
                        text=char,
                        style=ft.TextStyle(color=ft.colors.RED, weight=ft.FontWeight.BOLD, size=24)
                    ))
            else:
                spans.append(ft.TextSpan(
                    text=char,
                    style=ft.TextStyle(color=ft.colors.BLACK, size=24)
                ))
        return spans

    text_display = ft.Text(
        spans=[],
        size=24,
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER,
    )

    input_field = ft.TextField(
        label="Введите текст здесь",
        width=400,
        text_align=ft.TextAlign.CENTER,
    )

    result_text = ft.Text(
        size=16,
        color=ft.colors.GREEN,
    )

    def check_input(e):
        current_input = input_field.value
        if not current_input:
            update_keyboard()
            return

        if len(current_input) > len(trainer.current_text):
            input_field.value = current_input[:-1]
            page.update()
            return

        last_char = current_input[-1]
        current_position = len(current_input) - 1

        if current_position < len(trainer.current_text):
            expected_char = trainer.current_text[current_position]

            if last_char != expected_char:
                # Показываем ошибку
                update_keyboard(last_char, expected_char)
                input_field.value = current_input[:-1]
                result_text.value = f"Ошибка! Нужно нажать: {expected_char}"
                result_text.color = ft.colors.RED
                page.update()
                return
            else:
                # Показываем правильное нажатие
                update_keyboard(last_char)

        text_display.spans = create_text_spans(trainer.current_text, current_input)

        if current_input == trainer.current_text:
            result_text.value = "Отлично! Правильно!"
            result_text.color = ft.colors.GREEN
            page.update()
            new_text()
        else:
            result_text.value = "Продолжайте печатать..."
            result_text.color = ft.colors.ORANGE

        page.update()

    def new_text():
        trainer.current_text = trainer.generate_text()
        text_display.spans = create_text_spans(trainer.current_text, "")
        input_field.value = ""
        result_text.value = "Начните печатать..."
        result_text.color = ft.colors.BLACK
        update_keyboard()
        page.update()

    new_text_button = ft.ElevatedButton("Новый текст", on_click=lambda _: new_text())

    input_field.on_change = check_input

    # Создаем контейнер для клавиатуры с отступами
    keyboard_container = ft.Container(
        content=keyboard,
        margin=ft.margin.only(top=20, bottom=20),
        padding=10,
        border_radius=10,
        bgcolor=ft.colors.BLUE_GREY_50,
    )

    # Добавляем элементы на страницу
    page.add(
        ft.Column(
            [
                ft.Text("Тренажер слепой печати", size=30, weight=ft.FontWeight.BOLD),
                ft.Container(padding=10),
                text_display,
                ft.Container(padding=5),
                input_field,
                ft.Container(padding=5),
                result_text,
                keyboard_container,
                new_text_button,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

    new_text()


if __name__ == "__main__":
    ft.app(target=main)
