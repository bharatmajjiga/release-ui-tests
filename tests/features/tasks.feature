Feature: Task & TaskRuns Creation & Corresponding Validations


  @smoke @sanity
  Scenario Outline: Verify User is able to create Task successfully
    Given the user is on the OpenShift login page
    When user chooses to login with kube:admin
    And the user logs in with valid credentials
    And Validate Pipelines button is visible in the left navigation bar
    And the user clicks on Pipelines button
    And the user clicks on Task links under Pipelines button
    And the user creates task with <task_yaml>
    Then validate task <task_name> is available under tasks page
    Examples:
    | task_yaml                 |   task_name     |
    | tasks/hello-world.yaml    |   hello-world   |


 @smoke @sanity
  Scenario Outline: Verify task details page is populated with appropriate info
    When the user clicks on Task links under Pipelines button
    When user clicks on task <task_name> on tasks page
    Then validate task details page of <task_name>

    Examples:
    |   task_name     |
    |   hello-world   |


@smoke @sanity
  Scenario Outline: Verify User is able to create TaskRun successfully
    When the user clicks on Task links under Pipelines button
    When user navigates to TaskRuns tab
    When the user creates taskrun with <taskrun_yaml>
    Then validate task <taskrun_name> is available under taskruns page
     Examples:
    | taskrun_yaml                 |   taskrun_name     |
    | taskruns/hello-world.yaml    |   hello-task-run      |