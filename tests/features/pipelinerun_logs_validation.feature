Feature: Validate PipelineRun Logs Page displays tasks and validates successful execution
  As a pipeline developer
  I want to view PipelineRun logs
  So that I can validate all tasks executed successfully

  Background:
    Given the user is logged into openshift console with auth kube:admin

  @smoke @sanity
  Scenario: Verify PipelineRun Logs page displays all tasks successfully
    Given a PipelineRun "hello-pipeline-run" exists in namespace "pipeline-test"
    When the user navigates to the PipelineRun "hello-pipeline-run" in namespace "pipeline-test"
    And the user navigates to Logs tab
    Then the PipelineRun Logs page should be visible
    And all tasks should be displayed in the task navigation
    And all tasks should have successful status
    And the logs container should be visible

  @smoke @sanity
  Scenario: Verify task navigation on PipelineRun Logs page
    Given a PipelineRun "hello-pipeline-run" exists in namespace "pipeline-test"
    When the user navigates to the PipelineRun "hello-pipeline-run" in namespace "pipeline-test"
    And the user navigates to Logs tab
    Then the PipelineRun Logs page should be visible
    And the task navigation should be visible
    And at least one task should be present

  @sanity
  Scenario: Verify comprehensive PipelineRun validation
    Given a PipelineRun "hello-pipeline-run" exists in namespace "pipeline-test"
    When the user navigates to the PipelineRun "hello-pipeline-run" in namespace "pipeline-test"
    And the user navigates to Logs tab
    Then the PipelineRun Logs page should be visible
    And the pipeline run should be validated as successful

  @sanity
  Scenario: Verify individual task selection and navigation
    Given a PipelineRun "hello-pipeline-run" exists in namespace "pipeline-test"
    When the user navigates to the PipelineRun "hello-pipeline-run" in namespace "pipeline-test"
    And the user navigates to Logs tab
    And the user clicks on the first available task
    Then the logs container should be visible
    And the selected task should be highlighted

  @sanity
  Scenario: Verify task status is displayed correctly
    Given a PipelineRun "hello-pipeline-run" exists in namespace "pipeline-test"
    When the user navigates to the PipelineRun "hello-pipeline-run" in namespace "pipeline-test"
    And the user navigates to Logs tab
    Then each task should display a status indicator
    And the status of task "hello" should be "success"

  @sanity
  Scenario: Verify expected tasks are displayed
    Given a PipelineRun "hello-pipeline-run" exists in namespace "pipeline-test"
    When the user navigates to the PipelineRun "hello-pipeline-run" in namespace "pipeline-test"
    And the user navigates to Logs tab
    Then the following tasks should be displayed:
      | task_name |
      | hello     |

  @sanity
  Scenario: Verify all task statuses can be retrieved
    Given a PipelineRun "hello-pipeline-run" exists in namespace "pipeline-test"
    When the user navigates to the PipelineRun "hello-pipeline-run" in namespace "pipeline-test"
    And the user navigates to Logs tab
    Then task statuses should be retrievable for all tasks
    And all retrieved task statuses should be valid

  @regression
  Scenario: Verify logs page loads after waiting for completion
    Given a PipelineRun "hello-pipeline-run" exists in namespace "pipeline-test"
    When the user navigates to the PipelineRun "hello-pipeline-run" in namespace "pipeline-test"
    And the user navigates to Logs tab
    And the user waits for logs to fully load
    Then the PipelineRun Logs page should be visible
    And all tasks should be displayed in the task navigation
    And the logs container should be visible
