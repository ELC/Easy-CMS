Feature: CMS Studio version badge

  Scenario: CMS Studio version is visible from HAR replay
    Given the CMS Studio version Web View is open with HAR replay
    Then the CMS Studio version badge shows "0.1.0"
