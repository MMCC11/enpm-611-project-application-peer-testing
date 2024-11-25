import unittest
from unittest.mock import MagicMock, patch
from io import StringIO
from datetime import datetime
from analysis.issue_analysis import IssueAnalysis
from models.model import Issue
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')

class TestIssueAnalysis(unittest.TestCase):
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
        issue1.state = "closed"
        issue1.assignees = "assigned"
        issue1.events = [self.mock_event("closed"), self.mock_event("assigned")]
        issue2 = Issue()
        issue2.number = 2
        issue2.title = "Test Issue 2"
        issue2.labels = ["kind/feature"]
        issue2.state = "open"
        issue2.assignees = "assigned"
        issue3 = Issue()
        issue3.number = 3
        issue3.title = "Test Issue 3"
        issue3.labels = ["kind/bug", "status/triage"]
        issue3 = Issue()
        issue3.number = 3
        issue3.title = "Test Issue 3"
        issue3.labels = ["test_label", "test_label2", "test_label3", "test_label4"]
        issue4 = Issue()
        issue4.number = 4
        issue4.title = "Test Issue 4"
        issue4.labels = ["test_label4"]
        issue5 = Issue()
        issue5.number = 5
        issue5.title = "Test Issue 5"
        issue5.labels = ["test_label5"]
        issue6 = Issue()
        issue6.number = 6
        issue6.title = "Test Issue 6"
        issue6.labels = ["test_label6"]
        issue7 = Issue()
        issue7.number = 7
        issue7.title = "Test Issue 7"
        issue7.labels = ["test_label7"]
        return [issue1, issue2, issue3, issue4, issue5, issue6,issue7] #created enough issues to ensure coverage on all statement


    def mock_data_loader(self, mock_issues):
        mock_loader = MagicMock()
        mock_loader.get_issues.return_value = mock_issues
        return mock_loader
    
    def mock_config(self):
        """Mock the config.get_parameter function to provide a specific user."""
        def mock_get_parameter(key):
            if key == "label":
                return "kind/bug"  
            return None
        return mock_get_parameter
    
    def test_issue_analysis_empty_data_loader(self):
        mock_loader = MagicMock()
        mock_loader.get_issues.return_value = []
        with patch("data.data_loader.DataLoader.get_issues", mock_loader.get_issues):
            analysis = IssueAnalysis()
            with patch("matplotlib.pyplot.show"):
                analysis.run()

        mock_loader.get_issues.assert_called_once()

    def test_issue_analysis_run_no_input(self):
        mock_issues = self.mock_issues()
        mock_loader = self.mock_data_loader(mock_issues)
        def mock_get_parameter(key):
            return None
        with patch("data.data_loader.DataLoader.get_issues", mock_loader.get_issues):
            with patch("config.get_parameter", mock_get_parameter):
                analysis = IssueAnalysis()
                with patch("matplotlib.pyplot.show"):
                    analysis.run()


        mock_loader.get_issues.assert_called_once() 
        fig = plt.gcf()
        title = fig.axes[0].get_title()
        self.assertEqual(title, "Distribution of Time to Assign Issues") #checking for right graph

    def test_issue_analysis_run_label_input(self):
        mock_issues = self.mock_issues()
        mock_loader = self.mock_data_loader(mock_issues)
        with patch("data.data_loader.DataLoader.get_issues", mock_loader.get_issues):
            with patch("config.get_parameter", self.mock_config()):
                analysis = IssueAnalysis()
                with patch("matplotlib.pyplot.show"):
                    analysis.run()

        mock_loader.get_issues.assert_called_once() 
        fig = plt.gcf()
        title = fig.axes[0].get_title()
        self.assertEqual(title, "Distribution of Time to Assign Issues (Label = kind/bug)") #checking for right graph
    
    def test_issue_analysis_run_label_input_label_blank(self):
        mock_issues = self.mock_issues()
        mock_loader = self.mock_data_loader(mock_issues)
        def mock_get_parameter(key):
            return ""
        with patch("data.data_loader.DataLoader.get_issues", mock_loader.get_issues):
            with patch("config.get_parameter", mock_get_parameter):
                analysis = IssueAnalysis()
                with patch("matplotlib.pyplot.show"):
                    analysis.run()




    def test_issue_analysis_no_issues(self):
        mock_loader = MagicMock()
        mock_loader.get_issues.return_value = []
        with patch("data.data_loader.DataLoader.get_issues", mock_loader.get_issues):
            analysis = IssueAnalysis()
            with patch("matplotlib.pyplot.show"):
                analysis.run()

        mock_loader.get_issues.assert_called_once()

    def test_issue_analysis_no_labels(self):
        mock_issues = self.mock_issues()
        for issue in mock_issues:
            issue.labels = []

        mock_loader = self.mock_data_loader(mock_issues)
        with patch("data.data_loader.DataLoader.get_issues", mock_loader.get_issues):
            analysis = IssueAnalysis()
            with patch("matplotlib.pyplot.show"):
                analysis.run()

        captured = unittest.mock.MagicMock()
        analysis.run()

        assert "Label Trend Over Time" in captured.out

    def test_issue_analysis_plot_labels(self):
        mock_issues = self.mock_issues()
        mock_loader = self.mock_data_loader(mock_issues)
        with patch("data.data_loader.DataLoader.get_issues", mock_loader.get_issues):
            analysis = IssueAnalysis()
            with patch("matplotlib.pyplot.show") as mock_show:
                analysis.run()

    def test_issue_analysis_invalid_label_format(self):
        mock_issues = self.mock_issues()
        mock_issues[0].labels = ["invalid/label_format"]
        mock_issues[1].labels = ["kind/feature"]

        mock_loader = self.mock_data_loader(mock_issues)
        with patch("data.data_loader.DataLoader.get_issues", mock_loader.get_issues):
            analysis = IssueAnalysis()
            with patch("matplotlib.pyplot.show"):
                analysis.run()
        assert "invalid/label_format" in mock_issues[0].labels
        assert "kind/feature" in mock_issues[1].labels

    def test_issue_analysis_invalid_created_date_type(self):
            # Mocking issues with invalid date formats
        mock_issues = self.mock_issues()
        mock_issues[0].created_date = "invalid-date-format"  
        mock_issues[1].created_date = 1234567890  

        mock_loader = self.mock_data_loader(mock_issues)

        with patch("data.data_loader.DataLoader.get_issues", mock_loader.get_issues):
            analysis = IssueAnalysis()
            captured_output = StringIO()
            with patch("sys.stdout", new=captured_output):  
                with patch("matplotlib.pyplot.show"):  
                    analysis.run()

            captured_value = captured_output.getvalue()
            assert "invalid date" in captured_value  

    def test_issue_analysis_invalid_month_format(self):
        mock_issues = self.mock_issues()
        mock_issues[0].created_date = "2024/10/20"  # Invalid format
        mock_issues[1].created_date = "2024-11-15"  # Valid format

        mock_loader = self.mock_data_loader(mock_issues)
        with patch("data.data_loader.DataLoader.get_issues", mock_loader.get_issues):
            analysis = IssueAnalysis()
            with patch("matplotlib.pyplot.show"):
                analysis.run()

        captured = unittest.mock.MagicMock()
        analysis.run()

        assert "2024-10" not in captured.out
        assert "2024-11" in captured.out

    def test_issue_analysis_handle_large_data_set(self):
        mock_issues = self.mock_issues()
        large_mock_issues = mock_issues * 1000 
        mock_loader = self.mock_data_loader(large_mock_issues)
        with patch("data.data_loader.DataLoader.get_issues", mock_loader.get_issues):
            analysis = IssueAnalysis()
            with patch("matplotlib.pyplot.show"):
                analysis.run()

        mock_loader.get_issues.assert_called_once()

if __name__ == "__main__":
    unittest.main()
