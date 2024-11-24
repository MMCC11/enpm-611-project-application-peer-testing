import unittest
from unittest.mock import MagicMock, patch
from io import StringIO
from analysis.reopened_issue_analysis import ReopenedIssueAnalysis
from models.model import Issue


class TestReopenedIssueAnalysis(unittest.TestCase):
    def mock_event(self, event_type):
        """Mock an Event object with a specific event_type."""
        mock_event = MagicMock()
        mock_event.event_type = event_type
        return mock_event

    def mock_issues(self):
        """Mock multiple issues with varying labels and events."""
        issue1 = Issue()
        issue1.number = 1
        issue1.title = "Test Issue 1"
        issue1.labels = ["kind/bug"]
        issue1.events = [self.mock_event("closed"), self.mock_event("reopened")]

        issue2 = Issue()
        issue2.number = 2
        issue2.title = "Test Issue 2"
        issue2.labels = ["kind/feature"]
        issue2.events = [self.mock_event("closed")]

        issue3 = Issue()
        issue3.number = 3
        issue3.title = "Test Issue 3"
        issue3.labels = ["kind/bug", "status/triage"]
        issue3.events = [
            self.mock_event("closed"),
            self.mock_event("reopened"),
            self.mock_event("closed"),
            self.mock_event("reopened"),
        ]

        return [issue1, issue2, issue3]

    def mock_data_loader(self, mock_issues):
        """Mock the DataLoader to return a predefined set of issues."""
        mock_loader = MagicMock()
        mock_loader.get_issues.return_value = mock_issues
        return mock_loader

    def test_reopened_issue_analysis_empty_data_loader(self):
        mock_loader = MagicMock()
        mock_loader.get_issues.return_value = []
        with patch("data.data_loader.DataLoader.get_issues", mock_loader.get_issues):
            analysis = ReopenedIssueAnalysis()
            analysis.run()

        self.assertEqual(analysis.reopened_issues_count, 0)
        self.assertEqual(len(analysis.reopened_issues_details), 0)

    def test_reopened_issue_analysis_run(self):
        mock_issues = self.mock_issues()
        mock_loader = self.mock_data_loader(mock_issues)
        with patch("data.data_loader.DataLoader.get_issues", mock_loader.get_issues):
            analysis = ReopenedIssueAnalysis()
            analysis.run()

        self.assertEqual(analysis.reopened_issues_count, 2)
        self.assertEqual(len(analysis.reopened_issues_details), 2)

    def test_reopened_issue_analysis_output(self):
        mock_issues = self.mock_issues()
        mock_loader = self.mock_data_loader(mock_issues)
        with patch("data.data_loader.DataLoader.get_issues", mock_loader.get_issues):
            analysis = ReopenedIssueAnalysis()
            captured_output = StringIO()
            with patch("sys.stdout", new=captured_output):
                analysis.run()

        output = captured_output.getvalue()
        self.assertIn("Total issues that were reopened after closing: 2", output)
        self.assertIn("Test Issue 1", output)
        self.assertIn("Test Issue 3", output)
        self.assertNotIn("Test Issue 2", output)

    def test_reopened_issue_analysis_fewer_than_five_labels(self):
        mock_issues = self.mock_issues()
        mock_loader = self.mock_data_loader(mock_issues)
        with patch("data.data_loader.DataLoader.get_issues", mock_loader.get_issues):
            analysis = ReopenedIssueAnalysis()
            analysis.run()

        # Verify that the plot does not fail for fewer than 5 labels
        self.assertLessEqual(len(analysis.reopened_issues_details), len(mock_issues))

    def test_reopened_issue_analysis_no_labels(self):
        issue_no_labels = Issue()
        issue_no_labels.number = 4
        issue_no_labels.title = "Test Issue No Labels"
        issue_no_labels.labels = []
        issue_no_labels.events = [self.mock_event("closed"), self.mock_event("reopened")]

        mock_loader = self.mock_data_loader([issue_no_labels])
        with patch("data.data_loader.DataLoader.get_issues", mock_loader.get_issues):
            analysis = ReopenedIssueAnalysis()
            analysis.run()

        self.assertEqual(analysis.reopened_issues_count, 1)
        self.assertEqual(len(analysis.reopened_issues_details[0]["labels"]), 0)

    def test_reopened_issue_analysis_large_dataset(self):
        mock_issues = self.mock_issues() * 500  # Simulate a large dataset
        mock_loader = self.mock_data_loader(mock_issues)
        with patch("data.data_loader.DataLoader.get_issues", mock_loader.get_issues):
            analysis = ReopenedIssueAnalysis()
            analysis.run()

        self.assertEqual(analysis.reopened_issues_count, 1000)
        self.assertEqual(len(analysis.reopened_issues_details), 1000)


if __name__ == "__main__":
    unittest.main()
