Feature: Triggers functionality validation

  Background:
    Given the user is on the OpenShift login page
    When user chooses to login with kube:admin
    And the user logs in with valid credentials
    And Validate Pipelines button is visible in the left navigation bar
    And the user clicks on Pipelines button
    And the user clicks on Task links under Pipelines button
    And the user creates task with tasks/hello-world.yaml
    And the user clicks on Pipelines links under Pipelines button
    And the user creates pipelines with yaml view via pipelines/hello-goodbye-pipeline.yaml

  @smoke @sanity
  Scenario Outline: Verify User is able to create PipelineRuns via YAML view successfully
    When the user clicks on Pipelines links under Pipelines button
    When the user navigates to pipelineruns tab
    And the user creates pipelineruns with yaml view via <pipelinerun_yaml>
    Then validate pipelinerun <pipelinerun_name> is available under pipelineruns page
    Examples:
    | pipelinerun_yaml                       |    pipelinerun_name      |
    | pipelineruns/hello-goodbye-run.yaml    |   hello-goodbye-run      |


 @smoke @sanity
  Scenario Outline: Verify pipelineruns details page is populated with appropriate info
    When the user clicks on Pipelines links under Pipelines button
    When the user navigates to pipelinerun tab
    When user clicks on pipelinerun <pipelinerun_name> on Pipelineruns page
    Then validate pipelinerun details page of <pipelinerun_name>
    Examples:
    |   pipelinerun_name    |
    |   hello-goodbye-run   |