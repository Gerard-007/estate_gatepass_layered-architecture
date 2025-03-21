from abc import ABC, abstractmethod


class IRepository(ABC):
    @abstractmethod
    def get_user_by_email(self, email: str) -> dict:
        pass

    @abstractmethod
    def insert_user(self, user_data: dict) -> str:
        pass

    @abstractmethod
    def delete_tokens(self, resident_id: str) -> None:
        pass

    @abstractmethod
    def find_token_by_id(self, token_id: str) -> dict:
        pass

    @abstractmethod
    def invalidate_token(self, token_id: str) -> None:
        pass

    @abstractmethod
    def insert_token(self, token_data: dict) -> str:
        pass
