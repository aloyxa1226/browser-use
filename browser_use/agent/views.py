from __future__ import annotations

from typing import Optional, Type, Union, List, Dict, Any

from openai import RateLimitError
from pydantic import BaseModel, ConfigDict, Field, ValidationError, create_model

from browser_use.browser.views import BrowserState
from browser_use.controller.registry.views import ActionModel
from browser_use.extensions.integration import ExtensionsManager

class TokenDetails(BaseModel):
    audio: int = 0
    cache_read: int = 0
    reasoning: int = 0


class TokenUsage(BaseModel):
    input_tokens: int
    output_tokens: int
    total_tokens: int
    input_token_details: TokenDetails = Field(default=TokenDetails())
    output_token_details: TokenDetails = Field(default=TokenDetails())

    # allow arbitrary types
    model_config = ConfigDict(arbitrary_types_allowed=True)


class Pricing(BaseModel):
    uncached_input: float  # per 1M tokens
    cached_input: float
    output: float


class ModelPricingCatalog(BaseModel):
    gpt_4o: Pricing = Field(default=Pricing(uncached_input=2.50, cached_input=1.25, output=10.00))
    gpt_4o_mini: Pricing = Field(
        default=Pricing(uncached_input=0.15, cached_input=0.075, output=0.60)
    )
    claude_3_5_sonnet: Pricing = Field(
        default=Pricing(uncached_input=3.00, cached_input=1.50, output=15.00)
    )


class ActionResult(BaseModel):
    """Result of executing an action"""

    is_done: Optional[bool] = False
    extracted_content: Optional[str] = None
    error: Optional[str] = None


class AgentBrain(BaseModel):
    """Agent brain state and functionality."""
    
    browser: Optional[Browser] = Field(default=None, description="Browser instance")
    extensions: Optional[ExtensionsManager] = Field(default=None, description="Extensions manager")
    current_state: Optional[BrowserState] = Field(default=None, description="Current browser state")
    conversation_history: List[Dict[str, Any]] = Field(default_factory=list, description="Conversation history")
    valuation_previous_goal: str
    memory: str
    next_goal: str
    
    class Config:
        arbitrary_types_allowed = True
        
    async def update_state(self) -> None:
        """Update the current browser state."""
        if not self.browser or not self.browser.page:
            logger.warning("Browser or page not available")
            return
            
        try:
            self.current_state = BrowserState(
                url=self.browser.page.url,
                title=await self.browser.page.title(),
                html=await self.browser.page.content(),
                text=await self.browser.page.inner_text("body")
            )
        except Exception as e:
            logger.error(f"Error updating state: {str(e)}")
            
    def add_to_history(self, message: Dict[str, Any]) -> None:
        """Add a message to the conversation history."""
        self.conversation_history.append(message)


class AgentOutput(BaseModel):
    """Output model for agent

    @dev note: this model is extended with custom actions in AgentService. You can also use some fields that are not in this model as provided by the linter, as long as they are registered in the DynamicActions model.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    current_state: AgentBrain
    action: ActionModel

    @staticmethod
    def type_with_custom_actions(custom_actions: Type[ActionModel]) -> Type['AgentOutput']:
        """Extend actions with custom actions"""
        return create_model(
            'AgentOutput',
            __base__=AgentOutput,
            action=(custom_actions, Field(...)),  # Properly annotated field with no default
            __module__=AgentOutput.__module__,
        )


class AgentHistory(BaseModel):
    """History item for agent actions"""

    model_output: AgentOutput | None
    result: ActionResult
    state: BrowserState

    model_config = ConfigDict(arbitrary_types_allowed=True, protected_namespaces=())


class AgentError:
    """Container for agent error handling"""

    VALIDATION_ERROR = 'Invalid model output format. Please follow the correct schema.'
    RATE_LIMIT_ERROR = 'Rate limit reached. Waiting before retry.'
    NO_VALID_ACTION = 'No valid action found'

    @staticmethod
    def format_error(error: Exception) -> str:
        """Format error message based on error type"""
        if isinstance(error, ValidationError):
            return f'{AgentError.VALIDATION_ERROR}\nDetails: {str(error)}'
        if isinstance(error, RateLimitError):
            return AgentError.RATE_LIMIT_ERROR
        return f'Unexpected error: {str(error)}'
