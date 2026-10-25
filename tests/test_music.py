"""Регрессионные тесты для команд ADD, REM, PRINT (вариант 18)."""

import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from models import Song, Symphony
from processor import CommandProcessor


class MusicalWorkTests(unittest.TestCase):
    """Проверки предметной модели."""

    def test_song_type_and_author(self) -> None:
        work = Song("Кукушка", 4.25, "Кино")
        self.assertEqual((work.get_type(), work.get_author()), ("SONG", "Кино"))

    def test_symphony_type_and_author(self) -> None:
        work = Symphony("№5", 31.2, "Бетховен")
        self.assertEqual((work.get_type(), work.get_author()), ("SYMPHONY", "Бетховен"))

    def test_duration_comparisons(self) -> None:
        work = Song("Кукушка", 4.25, "Кино")
        cases = [("<", "5", True), (">=", "4.25", True),
                 ("==", "4.25", True), ("!=", "4.25", False),
                 ("<", "2", False), (">", "abc", False),
                 ("???", "3", False)]
        for comparison, value, expected in cases:
            with self.subTest(comparison=comparison, value=value):
                self.assertEqual(work.matches("duration", comparison, value), expected)

    def test_text_matching(self) -> None:
        work = Song("Кукушка", 4.25, "Кино")
        self.assertTrue(work.matches("name", "==", "Кукушка"))
        self.assertTrue(work.matches("author", "!=", "Сплин"))
        self.assertTrue(work.matches("type", "==", "SONG"))
        self.assertFalse(work.matches("genre", "==", "rock"))
        self.assertFalse(work.matches("name", ">", "А"))


class CommandProcessorTests(unittest.TestCase):
    """Проверки интерфейса обработки текстовых команд."""

    def setUp(self) -> None:
        self.processor = CommandProcessor()
        self.output = io.StringIO()

    def run_commands(self, *commands: str) -> str:
        with redirect_stdout(self.output):
            for command in commands:
                self.processor.process_command(command)
        return self.output.getvalue()

    def test_add_song_and_symphony(self) -> None:
        self.run_commands('ADD SONG "Группа крови" 4.45 "Кино"',
                          'ADD SYMPHONY "Симфония №40" 25.3 "Моцарт"')
        self.assertEqual(len(self.processor.works), 2)
        self.assertIsInstance(self.processor.works[0], Song)
        self.assertIsInstance(self.processor.works[1], Symphony)

    def test_remove_by_duration(self) -> None:
        self.run_commands('ADD SONG "Кукушка" 4.25 "Кино"',
                          'ADD SYMPHONY "Симфония №5" 31.2 "Бетховен"',
                          'REM duration > 30')
        self.assertEqual([work.name for work in self.processor.works], ["Кукушка"])

    def test_remove_by_author(self) -> None:
        self.run_commands('ADD SONG "Кукушка" 4.25 "Кино"',
                          'ADD SONG "Романс" 3.02 "Сплин"',
                          'REM author == "Кино"')
        self.assertEqual([work.name for work in self.processor.works], ["Романс"])

    def test_print_outputs_properties(self) -> None:
        output = self.run_commands('ADD SONG "Кукушка" 4.25 "Кино"', "PRINT")
        for value in ["Кукушка", "Исполнитель: Кино", "4.25"]:
            self.assertIn(value, output)

    def test_malformed_quoted_commands_not_crash(self) -> None:
        output = self.run_commands('ADD SONG "Незакрытые кавычки 4.25 Кино',
                                   'REM name == "Незакрытые кавычки')
        self.assertIn("Ошибка синтаксиса ADD", output)
        self.assertIn("Ошибка синтаксиса REM", output)
        self.assertEqual(self.processor.works, [])

    def test_missing_file(self) -> None:
        with redirect_stdout(self.output):
            self.processor.process_file("nonexistent-commands-unique.txt")
        self.assertIn("не найден", self.output.getvalue())

    def test_read_file_with_comments(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            file_path = Path(directory) / "sample.txt"
            file_path.write_text('# comment\n\nADD SONG "Кукушка" 4.25 "Кино"\n', encoding='utf-8')
            with redirect_stdout(self.output):
                self.processor.process_file(str(file_path))
        self.assertEqual(len(self.processor.works), 1)

    def test_unknown_command_or_type(self) -> None:
        output = self.run_commands('ADD OPERA "Кармен" 100 "Бизе"', "UNKNOWN")
        self.assertIn("Неизвестный тип произведения", output)
        self.assertIn("Неизвестная команда", output)

    def test_invalid_duration(self) -> None:
        output = self.run_commands('ADD SONG "Кукушка" bad "Кино"')
        self.assertIn("длительность должна быть числом", output)
        self.assertFalse(self.processor.works)


if __name__ == "__main__":
    unittest.main()
