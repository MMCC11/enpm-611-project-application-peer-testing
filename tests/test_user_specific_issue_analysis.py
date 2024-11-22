import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend for tests

import pytest
from unittest.mock import patch, MagicMock
from analysis.user_specific_issue_analysis import UserSpecificIssueAnalysis
from models.model import Issue, Event
from datetime import datetime


@pytest.fixture
def mock_issues():
    """
    Create mock issues for testing.
    """
    issue1 = Issue()
    issue1.creator = "test_user"
    issue1.events = [
        Event({"event_type": "commented", "author": "test_user", "event_date": datetime(2024, 11, 1)}),
        Event({"event_type": "labeled", "author": "test_user", "event_date": datetime(2024, 11, 2), "label": "kind/bug"}),
        Event({"event_type": "closed", "author": "another_user", "event_date": datetime(2024, 11, 3)})
    ]
    
    issue2 = Issue()
    issue2.creator = "another_user"
    issue2.events = [
        Event({"event_type": "commented", "author": "test_user", "event_date": datetime(2024, 11, 4)}),
        Event({"event_type": "labeled", "author": "test_user", "event_date": datetime(2024, 11, 5), "label": "kind/feature"}),
        Event({"event_type": "closed", "author": "test_user", "event_date": datetime(2024, 11, 6)})
    ]
    
    issue3 = Issue()
    issue3.creator = "test_user"
    issue3.events = []

    return [issue1, issue2, issue3]


@pytest.fixture
def mock_data_loader(monkeypatch, mock_issues):
    """
    Mock the DataLoader to return predefined issues.
    """
    mock_loader = MagicMock()
    mock_loader.get_issues.return_value = mock_issues
    monkeypatch.setattr("data.data_loader.DataLoader.get_issues", mock_loader.get_issues)
    return mock_loader


@pytest.fixture
def mock_config(monkeypatch):
    """
    Mock the config.get_parameter function to provide a specific user.
    """
    def mock_get_parameter(key):
        if key == "user":
            return "test_user"
        return None

    monkeypatch.setattr("config.get_parameter", mock_get_parameter)


def test_user_specific_issue_analysis_output(mock_data_loader, mock_config):
    """
    Test the output of the UserSpecificIssueAnalysis class.
    """
    analysis = UserSpecificIssueAnalysis()

    with patch("builtins.print") as mock_print, patch("matplotlib.pyplot.show"):
        analysis.run()

        # Verify printed output
        mock_print.assert_any_call("Insights for User: test_user")
        mock_print.assert_any_call("Issues Created: 2")
        mock_print.assert_any_call("Comments Made: 2")
        mock_print.assert_any_call("Issues Labeled: 2")
        mock_print.assert_any_call("Issues Closed: 1")
        mock_print.assert_any_call("\nLabel Interactions:")


def test_user_specific_issue_analysis_no_user(mock_data_loader, monkeypatch):
    """
    Test the behavior when no user is specified.
    """
    def mock_get_parameter(key):
        return None  # Simulate missing user

    monkeypatch.setattr("config.get_parameter", mock_get_parameter)

    analysis = UserSpecificIssueAnalysis()

    with patch("builtins.print") as mock_print, patch("matplotlib.pyplot.show"):
        analysis.run()

        # Verify printed output
        mock_print.assert_any_call("No user specified. Please provide a user with the --user flag.")


# def test_user_specific_issue_analysis_no_interactions(mock_data_loader, monkeypatch):
#     """
#     Test the behavior when the user has no interactions.
#     """
#     def mock_get_issues():
#         return []  # Simulate no issues

#     mock_data_loader.get_issues.side_effect = mock_get_issues

#     analysis = UserSpecificIssueAnalysis()

#     with patch("builtins.print") as mock_print, patch("matplotlib.pyplot.show"):
#         analysis.run()

#         # Verify printed output
#         mock_print.assert_any_call("Insights for User: test_user")
#         mock_print.assert_any_call("Issues Created: 0")
#         mock_print.assert_any_call("Comments Made: 0")
#         mock_print.assert_any_call("Issues Labeled: 0")
#         mock_print.assert_any_call("Issues Closed: 0")


def test_user_specific_issue_analysis_label_chart(mock_data_loader, mock_config):
    """
    Test that the horizontal bar chart is generated without errors.
    """
    analysis = UserSpecificIssueAnalysis()

    with patch("matplotlib.pyplot.show") as mock_show:
        analysis.run()

        # Verify the chart display
        mock_show.assert_called_once()
