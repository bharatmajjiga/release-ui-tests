Feature: Pipelines UI Navigation & Visibility

  @smoke @e2e
  Scenario: Verify Pipelines button is visible in left navigation bar
    Given the user is on the OpenShift login page
    When user chooses to login with kube:admin
    And the user logs in with valid credentials
    Then Validate Pipelines button is visible in the left navigation bar


  @smoke @e2e
  Scenario Outline: Verify appropriate links are available under pipelines button
    Given the user is on the OpenShift login page
    When user chooses to login with kube:admin
    And the user logs in with valid credentials
    And Validate Pipelines button is visible in the left navigation bar
    And the user clicks on Pipelines button
    Then Verify the following <links> are available under Pipelines button
    Examples:
    | links     |
    | Overview  |
    | Pipelines |
    | Tasks     |
    | Triggers  |


  @smoke @e2e
  Scenario: Verify successful navigation to Overview page
    Given the user is on the OpenShift login page
    When user chooses to login with kube:admin
    And the user logs in with valid credentials
    And Validate Pipelines button is visible in the left navigation bar
    And the user clicks on Pipelines button
    Then the user navigates to the Overview page


  @smoke @e2e
  Scenario: Verify successful navigation to Pipelines page and Sub Tabs
    Given the user is on the OpenShift login page
    When user chooses to login with kube:admin
    And the user logs in with valid credentials
    And Validate Pipelines button is visible in the left navigation bar
    And the user clicks on Pipelines button
    Then the user navigates to the Pipelines page
    And the user navigates to PipelineRuns tab
    And the user navigates to Repositories tab


  @smoke @e2e
  Scenario: Verify successful navigation to Tasks page and Sub Tabs
    Given the user is on the OpenShift login page
    When user chooses to login with kube:admin
    And the user logs in with valid credentials
    And Validate Pipelines button is visible in the left navigation bar
    And the user clicks on Pipelines button
    Then the user navigates to the Tasks page
    And the user navigates to TaskRuns tab


  @smoke @e2e
  Scenario: Verify successful navigation to Triggers page and Sub Tabs
    Given the user is on the OpenShift login page
    When user chooses to login with kube:admin
    And the user logs in with valid credentials
    And Validate Pipelines button is visible in the left navigation bar
    And the user clicks on Pipelines button
    Then the user navigates to the Triggers page
    And the user navigates to TriggerTemplates tab
    And the user navigates to TriggerBindings tab
    And the user navigates to ClusterTriggerBindings tab
