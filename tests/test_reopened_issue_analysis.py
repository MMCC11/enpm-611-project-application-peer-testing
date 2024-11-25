import unittest
from unittest.mock import MagicMock, patch
from io import StringIO
from analysis.reopened_issue_analysis import ReopenedIssueAnalysis
from models.model import Issue, Event


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
        issue1.labels = ["bug", "backend", "priority_high", "documentation", "security", "performance"]
        issue1.events = [self.mock_event("closed"), self.mock_event("reopened")]

        issue2 = Issue()
        issue2.number = 2
        issue2.title = "Test Issue 2"
        issue2.labels = ["UI", "low_priority", "documentation", "testing", "optimization", "feedback"]
        issue2.events = [self.mock_event("closed")]

        issue3 = Issue()
        issue3.number = 3
        issue3.title = "Test Issue 3"
        issue3.labels = ["bug", "urgent", "frontend", "testing", "feature", "UX"]
        issue3.events = [
            self.mock_event("closed"),
            self.mock_event("reopened"),
            self.mock_event("closed"),
            self.mock_event("reopened"),
        ]

        return [issue1, issue2, issue3]

    def mock_issues_fewer_than_five_labels(self):
        """Mock issues with fewer than five labels."""
        issue = Issue()
        issue.number = 4
        issue.title = "Test Issue Fewer Labels"
        issue.labels = ["bug", "UI"]
        issue.events = [self.mock_event("closed"), self.mock_event("reopened")]

        return [issue]

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

    @patch('sys.stdout', new_callable=StringIO)
    def test_reopened_issue_analysis_output(self, mock_stdout):
        # Arrange
        issues = []

        # Issue 1
        issue1 = Issue()
        issue1.number = 1
        issue1.title = "Test Issue 1"
        issue1.labels = ["bug", "backend", "priority_high", "documentation", "security", "performance"]
        issue1.events = [
            Event({"event_type": "closed", "author": "user2", "event_date": "2024-01-02T16:00:00Z"}),
            Event({"event_type": "reopened", "author": "user1", "event_date": "2024-01-03T09:00:00Z"})
        ]
        issues.append(issue1)

        # Issue 2
        issue2 = Issue()
        issue2.number = 2
        issue2.title = "Test Issue 2"
        issue2.labels = ["frontend", "testing", "feature", "UX", "bug", "documentation", "urgent"]
        issue2.events = [
            Event({"event_type": "closed", "author": "user3", "event_date": "2024-01-04T12:00:00Z"})
        ]
        issues.append(issue2)

        # Issue 3
        issue3 = Issue()
        issue3.number = 3
        issue3.title = "Test Issue 3"
        issue3.labels = ["bug", "urgent", "frontend", "testing", "feature", "UX"]
        issue3.events = [
            Event({"event_type": "closed", "author": "user4", "event_date": "2024-01-05T10:00:00Z"}),
            Event({"event_type": "reopened", "author": "user5", "event_date": "2024-01-06T14:00:00Z"})
        ]
        issues.append(issue3)

        # Patch the data loader to return our mock issues
        with patch('data.data_loader.DataLoader.get_issues', return_value=issues):
            analysis = ReopenedIssueAnalysis()

            # Act
            analysis.run()

        # Assert
        output = mock_stdout.getvalue()
        self.assertIn("Total issues that were reopened after closing: 2", output)
        self.assertIn("bug: 2", output)
        self.assertIn("backend: 1", output)
        self.assertIn("priority_high: 1", output)
        self.assertIn("documentation: 1", output)
        self.assertIn("security: 1", output)
        self.assertIn("performance: 1", output)
        self.assertIn("urgent: 1", output)
        self.assertIn("frontend: 1", output)
        self.assertIn("testing: 1", output)
        self.assertIn("feature: 1", output)
        self.assertIn("UX: 1", output)

    def test_reopened_issue_analysis_fewer_than_five_labels(self):
        mock_issues = self.mock_issues_fewer_than_five_labels()
        mock_loader = self.mock_data_loader(mock_issues)
        with patch("data.data_loader.DataLoader.get_issues", mock_loader.get_issues):
            analysis = ReopenedIssueAnalysis()
            analysis.run()

        # Verify that the plot does not fail for fewer than 5 labels
        self.assertLessEqual(len(analysis.reopened_issues_details), len(mock_issues))

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
