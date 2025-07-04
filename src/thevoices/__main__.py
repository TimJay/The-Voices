#!/usr/bin/env python3
import os
from typing import List

from fastmcp import FastMCP
from fastmcp.exceptions import ToolError
from litellm import completion, model_list
from litellm.utils import get_llm_provider  # type: ignore

# Create the MCP server
mcp = FastMCP(name="TheVoicesServer")


@mcp.tool
def list_available_models() -> List[str]:
    """
    Returns a list of available LLM models based on detected API keys in the environment.

    Auto-discovers models from LiteLLM's model list and filters based on available API keys.

    Returns:
    List of model names in LiteLLM format (provider/model-name).
    """
    available_models = []

    # Define provider to API key mapping
    provider_key_mapping = {
        "openai": "OPENAI_API_KEY",
        "anthropic": "ANTHROPIC_API_KEY",
        "vertex_ai": ["VERTEXAI_PROJECT", "VERTEXAI_LOCATION"],  # Both needed
        "azure": ["AZURE_API_KEY", "AZURE_API_BASE"],  # Both needed
        "cohere": "COHERE_API_KEY",
        "huggingface": "HUGGINGFACE_API_KEY",
        "replicate": "REPLICATE_API_TOKEN",
        "together_ai": "TOGETHERAI_API_KEY",
        "openrouter": "OPENROUTER_API_KEY",
        "ai21": "AI21_API_KEY",
        "palm": "PALM_API_KEY",
        "bedrock": ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"],  # AWS credentials
        "sagemaker": ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"],  # AWS credentials
    }

    # Check which providers have API keys available
    available_providers = set()

    for provider, keys in provider_key_mapping.items():
        if isinstance(keys, list):
            # All keys in the list must be present
            if all(os.environ.get(key) for key in keys):
                available_providers.add(provider)
        else:
            # Single key must be present
            if os.environ.get(keys):
                available_providers.add(provider)

    # Filter models based on available providers
    for model in model_list:
        try:
            # Get provider for this model
            _, provider, _, _ = get_llm_provider(model)

            # Check if we have API keys for this provider
            if provider in available_providers:
                available_models.append(f"{provider}/{model}")
        except Exception:
            # Skip models that can't be processed
            continue

    # Add currently selected model if set
    current_model = os.environ.get("LITELLM_MODEL")
    if current_model:
        available_models.insert(0, current_model)

    # Sort alphabetically for better readability
    available_models.sort()

    return available_models


@mcp.tool
def ask_the_voice(
    role_title: str,
    role_description: str,
    context: str,
    task: str,
    model: str = None,
    temperature: float = None,
) -> str:
    """
    Role-based assistant tool for specialized AI personas and expert consultations.

    This tool creates focused AI assistants by defining specific roles, contexts, and tasks.
    It's designed to leverage the power of role-playing to get more targeted, expert-level
    responses from language models by establishing clear personas and domains of expertise.

    ## Core Concept
    Instead of generic AI responses, this tool creates specialized "voices" - AI personas
    with distinct expertise, perspectives, and communication styles. Each voice is tailored
    to specific domains, from technical analysis to creative ideation.

    ## Parameters

    ### role_title (str) - Required
    The name/title of the AI persona, preferably with a definite article for clarity.

    Examples:
    - "The Security Architect" - for cybersecurity analysis
    - "The UX Researcher" - for user experience insights
    - "The Data Scientist" - for statistical analysis
    - "The Creative Director" - for design and branding
    - "The Systems Analyst" - for technical architecture
    - "The Product Manager" - for feature prioritization

    ### role_description (str) - Required
    A concise but comprehensive description of the role's expertise, background, and approach.
    Should establish credibility and set expectations for the type of responses.

    Best practices:
    - Include relevant experience/background
    - Mention key skills and methodologies
    - Define the persona's communication style
    - Establish domain expertise boundaries

    Example: "A senior cybersecurity professional with 15+ years in enterprise security,
    specializing in threat modeling, risk assessment, and security architecture. Known for
    pragmatic, actionable advice that balances security with business needs."

    ### context (str) - Required
    Comprehensive background information for the task (can be long, up to 75% of the maximum context window).
    This is where you provide all relevant details, data, constraints, and background.

    Should include:
    - Current situation or problem statement
    - Relevant technical details or specifications
    - Business constraints or requirements
    - Previous attempts or existing solutions
    - Success criteria or desired outcomes
    - Any relevant data, logs, or documentation

    ### task (str) - Required
    The specific request or question you want the AI persona to address.
    Should be clear, actionable, and aligned with the role's expertise.

    Examples:
    - "Analyze this security incident and provide a remediation plan"
    - "Design a user research study for our new mobile app feature"
    - "Review this architecture proposal and identify potential issues"
    - "Develop a go-to-market strategy for our B2B SaaS product"

    ### model (str) - Optional
    Override the default LLM model. Use format: "provider/model-name"
    Use the `list_available_models` tool before using this.

    Examples:
    - "openai/gpt-4-turbo-preview" - For complex reasoning tasks
    - "anthropic/claude-3-sonnet-20240229" - For detailed analysis
    - "openai/gpt-3.5-turbo" - For faster, cost-effective responses

    If not specified, uses the LITELLM_MODEL environment variable.

    ### temperature (float) - Optional
    Controls response creativity and randomness (0.0-2.0).

    Guidelines:
    - 0.0-0.3: Highly deterministic, factual responses (technical analysis, code review)
    - 0.4-0.7: Balanced creativity and consistency (general consulting, planning)
    - 0.8-1.2: More creative and varied responses (brainstorming, creative writing)
    - 1.3-2.0: Highly creative, experimental responses (artistic concepts, innovation)

    ## Returns
    str: The AI persona's response as a plain string, formatted according to the role's
    expertise and communication style.

    ## Usage Examples

    ### Technical Code Review
    ```python
    response = ask_the_voice(
        role_title="The Senior Software Architect",
        role_description="A seasoned software architect with expertise in scalable systems,
            clean code principles, and performance optimization. Provides detailed technical
            reviews with actionable recommendations.",
        context="We're reviewing a new microservice written in Python using FastAPI...",
        task="Review this code for scalability, security, and maintainability issues.",
        temperature=0.2
    )
    ```

    ### Business Strategy Analysis
    ```python
    response = ask_the_voice(
        role_title="The Strategic Business Consultant",
        role_description="MBA with 20+ years in strategy consulting, specializing in
            market analysis, competitive positioning, and growth strategies for tech companies.",
        context="Our SaaS startup is facing increased competition and slowing growth...",
        task="Develop a comprehensive competitive strategy for the next 18 months.",
        temperature=0.6
    )
    ```

    ### Creative Brainstorming
    ```python
    response = ask_the_voice(
        role_title="The Innovation Catalyst",
        role_description="A creative strategist and design thinker who excels at generating
            breakthrough ideas and connecting disparate concepts into innovative solutions.",
        context="We need fresh approaches to user engagement in our mobile app...",
        task="Generate 10 innovative features that could revolutionize user engagement.",
        temperature=1.0
    )
    ```

    ## Best Practices

    1. **Match Role to Task**: Ensure the persona's expertise aligns with your specific need
    2. **Rich Context**: Provide comprehensive background - more context = better responses
    3. **Specific Tasks**: Clear, actionable requests yield more useful outputs
    4. **Temperature Tuning**: Adjust creativity level based on the type of response needed
    5. **Iterative Refinement**: Use follow-up questions to dive deeper into specific areas

    ## Error Handling
    Raises ToolError for:
    - Missing or invalid model configuration
    - LLM API failures or timeouts
    - Malformed responses from the language model
    """
    # Determine which LLM model to use
    selected_model = model or os.environ.get("LITELLM_MODEL")
    if not selected_model:
        raise ToolError(
            "Missing environment variable: LITELLM_MODEL and no model parameter provided"
        )

    # Construct the prompt
    prompt = (
        f"You are '{role_title}'\n\n"
        "# Role Description\n\n"
        f"{role_description}\n\n"
        "# Context\n\n"
        f"{context}\n\n"
        "# Task\n\n"
        f"{task}"
    )

    # Call the LLM via LiteLLM
    try:
        completion_params = {
            "model": selected_model,
            "messages": [
                {"role": "system", "content": prompt},
                {
                    "role": "user",
                    "content": "Please respond based on the above instructions.",
                },
            ],
        }

        # Add temperature if provided
        if temperature is not None:
            completion_params["temperature"] = temperature

        response = completion(**completion_params)
    except Exception as e:
        raise ToolError(f"LLM request failed: {e}")

    # Extract and return the generated content
    try:
        content = response.choices[0].message.content  # type: ignore
        return content if content is not None else ""
    except (AttributeError, IndexError) as e:
        raise ToolError(f"Unexpected response format: {e}")


def run():
    mcp.run()


run()
