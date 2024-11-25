import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
from reopened_issue_analysis import ReopenedIssueAnalysis
from models.model import Issue


class TestReopenedIssueAnalysis(unittest.TestCase):
    @patch("reopened_issue_analysis.DataLoader.get_issues")
    def test_less_than_five_labels(self, mock_get_issues):
        """
        Test plot_reopened_issues with fewer than 5 labels.
        """
        # Mocking issues with fewer than 5 unique labels
        mock_issues = [
            Issue({
                "number": 1,
                "creator": "user1",
                "labels": ["bug"],
                "created_date": datetime(2024, 1, 1),
                "events": [
                    {"event_type": "closed", "author": "user1", "event_date": datetime(2024, 1, 10)}
                ]
            }),
            Issue({
                "number": 2,
                "creator": "user2",
                "labels": ["enhancement"],
                "created_date": datetime(2024, 2, 1),
                "events": [
                    {"event_type": "closed", "author": "user2", "event_date": datetime(2024, 2, 10)}
                ]
            }),
        ]
        mock_get_issues.return_value = mock_issues

        # Run analysis
        analysis = ReopenedIssueAnalysis()

        # Ensure no IndexError is raised
        try:
            analysis.run()
        except IndexError as e:
            self.fail(f"Unexpected IndexError: {e}")

    @patch("reopened_issue_analysis.DataLoader.get_issues")
    def test_reopened_issue_analysis_empty_data_loader(self, mock_get_issues):
        """
        Test the handling of an empty dataset.
        """
        mock_get_issues.return_value = []  # No issues

        analysis = ReopenedIssueAnalysis()

        # Ensure the method runs without raising errors
        try:
            analysis.run()
        except IndexError as e:
            self.fail(f"Unexpected IndexError: {e}")

    @patch("reopened_issue_analysis.DataLoader.get_issues")
    def test_reopened_issue_analysis_output(self, mock_get_issues):
        """
        Test plotting logic with a normal dataset.
        """
        mock_issues = [
            Issue({
                "number": 1,
                "creator": "user1",
                "labels": ["bug"],
                "created_date": datetime(2024, 1, 1),
                "events": [
                    {"event_type": "closed", "author": "user1", "event_date": datetime(2024, 1, 10)}
                ]
            }),
            Issue({
                "number": 2,
                "creator": "user2",
                "labels": ["enhancement"],
                "created_date": datetime(2024, 2, 1),
                "events": [
                    {"event_type": "closed", "author": "user2", "event_date": datetime(2024, 2, 10)}
                ]
            }),
            Issue({
                "number": 3,
                "creator": "user3",
                "labels": ["documentation"],
                "created_date": datetime(2023, 11, 15),
                "events": [
                    {"event_type": "closed", "author": "user3", "event_date": datetime(2023, 12, 15)}
                ]
            }),
        ]
        mock_get_issues.return_value = mock_issues

        analysis = ReopenedIssueAnalysis()

        # Run and validate that no IndexError occurs
        try:
            analysis.run()
        except IndexError as e:
            self.fail(f"Unexpected IndexError: {e}")


if __name__ == "__main__":
    unittest.main()
