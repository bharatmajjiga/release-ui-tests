"""
Locators module for UI automation.

This module contains all UI element locators organized by domain.
Locators are separated from page objects to allow easy versioning and maintenance
across different OpenShift Console releases.

Module organization:
- commons.py: Shared UI components (Login, Navigation, Actions, Favorites, Project Selector)
- pipelines.py: Pipeline-related page locators
- pipelineruns.py: PipelineRun-related page locators
- tasks.py: Task-related page locators
- triggers.py: Trigger-related page locators (EventListener, TriggerTemplate, TriggerBinding)
- overview.py: Overview and Repositories page locators
"""
