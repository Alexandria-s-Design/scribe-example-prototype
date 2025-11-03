"""
Cell Collective API Wrapper
Kid-friendly interface for Cell Collective Teaching Platform
"""

import requests
from typing import Dict, List, Optional, Any


class CellCollectiveAPI:
    """
    Python wrapper for Cell Collective Teaching Platform API

    Based on reverse-engineered API from teach.cellcollective.org
    """

    def __init__(self, base_url: str = "https://teach.cellcollective.org"):
        """Initialize API wrapper"""
        self.base_url = base_url
        self.session = requests.Session()
        self.token = None
        self.user_profile = None
        self.headers = {}

    # ========== Authentication ==========

    def set_token(self, token: str):
        """
        Set authentication token (cookie-based)

        Args:
            token: Session cookie value (connect.sid or full cookie string)
        """
        # Clean token if user copied full cookie string
        if 'connect.sid=' in token:
            # Extract just the value: "connect.sid=s%3A..." -> "s%3A..."
            token = token.split('connect.sid=')[1].split(';')[0]

        self.token = token

        # Cell Collective uses cookie-based auth
        # We need to send it as a Cookie header, not using session.cookies
        # because requests doesn't send domain-specific cookies correctly
        self.headers['Cookie'] = f'connect.sid={token}'

        print(f"[DEBUG] Token set: {token[:20]}... (length: {len(token)})")
        print(f"[DEBUG] Will send Cookie header: connect.sid={token[:20]}...")

    def get_profile(self) -> Optional[Dict[str, Any]]:
        """
        Get current user profile

        Returns:
            User profile data or None if not authenticated
        """
        print(f"[DEBUG] Getting profile from {self.base_url}/v1/users/profile/me")
        print(f"[DEBUG] Using token: {self.token[:20] if self.token else 'None'}...")
        print(f"[DEBUG] Sending headers: {self.headers}")

        response = self.session.get(f"{self.base_url}/v1/users/profile/me", headers=self.headers)

        print(f"[DEBUG] Profile response status: {response.status_code}")
        if response.status_code != 200:
            print(f"[DEBUG] Profile response text: {response.text[:200]}")

        if response.status_code == 200:
            self.user_profile = response.json()
            return self.user_profile

        return None

    # ========== Initialize Application ==========

    def initialize(self) -> Dict[str, Any]:
        """
        Initialize application and get all metadata

        Returns:
            definitionMap, metadataValueRangeMap, modelDomainAccessList, etc.
        """
        response = self.session.get(f"{self.base_url}/web/_api/initialize")

        if response.status_code == 200:
            return response.json()

        return {}

    # ========== Model Discovery ==========

    def get_model_counts(self, model_types: str = "BiologicalModel") -> Dict[str, int]:
        """
        Get count of available models

        Args:
            model_types: Type of models (default: BiologicalModel)

        Returns:
            Dict with counts: {shared, workspace, published, my}
        """
        response = self.session.get(
            f"{self.base_url}/web/_api/model/cards/count/teaching",
            params={"modelTypes": model_types}
        )

        if response.status_code == 200:
            return response.json()

        return {}

    def get_model_ids(self, model_types: str = "BiologicalModel") -> Dict[str, List[int]]:
        """
        Get IDs of all available models

        Args:
            model_types: Type of models

        Returns:
            Dict with ID lists: {shared, published, my}
        """
        response = self.session.get(
            f"{self.base_url}/web/_api/model/cards/ids/teaching",
            params={"modelTypes": model_types}
        )

        if response.status_code == 200:
            return response.json()

        return {}

    def get_model_cards(self, model_ids: List[int]) -> List[Dict[str, Any]]:
        """
        Get card data for multiple models

        Args:
            model_ids: List of model IDs

        Returns:
            List of model card data
        """
        # Join IDs with comma
        id_string = ",".join(str(id) for id in model_ids)

        response = self.session.get(
            f"{self.base_url}/web/api/model/cards/teaching",
            params={"id": id_string}
        )

        if response.status_code == 200:
            data = response.json()
            if "data" in data:
                return data["data"]

        return []

    # ========== Model Data ==========

    def get_model(
        self,
        model_id: int,
        version: int = 1,
        slim: bool = False,
        domain: str = "teaching",
        model_type: str = "BiologicalModel"
    ) -> Optional[Dict[str, Any]]:
        """
        Get complete model data

        Args:
            model_id: Model ID
            version: Model version (default: 1)
            slim: Return slim data (default: False)
            domain: Domain (default: teaching)
            model_type: Model type (default: BiologicalModel)

        Returns:
            Complete model data including components and relationships
        """
        params = {
            "slim": str(slim).lower(),
            "domain": domain,
            "modeltype": model_type
        }

        url = f"{self.base_url}/web/api/model/{model_id}/version/{version}"
        print(f"[DEBUG] Getting model from {url}")
        print(f"[DEBUG] Params: {params}")
        print(f"[DEBUG] Using token: {self.token[:20] if self.token else 'None'}...")
        print(f"[DEBUG] Sending headers: {self.headers}")

        response = self.session.get(url, params=params, headers=self.headers)

        print(f"[DEBUG] Model response status: {response.status_code}")
        if response.status_code != 200:
            print(f"[DEBUG] Model response text: {response.text[:200]}")

        if response.status_code == 200:
            data = response.json()
            if "data" in data:
                model_data = data["data"]
                print(f"[DEBUG] Model components: {len(model_data.get('externalComponentSet', []))}")
                print(f"[DEBUG] Model relationships: {len(model_data.get('relationshipSet', []))}")
                return model_data

        return None

    def download_model_image(self, token: str) -> Optional[bytes]:
        """
        Download model visualization image

        Args:
            token: Download token

        Returns:
            PNG image bytes or None
        """
        response = self.session.get(
            f"{self.base_url}/web/_api/model/download",
            params={"token": token}
        )

        if response.status_code == 201:
            return response.content

        return None

    # ========== Courses ==========

    def get_courses(self) -> List[Dict[str, Any]]:
        """
        Get list of courses user has access to

        Returns:
            List of course data
        """
        response = self.session.get(f"{self.base_url}/web/api/course/")

        if response.status_code == 200:
            data = response.json()
            if "data" in data:
                return data["data"]

        return []

    # ========== User Lookup ==========

    def lookup_users(self, user_ids: List[int]) -> Dict[str, Any]:
        """
        Look up user information by IDs

        Args:
            user_ids: List of user IDs

        Returns:
            Dict mapping user IDs to user data
        """
        id_string = ",".join(str(id) for id in user_ids)

        response = self.session.get(
            f"{self.base_url}/web/_api/user/lookupUsers",
            params={"id": id_string}
        )

        if response.status_code == 200:
            return response.json()

        return {}

    # ========== Kid-Friendly Helpers ==========

    def list_all_models(self) -> List[Dict[str, Any]]:
        """
        Kid-friendly: Get all models user can see

        Returns:
            List of all available model cards
        """
        # Get all model IDs
        model_ids_dict = self.get_model_ids()

        # Combine all ID lists
        all_ids = []
        for id_list in model_ids_dict.values():
            if isinstance(id_list, list):
                all_ids.extend(id_list)

        # Get card data for all IDs
        if all_ids:
            return self.get_model_cards(all_ids)

        return []

    def get_model_details(self, model_id: int) -> Dict[str, Any]:
        """
        Kid-friendly: Get everything about a model

        Args:
            model_id: The model to get

        Returns:
            Complete model information
        """
        model_data = self.get_model(model_id)

        if model_data:
            return {
                "id": model_id,
                "name": model_data.get("name", "Unknown"),
                "description": model_data.get("description", ""),
                "components": model_data.get("externalComponentSet", []),
                "relationships": model_data.get("relationshipSet", []),
                "metadata": model_data.get("metadataPropertyMap", {}),
                "version": model_data.get("version", 1)
            }

        return {}


# ========== Example Usage ==========

if __name__ == "__main__":
    # Initialize API
    api = CellCollectiveAPI()

    # Set authentication token (you'll get this from login)
    # api.set_token("your_jwt_token_here")

    # Get user profile
    # profile = api.get_profile()
    # print(f"User: {profile.get('data', {}).get('firstName')}")

    # Get all available models
    # models = api.list_all_models()
    # print(f"Found {len(models)} models")

    # Get specific model details
    # model = api.get_model_details(295828)
    # print(f"Model: {model.get('name')}")
    # print(f"Components: {len(model.get('components', []))}")

    print("Cell Collective API Wrapper initialized!")
    print("Set token with: api.set_token('your_jwt_token')")
    print("Then call methods like: api.list_all_models()")
