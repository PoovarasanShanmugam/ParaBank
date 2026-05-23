"""
Bridge module for Behave compatibility.
Behave requires step definitions inside features/steps/ by convention.
All actual step implementation logic lives in the top-level step_definitions/ folder.
This file re-exports all steps so Behave can discover them.
"""
from step_definitions.registration_steps import *  # noqa: F401,F403
