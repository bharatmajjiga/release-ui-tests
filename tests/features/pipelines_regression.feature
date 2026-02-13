Feature: Pipelines UI Navigation & Visibility

  Background:
    Given the user is logged in to the OpenShift console with kube:admin

  @smoke @e2e
  Scenario: Verify Duplicate Pipelines button is not visible in the left navigation bar
    Then Validate Duplicate Pipelines buttons are not visible in the left navigation bar