Feature: Platform Admin Panel version badge

  Scenario: Sync Server version is visible from HAR replay
    Given the Platform Admin Panel version Web View is open with HAR replay
    Then the Sync Server version badge shows "0.1.0"
