from typing import List

from application.usecases.create_meet_usecase import CreateMeetResponseOutput
from application.usecases.get_meet_by_hash_usecase import GetMeetByHashResponseOutput
from application.usecases.list_meets_usecase import ListMeetsResponseOutput, ListMeetsItemData
from application.usecases.list_user_invitations_usecase import ListUserInvitationsResponseOutput, ListUserInvitationsItemData
from application.usecases.list_user_managed_meets_usecase import ListUserManagedMeetsResponseOutput, ListUserManagedMeetsItemData
from application.usecases.update_meet_usecase import UpdateMeetResponseOutput
from application.usecases.delete_meet_usecase import DeleteMeetResponseOutput
from presentation.dto.create_meet_dto import MeetResponseData
from presentation.dto.meet_dto import MeetDetailData, MeetListItemData
from presentation.dto.base_dto import MutationResponseDTO, SingleResponseDTO, PaginatedResponseDTO


class MeetPresenter:
    @staticmethod
    def format_create_response(dto: CreateMeetResponseOutput) -> MutationResponseDTO[MeetResponseData]:
        data = MeetResponseData(
            id=dto.id,
            title=dto.title,
            meet_hash=dto.meet_hash,
            start_time=dto.start_time,
            expires_at=dto.expires_at,
            creator_id=dto.creator_id,
        )

        print(f"Formatted CreateMeetResponseOutput: {data}")
        return MutationResponseDTO(
            data=data,
            message="Meeting created successfully.",
        )

    @staticmethod
    def format_single_meet_response(dto: GetMeetByHashResponseOutput) -> SingleResponseDTO[MeetDetailData]:
        data = MeetDetailData(
            id=dto.id,
            title=dto.title,
            meet_hash=dto.meet_hash,
            start_time=dto.start_time,
            expires_at=dto.expires_at,
            creator_id=dto.creator_id,
            is_active=dto.is_active,
            participant_ids=dto.participant_ids,
            created_at=dto.created_at,
            updated_at=dto.updated_at,
        )
        return SingleResponseDTO(
            data=data,
            permissions=[],
        )

    @staticmethod
    def _build_list_items(items):
        return [
            MeetListItemData(
                id=item.id,
                title=item.title,
                meet_hash=item.meet_hash,
                start_time=item.start_time,
                expires_at=item.expires_at,
                creator_id=item.creator_id,
                is_active=item.is_active,
                participant_count=item.participant_count,
            )
            for item in items
        ]

    @staticmethod
    def format_list_meets_response(dto: ListMeetsResponseOutput) -> PaginatedResponseDTO[MeetListItemData]:
        items = MeetPresenter._build_list_items(dto.items)
        total_pages = max(1, (dto.total + dto.size - 1) // dto.size)
        return PaginatedResponseDTO(
            data=items,
            total=dto.total,
            current_page=dto.page,
            pages=total_pages,
            is_next=dto.page < total_pages,
            is_prev=dto.page > 1,
            size=dto.size,
            permissions=[],
        )

    @staticmethod
    def format_update_response(dto: UpdateMeetResponseOutput) -> MutationResponseDTO[MeetDetailData]:
        data = MeetDetailData(
            id=dto.id,
            title=dto.title,
            meet_hash=dto.meet_hash,
            start_time=dto.start_time,
            expires_at=dto.expires_at,
            creator_id=dto.creator_id,
            is_active=dto.is_active,
            participant_ids=dto.participant_ids,
            created_at=dto.created_at,
            updated_at=dto.updated_at,
        )
        return MutationResponseDTO(
            data=data,
            message="Meeting updated successfully.",
        )

    @staticmethod
    def format_delete_response(dto: DeleteMeetResponseOutput) -> MutationResponseDTO:
        return MutationResponseDTO(
            data={"meet_hash": dto.meet_hash},
            message="Meeting deleted successfully.",
        )

    @staticmethod
    def format_invitations_response(dto: ListUserInvitationsResponseOutput) -> PaginatedResponseDTO[MeetListItemData]:
        items = MeetPresenter._build_list_items(dto.items)
        total_pages = max(1, (dto.total + dto.size - 1) // dto.size)
        return PaginatedResponseDTO(
            data=items,
            total=dto.total,
            current_page=dto.page,
            pages=total_pages,
            is_next=dto.page < total_pages,
            is_prev=dto.page > 1,
            size=dto.size,
            permissions=[],
        )

    @staticmethod
    def format_managed_meets_response(dto: ListUserManagedMeetsResponseOutput) -> PaginatedResponseDTO[MeetListItemData]:
        items = MeetPresenter._build_list_items(dto.items)
        total_pages = max(1, (dto.total + dto.size - 1) // dto.size)
        return PaginatedResponseDTO(
            data=items,
            total=dto.total,
            current_page=dto.page,
            pages=total_pages,
            is_next=dto.page < total_pages,
            is_prev=dto.page > 1,
            size=dto.size,
            permissions=[],
        )
