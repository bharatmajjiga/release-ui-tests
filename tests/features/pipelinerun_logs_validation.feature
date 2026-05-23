Feature: PipelineRun Logs Page Validation

  Background:
    Given the user is logged into openshift console with auth kube:admin
    When the user expands Pipelines in left navigation bar
    And the user navigates to the Pipelines page
    And the user navigates to PipelineRuns tab
    And user switches to current project
    When the user creates a pipelinerun from YAML file "simple_pipelinerun.yaml"
    And the user navigates to Logs tab
    And the user waits for logs to fully load

  @smoke @sanity
  Scenario: Verify PipelineRun Logs page displays all required elements
    Then the PipelineRun Logs page should be visible
    And the task navigation should be visible
    And all tasks should be displayed in the task navigation
    And all tasks should have successful status
    And the logs container should be visible

  @sanity
  Scenario Outline: Verify task status indicators and user interactions
    Then each task should display a status indicator
    And the status of task "<task_name>" should be "<task_status>"
    When the user clicks on the first available task
    Then the logs container should be visible
    And the selected task should be highlighted

    Examples:
      | task_name | task_status |
      | greet     | success     |
