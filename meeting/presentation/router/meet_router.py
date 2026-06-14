from fastapi import APIRouter, Depends

from domain.entity.user_entity import User
from application.usecases.create_meet_usecase import CreateMeetRequestInput, CreateMeetUseCase
from application.usecases.get_meet_by_hash_usecase import GetMeetByHashRequestInput, GetMeetByHashUseCase
from application.usecases.list_meets_usecase import ListMeetsRequestInput, ListMeetsUseCase
from application.usecases.update_meet_usecase import UpdateMeetRequestInput, UpdateMeetUseCase
from application.usecases.delete_meet_usecase import DeleteMeetRequestInput, DeleteMeetUseCase
from presentation.dto.create_meet_dto import CreateMeetRequestDTO, MeetResponseData
from presentation.dto.meet_dto import ListMeetsQueryDTO, UpdateMeetRequestDTO, MeetDetailData, MeetListItemData
from presentation.dto.base_dto import MutationResponseDTO, SingleResponseDTO, PaginatedResponseDTO
from presentation.presenter.meet_presenter import MeetPresenter
from presentation.dependencies.auth_stub import get_current_user_stub


router = APIRouter(prefix="/meets", tags=["Meets"])


def create_meet_use_case_stub() -> CreateMeetUseCase:
    raise NotImplementedError("This dependency must be overridden by the Composition Root.")


def get_meet_by_hash_use_case_stub() -> GetMeetByHashUseCase:
    raise NotImplementedError("This dependency must be overridden by the Composition Root.")


def list_meets_use_case_stub() -> ListMeetsUseCase:
    raise NotImplementedError("This dependency must be overridden by the Composition Root.")


def update_meet_use_case_stub() -> UpdateMeetUseCase:
    raise NotImplementedError("This dependency must be overridden by the Composition Root.")


def delete_meet_use_case_stub() -> DeleteMeetUseCase:
    raise NotImplementedError("This dependency must be overridden by the Composition Root.")


@router.post("", response_model=MutationResponseDTO[MeetResponseData])
def create_meet(
    request: CreateMeetRequestDTO,
    current_user: User = Depends(get_current_user_stub),
    use_case: CreateMeetUseCase = Depends(create_meet_use_case_stub),
):
    dto_request = CreateMeetRequestInput(
        actor_id=current_user.id,
        actor_role=current_user.role,
        title=request.title,
        start_time=request.start_time,
        expires_at=request.expires_at,
        guest_usernames=request.guest_usernames,
        assign_to_username=request.assign_to_username,
    )
    dto_response = use_case.execute(dto_request)
    return MeetPresenter.format_create_response(dto_response)


@router.get("/{meet_hash}", response_model=SingleResponseDTO[MeetDetailData])
def get_meet_by_hash(
    meet_hash: str,
    current_user: User = Depends(get_current_user_stub),
    use_case: GetMeetByHashUseCase = Depends(get_meet_by_hash_use_case_stub),
):
    dto_request = GetMeetByHashRequestInput(
        meet_hash=meet_hash,
        actor_id=current_user.id,
        actor_role=current_user.role,
    )
    dto_response = use_case.execute(dto_request)
    return MeetPresenter.format_single_meet_response(dto_response)


@router.get("", response_model=PaginatedResponseDTO[MeetListItemData])
def list_meets(
    query: ListMeetsQueryDTO = Depends(),
    current_user: User = Depends(get_current_user_stub),
    use_case: ListMeetsUseCase = Depends(list_meets_use_case_stub),
):
    dto_request = ListMeetsRequestInput(
        actor_id=current_user.id,
        actor_role=current_user.role,
        page=query.page,
        size=query.size,
        start_date=query.start_date,
        end_date=query.end_date,
        guest_username=query.guest_username,
        title_query=query.title_query,
    )
    dto_response = use_case.execute(dto_request)
    return MeetPresenter.format_list_meets_response(dto_response)


@router.put("/{meet_hash}", response_model=MutationResponseDTO[MeetDetailData])
def update_meet(
    meet_hash: str,
    request: UpdateMeetRequestDTO,
    current_user: User = Depends(get_current_user_stub),
    use_case: UpdateMeetUseCase = Depends(update_meet_use_case_stub),
):
    dto_request = UpdateMeetRequestInput(
        meet_hash=meet_hash,
        actor_id=current_user.id,
        actor_role=current_user.role,
        title=request.title,
        start_time=request.start_time,
        expires_at=request.expires_at,
        guest_usernames=request.guest_usernames,
        assign_to_username=request.assign_to_username,
    )
    dto_response = use_case.execute(dto_request)
    return MeetPresenter.format_update_response(dto_response)


@router.delete("/{meet_hash}", response_model=MutationResponseDTO)
def delete_meet(
    meet_hash: str,
    current_user: User = Depends(get_current_user_stub),
    use_case: DeleteMeetUseCase = Depends(delete_meet_use_case_stub),
):
    dto_request = DeleteMeetRequestInput(
        meet_hash=meet_hash,
        actor_id=current_user.id,
        actor_role=current_user.role,
    )
    dto_response = use_case.execute(dto_request)
    return MeetPresenter.format_delete_response(dto_response)
