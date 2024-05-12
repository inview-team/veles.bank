from typing import Protocol, Annotated
from uuid import UUID
import secrets

from fastapi import Depends, HTTPException

from src.apps.company.repository import CompanyRepositoryProtocol, CompanyRepository
from src.apps.company.utils import rebuild_phone_number
from src.apps.user.repository import UserRepositoryProtocol, UserRepository
from src.apps.user.schema import UserReadSchema
from src.apps.wallet.repository import WalletRepositoryProtocol, WalletRepository
from src.apps.wallet.schema import WalletReadSchema, WalletCreateSchema, WalletSearchSchema, WalletResponseSchema, \
    WalletMeSchema


class WalletServiceProtocol(Protocol):
    """
    Account service protocol
    """

    async def get_by_holder_id(self, holder_id: UUID) -> WalletReadSchema:
        ...

    async def get_all_wallets(self, user_id: UUID) -> WalletReadSchema:
        ...

    async def get_by_user_and_wallet_id(self, user_id: UUID, wallet_id: UUID) -> WalletMeSchema:
        ...

    async def create(self, user: UserReadSchema) -> WalletReadSchema:
        ...

    async def get_wallet_by_value(self, params: WalletSearchSchema) -> WalletResponseSchema | None:
        ...


class WalletServiceImpl(WalletServiceProtocol):
    """
    Account service
    """

    def __init__(
        self,
        wallet_repository: WalletRepositoryProtocol,
        user_repository: UserRepositoryProtocol,
        company_repository: CompanyRepositoryProtocol
    ):
        self.wallet_repository = wallet_repository
        self.user_repository = user_repository
        self.company_repository = company_repository

    async def get_all_wallets(self, user_id: UUID) -> WalletReadSchema:
        """
        Get all accounts
        :param user_id:
        :return:
        """

        return await self.wallet_repository.first(user_id)

    async def get_by_user_and_wallet_id(self, user_id: UUID, wallet_id: UUID) -> WalletMeSchema:
        """
        Get wallet by user id and wallet id
        :param wallet_id:
        :param user_id: UUID
        :return: AccountReadSchema | None
        """

        wallet = await self.wallet_repository.get_by_user_and_account_id(user_id, wallet_id)
        if not wallet:
            raise HTTPException(status_code=404, detail="Wallet not found")
        holder_id = wallet.user_id if wallet.user_id else wallet.company_id
        return WalletMeSchema(holder_id=holder_id, **wallet.model_dump(exclude={"company_id", "user_id"}))

    async def create(self, user: UserReadSchema) -> WalletReadSchema:
        wallet_dto = WalletCreateSchema(
            balance=0.0, type="debet",
            number=str(secrets.randbelow(10 ** 16)),
            status=True, user_id=user.id,
            company_id=None,
        )
        return await self.wallet_repository.create(wallet_dto)

    async def get_wallet_by_value(self, params: WalletSearchSchema) -> WalletResponseSchema | None:
        if params.type == "phone":
            phone_number = await rebuild_phone_number(params.value)
            user = (await self.user_repository.get_user_by_phone_number(phone_number))
            if not user:
                raise HTTPException(status_code=404, detail="User with these phone_number not found")
            wallet = await self.wallet_repository.get_by_user_id(user.id)
            if not wallet:
                raise HTTPException(status_code=404, detail="Wallet with these user not found")
            return WalletResponseSchema(holder_id=wallet.id, **wallet.model_dump(exclude={"company_id", "user_id"}))
        elif params.type == "company":
            company = (await self.company_repository.get_by_name(params.value))
            if not company:
                raise HTTPException(status_code=404, detail="Company with these name not found")
            wallet = await self.wallet_repository.get_by_company_id(company.id)
            if not wallet:
                raise HTTPException(status_code=404, detail="Wallet with these company not found")
            return WalletResponseSchema(holder_id=wallet.id, **wallet.model_dump(exclude={"company_id", "user_id"}))
        return None

    async def get_by_holder_id(self, holder_id: UUID) -> WalletReadSchema:
        return await self.wallet_repository.first(holder_id)


async def get_account_service(
    wallet_repository: WalletRepository,
    user_repository: UserRepository,
    company_repository: CompanyRepository,
) -> WalletServiceProtocol:
    return WalletServiceImpl(wallet_repository, user_repository, company_repository)


WalletService = Annotated[WalletServiceProtocol, Depends(get_account_service)]
