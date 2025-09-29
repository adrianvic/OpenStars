from Protocol.Messages.Client.EndClientTurnMessage import EndClientTurnMessage
from Protocol.Messages.Client.LoginMessage import LoginMessage
from Protocol.Messages.Client.KeepAliveMessage import KeepAliveMessage
from Protocol.Messages.Client.SetNameMessage import SetNameMessage
from Protocol.Messages.Client.TeamCreateMessage import TeamCreateMessage
from Protocol.Messages.Client.TeamLeaveMessage import TeamLeaveMessage
from Protocol.Messages.Client.TeamChangeMemberSettingsMessage import TeamChangeMemberSettingsMessage
from Protocol.Messages.Client.TeamToggleSettingsMessage import TeamToggleSettingsMessage
from Protocol.Messages.Client.TeamSetLocationMessage import TeamSetLocationMessage
from Protocol.Messages.Client.GoHomeFromOfflinePractiseMessage import GoHomeFromOfflinePractiseMessage
from Protocol.Messages.Client.StartGameMessage import StartGameMessage
from Protocol.Messages.Client.GetPlayerProfileMessage import GetPlayerProfileMessage
from Protocol.Messages.Client.GetLeaderboardMessage import GetLeaderboardMessage
from Protocol.Messages.Client.SetSupportedCreatorMessage import SetSupportedCreatorMessage
from Protocol.Messages.Client.AskForBattleEndMessage import AskForBattleEndMessage
from Protocol.Messages.Client.AvatarNameCheckRequestMessage import AvatarNameCheckRequestMessage
from Protocol.Messages.Client.CreateAllianceMessage import CreateAllianceMessage
from Protocol.Messages.Client.AskForAllianceDataMessage import AskForAllianceDataMessage
from Protocol.Messages.Client.ChangeAllianceSettingsMessage import ChangeAllianceSettingsMessage
from Protocol.Messages.Client.JoinAllianceMessage import JoinAllianceMessage
from Protocol.Messages.Client.AskForJoinableAlliancesListMessage import AskForJoinableAlliancesListMessage
from Protocol.Messages.Client.LeaveAllianceMessage import LeaveAllianceMessage
from Protocol.Messages.Client.SearchAlliancesMessage import SearchAlliancesMessage
from Protocol.Messages.Client.ChatToAllianceStreamMessage import ChatToAllianceStreamMessage
from Protocol.Messages.Client.PlayerStatusMessage import PlayerStatusMessage
from Protocol.Messages.Client.AnalyticEventMessage import AnalyticEventMessage
from Protocol.Messages.Client.ClientCapabilitiesMessage import ClientCapabilitiesMessage
from Protocol.Messages.Client.TeamMemberStatusMessage import TeamMemberStatusMessage
from Protocol.Messages.Client.GetSeasonRewardsMessage import GetSeasonRewardsMessage
from Protocol.Messages.Client.ChronosEventSeenMessage import ChronosEventSeenMessage

packets = {
    14166: ChronosEventSeenMessage,
    14277: GetSeasonRewardsMessage,
    14361: TeamMemberStatusMessage,
    10107: ClientCapabilitiesMessage,
    10110: AnalyticEventMessage,
    10101: LoginMessage,
    14103: StartGameMessage,
    10108: KeepAliveMessage,
    10212: SetNameMessage,
    14102: EndClientTurnMessage,
    14109: GoHomeFromOfflinePractiseMessage,
    14110: AskForBattleEndMessage,
    14113: GetPlayerProfileMessage,
    14301: CreateAllianceMessage,
    14302: AskForAllianceDataMessage,
    14303: AskForJoinableAlliancesListMessage,
    14305: JoinAllianceMessage,
    14308: LeaveAllianceMessage,
    14315: ChatToAllianceStreamMessage,
    14316: ChangeAllianceSettingsMessage,
    14324: SearchAlliancesMessage,
    14350: TeamCreateMessage,
    14353: TeamLeaveMessage,
    14354: TeamChangeMemberSettingsMessage,
    14363: TeamSetLocationMessage,
    14372: TeamToggleSettingsMessage,
    14403: GetLeaderboardMessage,
    14600: AvatarNameCheckRequestMessage,
    18686: SetSupportedCreatorMessage,
    14366: PlayerStatusMessage
}
