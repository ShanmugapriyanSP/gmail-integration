import builtins
import os
import unittest
from unittest.mock import patch, MagicMock

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from resources.mock_data import MockData
from service.oauth_service import OAuthService, Config
from test_utils import TestUtils
from utils.generic import GenericUtils


@patch.object(os.path, 'exists')
@patch.object(GenericUtils, 'load_yaml', return_value=MockData.get_config())
class TestOAuthService(unittest.TestCase):

    @patch.object(InstalledAppFlow, 'from_client_secrets_file')
    @patch.object(Credentials, 'refresh')
    @patch.object(Credentials, 'from_authorized_user_file')
    def test_authenticate_with_existing_token(self, mock_from_authorized_user_file, mock_refresh,
                                              mock_from_client_secrets_file, mock_config, mock_token_existence):
        # Mock Credentials.from_authorized_user_file
        mock_credentials = Credentials(
            token='valid_token',
            refresh_token='valid_refresh_token',
            expiry=TestUtils.get_future_date()
        )
        mock_from_authorized_user_file.return_value = mock_credentials
        config_vars = Config()

        # WHEN
        oauth_service = OAuthService(config_vars)

        # THEN
        self.assertEqual(oauth_service.credentials, mock_credentials)
        # Verify client secret & refresh are not called
        mock_from_client_secrets_file.assert_not_called()
        mock_refresh.assert_not_called()

    @patch.object(builtins, 'open')
    @patch.object(Credentials, 'refresh')
    @patch.object(Credentials, 'from_authorized_user_file')
    def test_authenticate_with_expired_refresh_token(self,  mock_from_authorized_user_file,
                                                     mock_refresh, mock_token_write, mock_config, mock_token_existence):
        # GIVEN
        # Mock dependencies
        mock_token_existence.return_value = True
        # Mock credentials
        mock_from_authorized_user_file.return_value = Credentials(
            token="expired_token",
            refresh_token="expired_token",
            expiry=TestUtils.get_past_date()
        )
        config_vars = Config()

        # WHEN
        OAuthService(config_vars)

        # THEN
        # Verify refresh is called
        mock_refresh.assert_called_once()
        mock_token_write.assert_called_once()

    @patch.object(builtins, 'open')
    @patch.object(InstalledAppFlow, 'from_client_secrets_file')
    def test_authenticate_no_existing_token(self, mock_from_client_secrets_file, mock_token_write, mock_config,
                                            mock_token_existence):
        # GIVEN
        # Mock dependencies
        mock_token_existence.return_value = False
        mock_from_client_secrets_file.return_value = MagicMock(spec=InstalledAppFlow)
        config_vars = Config()

        # WHEN
        OAuthService(config_vars)

        # THEN
        mock_from_client_secrets_file.assert_called_once()
        mock_token_write.assert_called_once()


    # @patch('os.path.exists')
    # def test_authenticate_invalid_token(self, mock_exists):
    #     # Mock os.path exists to simulate an invalid token file
    #     mock_exists.return_value = True
    #
    #     # Mock Credentials.from_authorized_user_file to raise exception
    #     with patch.object(Credentials, 'from_authorized_user_file') as mock_from_authorized_user_file:
    #         mock_from_authorized_user_file.side_effect = Exception('Invalid token file')
    #
    #     # Configure test case
    #     config_vars = Config()  # Assuming Config provides necessary data
    #
    #     # Call the method and assert it raises an exception
    #     with self.assertRaises(Exception):
    #         OAuthService(config_vars)
