# TheVoices

A FastMCP server providing role-based AI assistant tools for specialized AI personas and LLM model discovery.

## GitHub is only Mirror

This GitHub repository is a read-only mirror. For issues, bug reports, feature requests, and contributions, please visit the main repository at:

**https://git.jagenberg.info/tim/TheVoices**

## Features

- **Model Discovery**: Auto-detect available LLM models based on API keys
- **Role-based AI**: Create specialized AI assistants with defined expertise and personas
- **Multiple Providers**: Support for OpenAI, Anthropic, Azure, and other LLM providers

## Usage

For example in Zed:

```json
"context_servers": {
  "TheVoices": {
    "source": "custom",
    "command": {
      "path": "uvx",
      "args": ["https://git.jagenberg.info/tim/TheVoices.git"],
      "env": {
        "LITELLM_MODEL": "openai/gpt-4.1",
        "ANTHROPIC_API_KEY": "YOUR_API_KEY",
        "OPENAI_API_KEY": "YOUR_API_KEY"
      }
    }
  }
}
```

### Available Tools

#### `list_available_models()`
Returns available LLM models based on your API keys.

#### `ask_the_voice(role_title, role_description, context, task, model?, temperature?)`
Create specialized AI assistants with defined roles and expertise.

**Example:**
```python
ask_the_voice(
    role_title="The Security Architect",
    role_description="Senior cybersecurity expert specializing in threat analysis",
    context="We detected unusual network traffic patterns...",
    task="Analyze this security incident and provide remediation steps"
)
```

## Requirements

- Python 3.13+
- FastMCP 2.9.2+
- LiteLLM 1.73.6+
- Valid API keys for at least one LLM provider

## License

This project is licensed under the Eclipse Public License 2.0. See the [EPL-2.0.txt](EPL-2.0.txt) file for details.