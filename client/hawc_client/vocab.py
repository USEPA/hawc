from requests import Response

from .client import BaseClient


class VocabClient(BaseClient):
    """
    Client class for vocabulary requests.
    """

    def bulk_create(self, terms: list[dict]) -> list[dict]:
        """
        Bulk creates a list of terms.

        Args:
            terms (list[dict]): List of serialized terms.

        Returns:
            list[dict]: List of created, serialized terms.
        """
        url = f"{self.session.root_url}/vocab/api/term/bulk-create/"
        return self.session.post(url, terms).json()

    def bulk_update(self, terms: list[dict]) -> list[dict]:
        """
        Bulk updates a list of terms.

        Args:
            terms (list[dict]): List of serialized terms.

        Returns:
            list[dict]: List of updated, serialized terms.
        """
        url = f"{self.session.root_url}/vocab/api/term/bulk-update/"
        return self.session.patch(url, terms).json()

    def list_guidelines(self) -> list[dict]:
        """
        List all guidelines.

        Returns:
            list[dict]: Guideline data
        """
        url = f"{self.session.root_url}/vocab/api/guideline/"
        return self.session.get(url).json()

    def create_guideline(self, data: dict) -> dict:
        """
        Create a new guideline.

        Args:
            data (dict): required metadata

        Returns:
            dict: The created guideline
        """
        url = f"{self.session.root_url}/vocab/api/guideline/"
        return self.session.post(url, data).json()

    def update_guideline(self, guideline_id: int, data: dict) -> dict:
        """
        Update an existing guideline.

        Args:
            guideline_id (int): guideline ID
            data (dict): fields to update

        Returns:
            dict: The updated guideline
        """
        url = f"{self.session.root_url}/vocab/api/guideline/{guideline_id}/"
        return self.session.patch(url, data).json()

    def delete_guideline(self, guideline_id: int) -> Response:
        """
        Delete a guideline.

        Args:
            guideline_id (int): guideline ID

        Returns:
            Response: The response object.
        """
        url = f"{self.session.root_url}/vocab/api/guideline/{guideline_id}/"
        return self.session.delete(url)

    def list_guideline_profiles(self, guideline_id: int | None = None) -> list[dict]:
        """
        List all guideline profiles, optionally filtered by guideline.

        Args:
            guideline_id (int, optional): Filter by guideline ID

        Returns:
            list[dict]: GuidelineProfile data
        """
        url = f"{self.session.root_url}/vocab/api/guideline-profile/"
        params = {}
        if guideline_id is not None:
            params["guideline"] = guideline_id
        return self.session.get(url, params=params).json()

    def create_guideline_profile(self, data: dict) -> dict:
        """
        Create a new guideline profile.

        Args:
            data (dict): required metadata

        Returns:
            dict: The created guideline profile
        """
        url = f"{self.session.root_url}/vocab/api/guideline-profile/"
        return self.session.post(url, data).json()

    def update_guideline_profile(self, profile_id: int, data: dict) -> dict:
        """
        Update an existing guideline profile.

        Args:
            profile_id (int): guideline profile ID
            data (dict): fields to update

        Returns:
            dict: The updated guideline profile
        """
        url = f"{self.session.root_url}/vocab/api/guideline-profile/{profile_id}/"
        return self.session.patch(url, data).json()

    def delete_guideline_profile(self, profile_id: int) -> Response:
        """
        Delete a guideline profile.

        Args:
            profile_id (int): guideline profile ID

        Returns:
            Response: The response object.
        """
        url = f"{self.session.root_url}/vocab/api/guideline-profile/{profile_id}/"
        return self.session.delete(url)

    def uids(self) -> list[tuple[int, int]]:
        """
        Get all term ids and uids.

        Returns:
            list[tuple[int,int]]: List of id, uid tuples for all terms.
        """
        url = f"{self.session.root_url}/vocab/api/term/uids/"
        return self.session.get(url).json()
