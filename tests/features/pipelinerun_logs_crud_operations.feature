Feature: PipelineRun Logs CRUD Operations

  Background:
    Given the user is logged into openshift console with auth kube:admin
    When the user expands Pipelines in left navigation bar
    And the user navigates to the Pipelines page
    And the user navigates to PipelineRuns tab
    And user switches to current project

  @smoke @sanity
  Scenario Outline: Create PipelineRun and verify logs display expected content
    When the user creates a pipelinerun from YAML file "<yaml_file>"
    And the user navigates to Logs tab
    And the user waits for logs to fully load
    Then the logs for task "<task_name>" should contain "<expected_text>"

    Examples:
      | yaml_file               | task_name | expected_text          |
      | simple_pipelinerun.yaml | greet     | Hello from pipeline!   |
