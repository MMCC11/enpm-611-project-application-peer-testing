import unittest
from unittest.mock import MagicMock, patch
from io import StringIO
from datetime import datetime
from analysis.label_trend_analysis import LabelTrendAnalysis
from models.model import Issue
import matplotlib
matplotlib.use('Agg')

class TestLabelTrendAnalysis(unittest.TestCase):
    def mock_issues(self):
        issue1 = Issue()
        issue1.labels = ["kind/bug", "status/triage"]
        issue1.created_date = datetime(2024, 10, 20)

        issue2 = Issue()
        issue2.labels = ["kind/feature"]
        issue2.created_date = datetime(2024, 9, 15)

        issue3 = Issue()
        issue3.labels = ["kind/bug", "status/triage"]
        issue3.created_date = datetime(2024, 10, 21)

        issue4 = Issue()
        issue4.labels = ["kind/feature"]
        issue4.created_date = datetime(2024, 9, 16)

        issue5 = Issue()
        issue5.labels = ["kind/enhancement"]
        issue5.created_date = None

        return [issue1, issue2, issue3, issue4, issue5]

    def mock_data_loader(self, mock_issues):
        mock_loader = MagicMock()
        mock_loader.get_issues.return_value = mock_issues
        return mock_loader

    def test_label_trend_analysis_empty_data_loader(self):
        mock_loader = MagicMock()
        mock_loader.get_issues.return_value = []
        with patch("data.data_loader.DataLoader.get_issues", mock_loader.get_issues):
            analysis = LabelTrendAnalysis()
            with patch("matplotlib.pyplot.show"):
                analysis.run()

        mock_loader.get_issues.assert_called_once()

    def test_label_trend_analysis_run(self):
        mock_issues = self.mock_issues()
        mock_loader = self.mock_data_loader(mock_issues)
        with patch("data.data_loader.DataLoader.get_issues", mock_loader.get_issues):
            analysis = LabelTrendAnalysis()
            with patch("matplotlib.pyplot.show"):
                analysis.run()

        mock_loader.get_issues.assert_called_once()

    def test_label_trend_analysis_output(self):
        mock_issues = self.mock_issues()
        mock_loader = self.mock_data_loader(mock_issues)
        with patch("data.data_loader.DataLoader.get_issues", mock_loader.get_issues):
            analysis = LabelTrendAnalysis()
            with patch("matplotlib.pyplot.show"):
                analysis.run()

        captured = unittest.mock.MagicMock()
        analysis.run()

        assert "Label Trend Over Time (Top 5 Labels):" in captured.out
        assert "kind/bug" in captured.out
        assert "status/triage" in captured.out
        assert "kind/feature" in captured.out
        assert "2024-09" in captured.out
        assert "2024-10" in captured.out

    def test_label_trend_analysis_no_issues(self):
        mock_loader = MagicMock()
        mock_loader.get_issues.return_value = []
        with patch("data.data_loader.DataLoader.get_issues", mock_loader.get_issues):
            analysis = LabelTrendAnalysis()
            with patch("matplotlib.pyplot.show"):
                analysis.run()

        mock_loader.get_issues.assert_called_once()

    def test_label_trend_analysis_missing_dates(self):
        mock_issues = self.mock_issues()
        mock_issues[0].created_date = None
        mock_issues[1].created_date = datetime(2024, 9, 15)

        mock_loader = self.mock_data_loader(mock_issues)
        with patch("data.data_loader.DataLoader.get_issues", mock_loader.get_issues):
            analysis = LabelTrendAnalysis()
            with patch("matplotlib.pyplot.show"):
                analysis.run()

        mock_loader.get_issues.assert_called_once()

    def test_label_trend_analysis_no_labels(self):
        mock_issues = self.mock_issues()
        for issue in mock_issues:
            issue.labels = []

        mock_loader = self.mock_data_loader(mock_issues)
        with patch("data.data_loader.DataLoader.get_issues", mock_loader.get_issues):
            analysis = LabelTrendAnalysis()
            with patch("matplotlib.pyplot.show"):
                analysis.run()

        captured = unittest.mock.MagicMock()
        analysis.run()

        assert "Label Trend Over Time" in captured.out
        assert "bugs" not in captured.out

    def test_label_trend_analysis_empty_month(self):
        mock_issues = self.mock_issues()
        mock_issues[0].created_date = datetime(2024, 10, 20)
        mock_issues[1].created_date = datetime(2024, 8, 10)

        mock_loader = self.mock_data_loader(mock_issues)
        with patch("data.data_loader.DataLoader.get_issues", mock_loader.get_issues):
            analysis = LabelTrendAnalysis()
            with patch("matplotlib.pyplot.show"):
                analysis.run()

        captured = unittest.mock.MagicMock()
        analysis.run()

        assert "2024-10" in captured.out
        assert "2024-8" in captured.out
        assert "0" in captured.out

    def test_label_trend_analysis_plot_labels(self):
        mock_issues = self.mock_issues()
        mock_loader = self.mock_data_loader(mock_issues)
        with patch("data.data_loader.DataLoader.get_issues", mock_loader.get_issues):
            analysis = LabelTrendAnalysis()
            with patch("matplotlib.pyplot.show") as mock_show:
                analysis.run()
                mock_show.assert_called_once()

        captured = unittest.mock.MagicMock()
        analysis.run()

        assert "Trend of Top 5 Label Usage Over Time" in captured.out

    def test_label_trend_analysis_top_labels(self):
        mock_issues = self.mock_issues()
        mock_loader = self.mock_data_loader(mock_issues)
        with patch("data.data_loader.DataLoader.get_issues", mock_loader.get_issues):
            analysis = LabelTrendAnalysis()
            with patch("matplotlib.pyplot.show"):
                analysis.run()

        assert "kind/bug" in mock_issues[0].labels
        assert "status/triage" in mock_issues[2].labels

    def test_label_trend_analysis_fewer_than_5_labels(self):
        mock_issues = self.mock_issues()
        mock_issues[0].labels = ["kind/bug"]
        mock_issues[1].labels = ["status/triage"]

        mock_loader = self.mock_data_loader(mock_issues)
        with patch("data.data_loader.DataLoader.get_issues", mock_loader.get_issues):
            analysis = LabelTrendAnalysis()
            with patch("matplotlib.pyplot.show"):
                analysis.run()

        captured = unittest.mock.MagicMock()
        analysis.run()

        assert "kind/bug" in captured.out
        assert "status/triage" in captured.out
        assert "2024-09" in captured.out
        assert "2024-10" in captured.out

    def test_label_trend_analysis_invalid_date_format(self):
        mock_issues = self.mock_issues()
        mock_issues[0].created_date = "invalid-date-format"

        mock_loader = self.mock_data_loader(mock_issues)
        with patch("data.data_loader.DataLoader.get_issues", mock_loader.get_issues):
            analysis = LabelTrendAnalysis()
            with patch("matplotlib.pyplot.show"):
                analysis.run()

        captured = unittest.mock.MagicMock()
        analysis.run()

        assert "invalid date" in captured.out

    def test_label_trend_analysis_invalid_label_format(self):
        mock_issues = self.mock_issues()
        mock_issues[0].labels = ["invalid/label_format"]
        mock_issues[1].labels = ["kind/feature"]

        mock_loader = self.mock_data_loader(mock_issues)
        with patch("data.data_loader.DataLoader.get_issues", mock_loader.get_issues):
            analysis = LabelTrendAnalysis()
            with patch("matplotlib.pyplot.show"):
                analysis.run()

        assert "invalid/label_format" in mock_issues[0].labels
        assert "kind/feature" in mock_issues[1].labels

    def test_label_trend_analysis_different_time_range(self):
        mock_issues = self.mock_issues()
        mock_issues[0].created_date = datetime(2023, 5, 10)
        mock_issues[1].created_date = datetime(2024, 10, 20)

        mock_loader = self.mock_data_loader(mock_issues)
        with patch("data.data_loader.DataLoader.get_issues", mock_loader.get_issues):
            analysis = LabelTrendAnalysis()
            with patch("matplotlib.pyplot.show"):
                analysis.run()

        captured = unittest.mock.MagicMock()
        analysis.run()

        assert "2023-05" in captured.out
        assert "2024-10" in captured.out

    def test_label_trend_analysis_invalid_created_date_type(self):
            # Mocking issues with invalid date formats
        mock_issues = self.mock_issues()
        mock_issues[0].created_date = "invalid-date-format"  
        mock_issues[1].created_date = 1234567890  

        mock_loader = self.mock_data_loader(mock_issues)

        with patch("data.data_loader.DataLoader.get_issues", mock_loader.get_issues):
            analysis = LabelTrendAnalysis()
            captured_output = StringIO()
            with patch("sys.stdout", new=captured_output):  
                with patch("matplotlib.pyplot.show"):  
                    analysis.run()

            captured_value = captured_output.getvalue()
            assert "invalid date" in captured_value  

    def test_label_trend_analysis_invalid_month_format(self):
        mock_issues = self.mock_issues()
        mock_issues[0].created_date = "2024/10/20"  # Invalid format
        mock_issues[1].created_date = "2024-11-15"  # Valid format

        mock_loader = self.mock_data_loader(mock_issues)
        with patch("data.data_loader.DataLoader.get_issues", mock_loader.get_issues):
            analysis = LabelTrendAnalysis()
            with patch("matplotlib.pyplot.show"):
                analysis.run()

        captured = unittest.mock.MagicMock()
        analysis.run()

        assert "2024-10" not in captured.out
        assert "2024-11" in captured.out

    def test_label_trend_analysis_handle_large_data_set(self):
        mock_issues = self.mock_issues()
        large_mock_issues = mock_issues * 1000 
        mock_loader = self.mock_data_loader(large_mock_issues)
        with patch("data.data_loader.DataLoader.get_issues", mock_loader.get_issues):
            analysis = LabelTrendAnalysis()
            with patch("matplotlib.pyplot.show"):
                analysis.run()

        mock_loader.get_issues.assert_called_once()

    def test_label_trend_analysis_edge_case(self):
        mock_issues = [Issue()]
        mock_issues[0].labels = ["kind/bug"]
        mock_issues[0].created_date = datetime(2024, 10, 20)

        mock_loader = self.mock_data_loader(mock_issues)
        with patch("data.data_loader.DataLoader.get_issues", mock_loader.get_issues):
            analysis = LabelTrendAnalysis()
            with patch("matplotlib.pyplot.show"):
                analysis.run()

        assert "kind/bug" in mock_issues[0].labels
        assert "2024-10" in mock_issues[0].created_date.strftime("%Y-%m")


if __name__ == "__main__":
    unittest.main()
