from typing import Protocol, Any
from agent.domain.schemas.hitl import DecisionCard, HitlEvent

class WebviewHost(Protocol):
    """
    Protocol for communicating with the Frontend (VS Code Webview).
    
    @TestScenarios
    1. Send Card:
       - Input: DecisionCard object.
       - Expected: Connection verified, message sent.
       
    2. Wait for Response:
       - Input: Card ID.
       - Expected: Blocks/Suspends until HitlEvent received or Timeout.
    """
    
    async def send_card(self, card: DecisionCard) -> None:
        """Push a decision card to the user interface."""
        ...
        
    async def wait_for_decision(self, card_id: str, timeout: int = 300) -> HitlEvent:
        """Wait for the user's interaction with a specific card."""
        ...
