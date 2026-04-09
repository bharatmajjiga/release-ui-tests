Feature: Pipeline creation via yaml & Corresponding Validations

  Background:
    Given the user is on the OpenShift login page
    When user chooses to login with kube:admin
    And the user logs in with valid credentials
    And Validate Pipelines button is visible in the left navigation bar
    And the user clicks on Pipelines button
    And the user clicks on Task links under Pipelines button
    And the user creates task with tasks/hello-world.yaml

  @smoke @sanity
  Scenario Outline: Verify User is able to create Pipelines via YAML view successfully
    When the user clicks on Pipelines links under Pipelines button
    And the user creates pipelines with yaml view via <pipeline_yaml>
    Then validate pipeline <pipeline_name> is available under pipelines page
    Examples:
    | pipeline_yaml                            |    pipeline_name            |
    | pipelines/hello-goodbye-pipeline.yaml    |   hello-goodbye-pipeline    |


 @smoke @sanity
  Scenario Outline: Verify pipelines details page is populated with appropriate info
    When the user clicks on Pipelines links under Pipelines button
    When user clicks on pipeline <pipeline_name> on Pipelines page
    Then validate pipelines details page of <pipeline_name>

    Examples:
    |   pipeline_name            |
    |   hello-goodbye-pipeline   |