import unittest
from unittest.mock import MagicMock, patch
from io import StringIO
from datetime import datetime
from analysis.event_label_categories_analysis import EventLabelCategoriesAnalysis
from models.model import Issue, Event
import matplotlib
matplotlib.use('Agg')
import config
import pandas as pd


class TestEventLabelCategoriesAnalysis(unittest.TestCase):

    # Tests running the analysis without a label provided
    @patch('config.get_parameter', return_value=None)
    def test_run_without_label_parameter(self, mock_get_parameter):
        """
        Test the behavior of EventLabelCategoriesAnalysis when no label parameter is provided.
        """

        # Mock the print function to capture its output
        with patch('builtins.print') as mock_print:
            analysis = EventLabelCategoriesAnalysis()
            analysis.run()
        
        # Verify that the error message is printed
        mock_print.assert_called_once_with(
            "Error: No label prefix provided. Please specify a label with the --label flag."
        )
        
        # Ensure the mock_get_parameter was called to check the parameter
        mock_get_parameter.assert_called_once()
    
    @patch('config.get_parameter', return_value='kind')  # Mock get_parameter to return 'kind'
    @patch('data.data_loader.DataLoader.get_issues', return_value=None)  # Mock get_issues to return None
    def test_run_with_no_issues(self, mock_get_issues, mock_get_parameter):
        """
        Test the behavior of EventLabelCategoriesAnalysis when DataLoader.get_issues returns None.
        """

        # Mock the print function to capture its output
        try:
            analysis = EventLabelCategoriesAnalysis()
            analysis.run()
        except TypeError:
            self.fail("TypeError raised when get_issues() returns None")

    def test_no_label_events_found(self):
        """
        Test the behavior of EventLabelCategoriesAnalysis when no issues were found with a certain label
        """
        # Setup: Create a mock for the DataLoader to return empty issues
        mock_data_loader = MagicMock()
        mock_data_loader.get_issues.return_value = []  # No issues to simulate no events
        
        # Set the label_prefix to something specific (e.g., "status/")
        with patch('config.get_parameter', return_value='status/'):
            with patch("data.data_loader.DataLoader.get_issues", mock_data_loader.get_issues):
                # Assert that the appropriate message was printed to stdout
                expected_output = "No label events found with prefix 'status/' in the issues data."

                with patch('builtins.print') as mock_print:
                    # Create an instance of the class and run the analysis
                    analysis = EventLabelCategoriesAnalysis()
                    analysis.run()
                    mock_print.assert_called_once_with(expected_output)

    @patch('data.data_loader.DataLoader.get_issues')  # Patch the method directly
    def test_run_with_label_prefix(self, mock_get_issues):
        """
        Test the behavior of EventLabelCategoriesAnalysis when running with a known input.
        """
        # Prepare mock data
        issue1 = MagicMock(spec=Issue)
        issue2 = MagicMock(spec=Issue)
        
        # Create mock events for issue1
        event1 = MagicMock(spec=Event)
        event1.event_type = 'labeled'
        event1.label = 'status/ready'
        issue1.events = [event1]

        # Create mock events for issue2
        event2 = MagicMock(spec=Event)
        event2.event_type = 'labeled'
        event2.label = 'status/in-progress'
        event3 = MagicMock(spec=Event)
        event3.event_type = 'labeled'
        event3.label = 'status/ready'
        issue2.events = [event2, event3]

        # Mock get_issues to return our mock issues
        mock_get_issues.return_value = [issue1, issue2]
        
        # Set label prefix
        config.set_parameter('label', 'status')

        # Capture the print output
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            # Run the analysis
            analysis = EventLabelCategoriesAnalysis()
            analysis.run()
            output = mock_stdout.getvalue()

        # Check if the output contains the expected results, based on code and input values it should be this
        expected_output = (
            "Status Event Analysis for label prefix 'status/':\n"
            "      Label  Event Count\n"
            "      ready            2\n"
            "in-progress            1"
        )

        self.assertIn(expected_output, output)


if __name__ == "__main__":
    unittest.main()
