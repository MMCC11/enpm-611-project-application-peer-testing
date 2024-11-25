import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta
import pandas as pd
from analysis.time_based_issue_analysis import TimeBasedIssueAnalysis
from models.model import Issue, Event


class TestTimeBasedIssueAnalysis(unittest.TestCase):
    def setUp(self):
        """Set up mock data for testing."""
        # Mock data for closed and open issues
        self.mock_issues = [
            Issue({
                "number": 1,
                "creator": "user1",
                "labels": ["bug"],
                "state": "closed",
                "closed_time": "",
                "created_date": "2024-10-12T13:13:00+00:00",
                "events": [
                    {
                        "event_type": "closed",
                        "author": "bram-tv",
                        "event_date": "2024-10-12T13:13:00+00:00",
                        "label": "kind/bug"
                    }
                ]
            }),
            Issue({
                "number": 2,
                "creator": "user2",
                "labels": ["enhancement"],
                "state": "closed",
                "created_date": "2024-12-12T13:13:00+00:00",
                "events": [
                    {
                        "event_type": "closed",
                        "author": "bram-tv",
                        "event_date": "2024-10-12T13:13:00+00:00",
                        "label": "kind/bug"
                    }
                ]
            }),
            Issue({
                "number": 3,
                "creator": "user3",
                "labels": ["documentation"],
                "state": "open",
                "created_date": "2024-10-12T10:13:00+00:00",
                "events": []
            }),
        ]
        self.empty_issues = []

    @patch("data.data_loader.DataLoader.get_issues")
    def test_run_with_closed_issues(self, mock_get_issues):
        """Test the `run` method with closed issues."""
        mock_get_issues.return_value = self.mock_issues
        analysis = TimeBasedIssueAnalysis()
        
        with patch.object(analysis, "analyse_closed_issues") as mock_analyse_closed, \
             patch.object(analysis, "analyse_based_on_user") as mock_analyse_user:
            analysis.run()
            # Assert that methods are called
            mock_analyse_closed.assert_called_once()
            mock_analyse_user.assert_not_called()

    @patch("data.data_loader.DataLoader.get_issues")
    def test_run_with_user_filter(self, mock_get_issues):
        """Test the `run` method with a specific user filter."""
        mock_get_issues.return_value = self.mock_issues
        with patch("config.get_parameter", return_value="user1"), \
             patch.object(TimeBasedIssueAnalysis, "analyse_based_on_user") as mock_analyse_user:
            analysis = TimeBasedIssueAnalysis()
            analysis.run()
            mock_analyse_user.assert_called_once()

    def test_create_dataframe(self):
        """Test the creation of a DataFrame from closed issues."""
        analysis = TimeBasedIssueAnalysis()
        closed_issues = [self.mock_issues[0], self.mock_issues[1]]
        df = analysis.create_dataframe(closed_issues)

        # Assert the DataFrame has the expected structure
        self.assertEqual(len(df), 2)
        self.assertIn("issue_id", df.columns)
        self.assertIn("creator", df.columns)
        self.assertIn("labels", df.columns)
        self.assertIn("time_diff_in_days", df.columns)

        # Assert time difference calculation is correct
        self.assertEqual(df.iloc[0]["time_diff_in_days"], 4)  # Difference between Jan 1 and Jan 5

    def test_empty_dataframe(self):
        """Test handling of an empty list of closed issues."""
        analysis = TimeBasedIssueAnalysis()
        df = analysis.create_dataframe(self.empty_issues)

        # Assert the DataFrame is empty
        self.assertTrue(df.empty)

    def test_analyse_closed_issues(self):
        """Test the analysis of closed issues."""
        analysis = TimeBasedIssueAnalysis()
        closed_issues = [self.mock_issues[0], self.mock_issues[1]]
        df = analysis.create_dataframe(closed_issues)

        with patch("plotly.express.bar") as mock_bar:
            analysis.analyse_closed_issues(df)

            # Ensure a plot is created
            mock_bar.assert_called()

    def test_analyse_closed_issues_with_duplicates(self):
        """Test analysis when there are duplicate creators."""
        analysis = TimeBasedIssueAnalysis()
        closed_issues = [
            Issue({
                "number": 1,
                "creator": "user1",
                "labels": ["bug"],
                "state": "closed",
                "created_date": datetime(2024, 1, 1),
                "events": [
                    {"event_type": "closed", "author": "user2", "event_date": datetime(2024, 1, 5)}
                ]
            }),
            Issue({
                "number": 2,
                "creator": "user1",
                "labels": ["enhancement"],
                "state": "closed",
                "created_date": datetime(2024, 1, 10),
                "events": [
                    {"event_type": "closed", "author": "user3", "event_date": datetime(2024, 1, 20)}
                ]
            }),
        ]
        df = analysis.create_dataframe(closed_issues)

        with patch("plotly.express.bar") as mock_bar:
            analysis.analyse_closed_issues(df)

            # Check if duplicates are handled correctly
            self.assertFalse(df.duplicated(subset=["creator"]).any())

    def test_get_approx_months(self):
        """Test the conversion of days to approximate months."""
        analysis = TimeBasedIssueAnalysis()
        days = 90  # 3 months
        months = analysis.get_approx_months(days)
        self.assertEqual(months, 3)

    def test_analyse_based_on_user(self):
        """Test user-specific analysis."""
        analysis = TimeBasedIssueAnalysis()
        closed_issues = [self.mock_issues[0], self.mock_issues[1]]
        df = analysis.create_dataframe(closed_issues)

        with patch("plotly.express.bar") as mock_bar:
            analysis.analyse_based_on_user("user1", df)

            # Ensure the plot is created only for the specific user
            mock_bar.assert_called()
            user_df = df[df["creator"] == "user1"]
            self.assertEqual(len(user_df), 1)

    def test_analyse_based_on_user_no_data(self):
        """Test user-specific analysis with no matching data."""
        analysis = TimeBasedIssueAnalysis()
        closed_issues = [self.mock_issues[0], self.mock_issues[1]]
        df = analysis.create_dataframe(closed_issues)

        with patch("plotly.express.bar") as mock_bar:
            analysis.analyse_based_on_user("nonexistent_user", df)

            # Ensure no plot is created for non-existent user
            mock_bar.assert_not_called()


if __name__ == "__main__":
    unittest.main()
