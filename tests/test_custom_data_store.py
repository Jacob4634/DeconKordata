import sqlite3
import tempfile
import unittest
from contextlib import closing
from pathlib import Path

from decon_v3 import (
    calculate_optimal_values,
    initialize_database,
    load_custom_data,
    save_custom_data,
)


class CustomDataStoreTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.database_path = Path(self.temp_dir.name) / "decon.db"
        initialize_database(self.database_path)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_initializes_expected_table_and_composite_primary_key(self):
        with closing(sqlite3.connect(self.database_path)) as connection:
            columns = connection.execute("PRAGMA table_info(custom_data)").fetchall()

        self.assertEqual(
            [column[1] for column in columns],
            ["material", "machine", "series", "diameter", "rpm", "feed", "ap", "ae"],
        )
        self.assertEqual(
            [column[1] for column in sorted(columns, key=lambda item: item[5]) if column[5]],
            ["material", "machine", "series", "diameter"],
        )

    def test_saves_and_loads_values_for_exact_selection(self):
        values = {"rpm": 4200.0, "feed": 350.0, "ap": 4.5, "ae": 1.2}
        key = ("6082-T6", "Doosan DNM400", "S610", 8.0)

        save_custom_data(self.database_path, *key, values)

        self.assertEqual(load_custom_data(self.database_path, *key), values)
        self.assertIsNone(
            load_custom_data(
                self.database_path, "6082-T6", "Doosan DNM400", "S610", 10.0
            )
        )

    def test_saving_same_selection_updates_existing_values(self):
        key = ("6082-T6", "Doosan DNM400", "S610", 8.0)
        save_custom_data(
            self.database_path,
            *key,
            {"rpm": 4000, "feed": 300, "ap": 4, "ae": 1},
        )
        updated = {"rpm": 4500, "feed": 360, "ap": 5, "ae": 1.5}

        save_custom_data(self.database_path, *key, updated)

        self.assertEqual(load_custom_data(self.database_path, *key), updated)

    def test_blank_values_are_stored_as_null(self):
        key = ("6082-T6", "Doosan DNM400", "S610", 8.0)
        values = {"rpm": None, "feed": None, "ap": None, "ae": None}

        save_custom_data(self.database_path, *key, values)

        self.assertEqual(load_custom_data(self.database_path, *key), values)

    def test_optimal_rpm_is_capped_at_machine_maximum(self):
        rpm, feed = calculate_optimal_values(12000, 4000, 0.2, 3)

        self.assertEqual(rpm, 4000)
        self.assertEqual(feed, 2400)

    def test_optimal_rpm_keeps_recommendation_below_machine_maximum(self):
        rpm, feed = calculate_optimal_values(3000, 4000, 0.2, 3)

        self.assertEqual(rpm, 3000)
        self.assertEqual(feed, 1800)


if __name__ == "__main__":
    unittest.main()
