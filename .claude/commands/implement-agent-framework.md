# Implement Agent Framework

Create the core agent orchestration framework for edge-assistant based on OpenAI agent patterns.

## Instructions

1. **Framework Setup**
   - Create `edge_assistant/agents/` directory structure
   - Implement base agent classes in `agents/base.py`
   - Extend Engine class with orchestration methods
   - Add agent state management to `state.py`

2. **Core Components Implementation**
   - Create Agent base class with OpenAI Responses integration
   - Implement AgentOrchestrator for managing multiple agents
   - Add function tool registration system
   - Create agent-as-tool wrapper functions

3. **Development Tools Creation**
   - Add project structure analysis tools
   - Create code pattern detection utilities
   - Implement safe multi-file editing with diff previews
   - Add context-aware code generation tools

4. **Integration with Existing System**
   - Extend current Engine class without breaking changes
   - Integrate with existing KB indexing system
   - Preserve safety model with diff previews
   - Maintain XDG state management compatibility

5. **Testing and Validation**
   - Create simple test agent for proof of concept
   - Test orchestration with basic development task
   - Validate integration with existing CLI commands
   - Ensure backward compatibility with current features