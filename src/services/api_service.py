"""API service for fetching collectibles data"""

import asyncio
import json
from datetime import datetime
from pathlib import Path
from typing import List

from loguru import logger

from ..models.collectible import Collectible
from ..utils.network import NetworkClient


class ApiService:
    """Service for interacting with CS:GO collectibles API"""

    def __init__(self, base_url: str, timeout: int = 30, max_retries: int = 3):
        """Initialize API service

        Args:
            base_url: Base URL for the API
            timeout: Request timeout in seconds
            max_retries: Maximum number of retry attempts
        """
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries
        self.network_client = NetworkClient(
            timeout=timeout, max_retries=max_retries
        )

    async def fetch_collectibles(self) -> List[Collectible]:
        """Fetch all collectibles from the API

        Returns:
            List of Collectible objects

        Raises:
            Exception: If API request fails
        """
        logger.info(f"Fetching collectibles from {self.base_url}")

        try:
            session = self.network_client.create_session()
            response = session.get(self.base_url, timeout=self.timeout)
            response.raise_for_status()

            raw_data = response.json()
            logger.info(
                f"Successfully fetched {len(raw_data)} raw collectibles"
            )

            # Convert to Pydantic models
            collectibles = []
            for item_data in raw_data:
                try:
                    collectible = Collectible(**item_data)
                    collectibles.append(collectible)
                except Exception as e:
                    item_id = item_data.get('id', 'unknown')
                    logger.warning(
                        f"Failed to parse collectible {item_id}: {e}"
                    )
                    continue

            logger.info(
                f"Successfully parsed {len(collectibles)} collectibles"
            )
            return collectibles

        except Exception as e:
            logger.error(f"Failed to fetch collectibles: {e}")
            raise

    def fetch_collectibles_sync(self) -> List[Collectible]:
        """Synchronous version of fetch_collectibles"""
        return asyncio.run(self.fetch_collectibles())

    def dump_collectibles(
        self, collectibles: List[Collectible], dump_folder: Path
    ) -> Path:
        """Dump collectibles to JSON file

        Args:
            collectibles: List of collectibles to dump
            dump_folder: Directory to save the dump file

        Returns:
            Path to the created dump file
        """
        if not collectibles:
            raise ValueError("No collectibles to dump")

        # Ensure dump folder exists
        dump_folder.mkdir(parents=True, exist_ok=True)

        # Create filename with timestamp
        timestamp = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
        filename = f"collectibles_{timestamp}.json"
        filepath = dump_folder / filename

        try:
            # Convert Pydantic models to dict for JSON serialization
            data = [collectible.model_dump() for collectible in collectibles]

            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4, default=str)

            collectible_count = len(collectibles)
            logger.info(
                f"Dumped {collectible_count} collectibles to {filepath}"
            )
            return filepath

        except Exception as e:
            logger.error(f"Failed to dump collectibles: {e}")
            raise
