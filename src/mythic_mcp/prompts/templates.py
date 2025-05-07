"""Prompt templates for Mythic MCP."""


def start_pentest(threat_actor: str, objective: str) -> str:
    """Generate a prompt for starting a penetration test.

    Args:
        threat_actor: The threat actor to emulate
        objective: The objective of the penetration test

    Returns:
        str: Generated prompt
    """
    return f"You are an automated pentester, tasked with emulating a specific threat actor. The threat actor is {threat_actor}. Your objective is: {objective}. Perform any required steps to meet the objective, using only techniques documented by the threat actor."


def start_recon() -> str:
    """Generate a prompt for starting reconnaissance.

    Returns:
        str: Generated prompt
    """
    return "You are an automated pentester, tasked with performing recon. Use the available agents to gather information on the compromised hosts." 