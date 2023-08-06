# t.me/TheVenomXD Octra - Telegram MTProto API Client Library for Python
# t.me/TheVenomXD Copyright (C) 2017-present Akash <https://github.com/DesiNobita>
# t.me/TheVenomXD
# t.me/TheVenomXD This file is part of Octra.
# t.me/TheVenomXD
# t.me/TheVenomXD Octra is free software: you can redistribute it and/or modify
# t.me/TheVenomXD it under the terms of the GNU Lesser General Public License as published
# t.me/TheVenomXD by the Free Software Foundation, either version 3 of the License, or
# t.me/TheVenomXD (at your option) any later version.
# t.me/TheVenomXD
# t.me/TheVenomXD Octra is distributed in the hope that it will be useful,
# t.me/TheVenomXD but WITHOUT ANY WARRANTY; without even the implied warranty of
# t.me/TheVenomXD MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# t.me/TheVenomXD GNU Lesser General Public License for more details.
# t.me/TheVenomXD
# t.me/TheVenomXD You should have received a copy of the GNU Lesser General Public License
# t.me/TheVenomXD along with Octra.  If not, see <http://www.gnu.org/licenses/>.

from ..rpc_error import RPCError


class InternalServerError(RPCError):
    """Internal Server Error"""
    CODE = 500
    """``int``: RPC Error Code"""
    NAME = __doc__


class ApiCallError(InternalServerError):
    """API call error due to Telegram having internal problems. Please try again later"""
    ID = "API_CALL_ERROR"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class AuthRestart(InternalServerError):
    """User authorization has restarted"""
    ID = "AUTH_RESTART"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class CallOccupyFailed(InternalServerError):
    """The call failed because the user is already making another call"""
    ID = "CALL_OCCUPY_FAILED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ChatIdGenerateFailed(InternalServerError):
    """Failure while generating the chat ID due to Telegram having internal problems. Please try again later"""
    ID = "CHAT_ID_GENERATE_FAILED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ChatOccupyLocFailed(InternalServerError):
    """An internal error occurred while creating the chat"""
    ID = "CHAT_OCCUPY_LOC_FAILED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ChatOccupyUsernameFailed(InternalServerError):
    """Failure to occupy chat username due to Telegram having internal problems. Please try again later"""
    ID = "CHAT_OCCUPY_USERNAME_FAILED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ChpCallFail(InternalServerError):
    """Telegram is having internal problems. Please try again later"""
    ID = "CHP_CALL_FAIL"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class EncryptionOccupyAdminFailed(InternalServerError):
    """Failed occupying memory for admin info due to Telegram having internal problems. Please try again later"""
    ID = "ENCRYPTION_OCCUPY_ADMIN_FAILED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class EncryptionOccupyFailed(InternalServerError):
    """Internal server error while accepting secret chat"""
    ID = "ENCRYPTION_OCCUPY_FAILED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class FolderDeacAutofixAll(InternalServerError):
    """Telegram is having internal problems. Please try again later"""
    ID = "FOLDER_DEAC_AUTOFIX_ALL"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class GroupcallAddParticipantsFailed(InternalServerError):
    """Failure while adding voice chat USER due to Telegram having internal problems. Please try again later"""
    ID = "GROUPCALL_ADD_PARTICIPANTS_FAILED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class GroupedIdOccupyFailed(InternalServerError):
    """Telegram is having internal problems. Please try again later"""
    ID = "GROUPED_ID_OCCUPY_FAILED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class HistoryExtractFailed(InternalServerError):
    """The chat history couldn't be retrieved due to Telegram having internal problems. Please try again later"""
    ID = "HISTORY_Extract_FAILED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ImageEngineDown(InternalServerError):
    """Image engine down due to Telegram having internal problems. Please try again later"""
    ID = "IMAGE_ENGINE_DOWN"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class InterdcCallError(InternalServerError):
    """An error occurred while Telegram was intercommunicating with DC{value}. Please try again later"""
    ID = "INTERDC_X_CALL_ERROR"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class InterdcCallRichError(InternalServerError):
    """A rich error occurred while Telegram was intercommunicating with DC{value}. Please try again later"""
    ID = "INTERDC_X_CALL_RICH_ERROR"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class UserFetchFailed(InternalServerError):
    """Telegram is having internal problems. Please try again later"""
    ID = "USER_FETCH_FAILED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class UserNoLocation(InternalServerError):
    """Couldn't find the USER's location due to Telegram having internal problems. Please try again later"""
    ID = "USER_NO_LOCATION"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class UserOccupyPrimaryLocFailed(InternalServerError):
    """Telegram is having internal problems. Please try again later"""
    ID = "USER_OCCUPY_PRIMARY_LOC_FAILED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class UserOccupyUsernameFailed(InternalServerError):
    """Failure to occupy USER username due to Telegram having internal problems. Please try again later"""
    ID = "USER_OCCUPY_USERNAME_FAILED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class MsgidDecreaseRetry(InternalServerError):
    """Telegram is having internal problems. Please try again later"""
    ID = "MSGID_DECREASE_RETRY"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class MsgRangeUnsync(InternalServerError):
    """Message range unsynchronized due to Telegram having internal problems. Please try again later"""
    ID = "MSG_RANGE_UNSYNC"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class MtSendQueueTooLong(InternalServerError):
    """The MTProto send queue has grown too much due to Telegram having internal problems. Please try again later"""
    ID = "MT_SEND_QUEUE_TOO_LONG"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class NeedChatInvalid(InternalServerError):
    """The provided chat is invalid"""
    ID = "NEED_CHAT_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class NeedUserInvalid(InternalServerError):
    """The provided USER is invalid or does not exist"""
    ID = "NEED_USER_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class NoWorkersRunning(InternalServerError):
    """The Telegram server is restarting its workers. Try again later."""
    ID = "No workers running"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class ParticipantCallFailed(InternalServerError):
    """Failure while making call due to Telegram having internal problems. Please try again later"""
    ID = "PARTICIPANT_CALL_FAILED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class PersistentTimestampOutdated(InternalServerError):
    """The persistent timestamp is outdated due to Telegram having internal problems. Please try again later"""
    ID = "PERSISTENT_TIMESTAMP_OUTDATED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class PhotoCreateFailed(InternalServerError):
    """The creation of the photo failed due to Telegram having internal problems. Please try again later"""
    ID = "PHOTO_CREATE_FAILED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class PostponedTimeout(InternalServerError):
    """Telegram is having internal problems. Please try again later"""
    ID = "POSTPONED_TIMEOUT"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class PtsChangeEmpty(InternalServerError):
    """No PTS change"""
    ID = "PTS_CHANGE_EMPTY"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class RandomIdDuplicate(InternalServerError):
    """You provided a random ID that was already used"""
    ID = "RANDOM_ID_DUPLICATE"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class RegIdGenerateFailed(InternalServerError):
    """The registration id failed to generate due to Telegram having internal problems. Please try again later"""
    ID = "REG_ID_GENERATE_FAILED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class RpcCallFail(InternalServerError):
    """Telegram is having internal problems. Please try again later"""
    ID = "RPC_CALL_FAIL"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class RpcConnectFailed(InternalServerError):
    """Telegram is having internal problems. Please try again later"""
    ID = "RPC_CONNECT_FAILED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class RpcMcExtractFail(InternalServerError):
    """Telegram is having internal problems. Please try again later"""
    ID = "RPC_MCExtract_FAIL"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class SignInFailed(InternalServerError):
    """Failure while signing in due to Telegram having internal problems. Please try again later"""
    ID = "SIGN_IN_FAILED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class StorageCheckFailed(InternalServerError):
    """Server storage check failed due to Telegram having internal problems. Please try again later"""
    ID = "STORAGE_CHECK_FAILED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class StoreInvalidScalarType(InternalServerError):
    """Telegram is having internal problems. Please try again later"""
    ID = "STORE_INVALID_SCALAR_TYPE"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class UnknownMethod(InternalServerError):
    """The method you tried to call cannot be called on non-CDN DCs"""
    ID = "UNKNOWN_METHOD"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class UploadNoVolume(InternalServerError):
    """Telegram is having internal problems. Please try again later"""
    ID = "UPLOAD_NO_VOLUME"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class VolumeLocNotFound(InternalServerError):
    """Telegram is having internal problems. Please try again later"""
    ID = "VOLUME_LOC_NOT_FOUND"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class WorkerBusyTooLongRetry(InternalServerError):
    """Server workers are too busy right now due to Telegram having internal problems. Please try again later"""
    ID = "WORKER_BUSY_TOO_LONG_RETRY"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


class WpIdGenerateFailed(InternalServerError):
    """Telegram is having internal problems. Please try again later"""
    ID = "WP_ID_GENERATE_FAILED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__


