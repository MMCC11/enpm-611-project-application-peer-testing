import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
from analysis.user_specific_issue_analysis import UserSpecificIssueAnalysis
from models.model import Issue, Event

mock_issues_data = [
    {
        "url": "https://github.com/user1/issue1",
        "creator": "user1",
        "labels": ["bug", "urgent"],
        "state": "open",
        "assignees": ["user2"],
        "title": "Issue 1 title",
        "text": "Issue description",
        "number": 1,
        "created_date": "2024-11-01T00:00:00Z",
        "updated_date": "2024-11-02T00:00:00Z",
        "timeline_url": "https://github.com/user1/issue1/timeline",
        "events": [
            {"event_type": "commented", "author": "user1", "event_date": "2024-11-01T01:00:00Z", "comment": "Initial comment"},
            {"event_type": "commented", "author": "user1", "event_date": "2024-11-03T01:00:00Z", "comment": "Final comment"},
            {"event_type": "labeled", "author": "user1", "event_date": "2024-11-02T02:00:00Z", "label": "bug"},
            {"event_type": "closed", "author": "user2", "event_date": "2024-11-03T03:00:00Z"}
        ]
    },
    {
        "url": "https://github.com/user2/issue2",
        "creator": "user2",
        "labels": ["feature"],
        "state": "closed",
        "assignees": ["user3"],
        "title": "Issue 2 title",
        "text": "Feature request",
        "number": 2,
        "created_date": "2024-10-15T00:00:00Z",
        "updated_date": "2024-10-16T00:00:00Z",
        "timeline_url": "https://github.com/user2/issue2/timeline",
        "events": [
            {"event_type": "commented", "author": "user2", "event_date": "2024-10-16T01:00:00Z", "comment": "Another comment"},
            {"event_type": "labeled", "author": "user3", "event_date": "2024-10-17T02:00:00Z", "label": "feature"},
            {"event_type": "closed", "author": "user3", "event_date": "2024-10-18T03:00:00Z"}
        ]
    }
]

class TestUserSpecificIssueAnalysis(unittest.TestCase):
    
    def mock_issues(self):
        """Mock issues data from the JSON-like structure."""
        issues = []
        for data in mock_issues_data:
            issue = Issue(data)
            issues.append(issue)
        return issues

    def mock_data_loader(self, mock_issues):
        """Mock the DataLoader to return predefined issues."""
        mock_loader = MagicMock()
        mock_loader.get_issues.return_value = mock_issues
        return mock_loader

    def mock_config(self):
        """Mock the config.get_parameter function to provide a specific user."""
        def mock_get_parameter(key):
            if key == "user":
                return "user1"  
            return None
        return mock_get_parameter

    @patch("builtins.print")
    @patch("matplotlib.pyplot.show")
    def test_user_specific_issue_analysis_output(self, mock_show, mock_print):
        """Test the output of the UserSpecificIssueAnalysis class."""
        analysis = UserSpecificIssueAnalysis()
        mock_issues = self.mock_issues()
        mock_loader = self.mock_data_loader(mock_issues)
        with patch("data.data_loader.DataLoader.get_issues", mock_loader.get_issues):
            with patch("config.get_parameter", self.mock_config()):
                analysis.run()
                mock_print.assert_any_call("Insights for User: user1")
                mock_print.assert_any_call("Issues Created: 1")
                mock_print.assert_any_call("Comments Made: 2")
                mock_print.assert_any_call("Issues Labeled: 2")
                mock_print.assert_any_call("Issues Closed: 1")
                mock_print.assert_any_call("\nLabel Interactions:")

    @patch("builtins.print")
    @patch("matplotlib.pyplot.show")
    def test_user_specific_issue_analysis_no_user(self, mock_show, mock_print):
        """Test the behavior when no user is specified."""
        def mock_get_parameter(key):
            return None 

        with patch("config.get_parameter", mock_get_parameter):
            analysis = UserSpecificIssueAnalysis()
            analysis.run()
            mock_print.assert_any_call("No user specified. Please provide a user with the --user flag.")

    @patch("builtins.print")
    @patch("matplotlib.pyplot.show")
    def test_user_specific_issue_analysis_no_interactions(self, mock_show, mock_print):
        """Test the behavior when the user has no interactions."""
        def mock_get_issues():
            return []  

        mock_loader = self.mock_data_loader([])
        with patch("data.data_loader.DataLoader.get_issues", mock_loader.get_issues):
            with patch("config.get_parameter", self.mock_config()):
                analysis = UserSpecificIssueAnalysis()
                analysis.run()
                mock_print.assert_any_call("Insights for User: user1")
                mock_print.assert_any_call("Issues Created: 0")
                mock_print.assert_any_call("Comments Made: 0")
                mock_print.assert_any_call("Issues Labeled: 0")
                mock_print.assert_any_call("Issues Closed: 0")
                
    @patch("matplotlib.pyplot.show")
    def test_user_specific_issue_analysis_label_chart(self, mock_show):
        """Test that the horizontal bar chart is generated without errors."""
        analysis = UserSpecificIssueAnalysis()
        mock_issues = self.mock_issues()
        mock_loader = self.mock_data_loader(mock_issues)
        with patch("data.data_loader.DataLoader.get_issues", mock_loader.get_issues):
            analysis.run()
            mock_show.assert_called_once()

    @patch("builtins.print")
    @patch("matplotlib.pyplot.show")
    def test_user_specific_issue_analysis_invalid_event(self, mock_show, mock_print):
        """Test that invalid events are handled gracefully."""
        issue = Issue(mock_issues_data[0])
        issue.creator = "user1"
        issue.events = [
            Event({"event_type": "unknown", "author": "user1", "event_date": "2024-11-01T01:00:00Z"})  # Invalid event
        ]
        mock_loader = self.mock_data_loader([issue])

        with patch("data.data_loader.DataLoader.get_issues", mock_loader.get_issues):
            with patch("config.get_parameter", self.mock_config()):
                analysis = UserSpecificIssueAnalysis()
                analysis.run()

                mock_print.assert_any_call("Issues Created: 1")
                mock_print.assert_any_call("Comments Made: 0")
                mock_print.assert_any_call("Issues Labeled: 0")
                mock_print.assert_any_call("Issues Closed: 0")

    @patch("builtins.print")
    @patch("matplotlib.pyplot.show")
    def test_user_specific_issue_analysis_empty_label(self, mock_show, mock_print):
        """Test behavior when an issue has an empty label."""
        issue = Issue(mock_issues_data[0])
        issue.creator = "user1"
        issue.events = [
            Event({"event_type": "labeled", "author": "user1", "label": ""}) 
        ]
        mock_loader = self.mock_data_loader([issue])

        with patch("data.data_loader.DataLoader.get_issues", mock_loader.get_issues):
            with patch("config.get_parameter", self.mock_config()):
                analysis = UserSpecificIssueAnalysis()
                analysis.run()

                mock_print.assert_any_call("Issues Created: 1")
                mock_print.assert_any_call("Issues Labeled: 1")

    @patch("matplotlib.pyplot.show")
    def test_user_specific_issue_analysis_missing_labels(self, mock_show):
        """Test that charts are generated even when some labels are missing."""
        issue = Issue(mock_issues_data[1])
        issue.creator = "user2"
        issue.events = [
            Event({"event_type": "labeled", "author": "user2"}) 
        ]
        mock_loader = self.mock_data_loader([issue])

        with patch("data.data_loader.DataLoader.get_issues", mock_loader.get_issues):
            analysis = UserSpecificIssueAnalysis()
            analysis.run()
            mock_show.assert_called_once()


if __name__ == "__main__":
    unittest.main()
