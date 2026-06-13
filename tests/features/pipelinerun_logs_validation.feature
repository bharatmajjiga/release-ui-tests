Feature: PipelineRun Logs Page Validation

  Background:
    Given the user is logged into openshift console with auth kube:admin
    When the user expands Pipelines in left navigation bar
    And the user navigates to the Pipelines page
    And user switches to current project

  @e2e
  Scenario: validation of PipelineRun Logs page elements and task interactions
    Given the user creates a pipelinerun from YAML file "simple_pipelinerun_inline.yaml"
    When the user navigates to Logs tab
    And the user waits for logs to fully load
    Then the PipelineRun Logs page should be visible
    And the task navigation should be visible
    And all tasks should be displayed in the task navigation
    And all tasks should have successful status
    And the logs container should be visible
    And each task should display a status indicator
    And the status of task "greet" should be "success"
    And the status of task "check" should be "success"
    When the user clicks on the first available task
    Then the logs container should be visible
    And the selected task should be highlighted
