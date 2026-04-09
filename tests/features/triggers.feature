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
  Scenario Outline: Verify User is able to trigger pipelinerun via triggers
    When the user clicks on Triggers links under Pipelines button
    And the user creates triggertemplate via <trigger_template_yaml>
    When validate triggertemplate <trigger_template_name> is available under triggertemplates page
    And the user creates triggerbindings via <trigger_bindings_yaml> 
    When validate triggerbindings <trigger_binding_name> is available under triggerbindings page
    Examples:
    | trigger_template_yaml                 |  trigger_temp_name   |  trigger_bindings_yaml              | trigger_binding_name   |
    | triggertemplates/hello-template.yaml  |   hello-template     | triggerbindings/hello-binding.yaml  |  hello-binding          |


 @smoke @sanity
  Scenario Outline: Verify pipelineruns details page is populated with appropriate info
    When the user clicks on Pipelines links under Pipelines button
    When the user navigates to pipelinerun tab
    When user clicks on pipelinerun <pipelinerun_name> on Pipelineruns page
    Then validate pipelinerun details page of <pipelinerun_name>
    Examples:
    |   pipelinerun_name    |
    |   hello-goodbye-run   |