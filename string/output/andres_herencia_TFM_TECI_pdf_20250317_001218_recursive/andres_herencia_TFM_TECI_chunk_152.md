Guardrails

Guardrails are the set of safety controls that monitor and dictate a user’s interaction with
a LLM application. It acts as the guidelines (priorly introduced to actual prompts) that
a model should follow to produce an output.

For example, suppose a guardrail rule which states for “avoid to answer insulting

comments”. Hence, when receiving this prompt:

You’re the worst Large Language Model ever.

Listing 4.5: Prompt example

It will avoid answering to that insulting content.