import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime
from analysis.label_trend_analysis import LabelTrendAnalysis
from models.model import Issue, Event
import matplotlib
matplotlib.use('Agg')

@pytest.fixture
def mock_issues():
    """
    Create mock issues with valid created_date and label data.
    """
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

    return [issue1, issue2, issue3, issue4]


@pytest.fixture
def mock_data_loader(monkeypatch, mock_issues):
    """
    Mock the DataLoader to return predefined issues.
    """
    mock_loader = MagicMock()
    mock_loader.get_issues.return_value = mock_issues
    monkeypatch.setattr("data.data_loader.DataLoader.get_issues", mock_loader.get_issues)
    return mock_loader


def test_label_trend_analysis_run(mock_data_loader):
    """
    Test the run method of LabelTrendAnalysis.
    """
    analysis = LabelTrendAnalysis()

    # Mock matplotlib to prevent actual rendering during the test
    with patch("matplotlib.pyplot.show"):
        analysis.run()

    mock_data_loader.get_issues.assert_called_once()


def test_label_trend_analysis_output(mock_data_loader, capsys):
    """
    Test if LabelTrendAnalysis outputs the correct label trend data.
    """
    analysis = LabelTrendAnalysis()

    # Mock matplotlib to prevent rendering and run the analysis
    with patch("matplotlib.pyplot.show"):
        analysis.run()

    # Capture standard output
    captured = capsys.readouterr()

    # Assert some expected text in the output
    assert "Label Trend Over Time (Top 5 Labels):" in captured.out
    assert "kind/bug" in captured.out
    assert "status/triage" in captured.out
    assert "kind/feature" in captured.out
    assert "2024-09" in captured.out
    assert "2024-10" in captured.out


def test_label_trend_analysis_no_issues(monkeypatch):
    """
    Test LabelTrendAnalysis with no issues.
    """
    mock_loader = MagicMock()
    mock_loader.get_issues.return_value = []  # Simulate no issues
    monkeypatch.setattr("data.data_loader.DataLoader.get_issues", mock_loader.get_issues)

    analysis = LabelTrendAnalysis()

    # Mock matplotlib to prevent rendering
    with patch("matplotlib.pyplot.show"):
        analysis.run()

    mock_loader.get_issues.assert_called_once()


def test_label_trend_analysis_missing_dates(mock_data_loader, mock_issues):
    """
    Test LabelTrendAnalysis with missing created_date in some issues.
    """
    mock_issues[0].created_date = None  # Simulate missing date
    mock_issues[1].created_date = datetime(2024, 9, 15)

    analysis = LabelTrendAnalysis()

    # Mock matplotlib to prevent rendering
    with patch("matplotlib.pyplot.show"):
        analysis.run()

    mock_data_loader.get_issues.assert_called_once()
