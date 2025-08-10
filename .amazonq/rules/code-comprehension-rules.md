# Code Comprehension

## Framework Architecture
- Modularity
  - Each module has a specific responsibility (e.g., page actions, validations).
- Inheritance
  - Use base classes like BasePage, BaseActions to reduce duplication.
- Dependency Injection
  - Inject actions and services into page objects.
- Configuration
  - Centralized config (YAML/`.env`).

## Code Simplicity & Patterns
- Low Complexity
  - Functions are short and focused.
- Single Responsibility
  - Every class and method should do ONE thing only.
- Predictability
  - Follow consistent coding and naming patterns.

## Maintainability & DRY Principle
- Reusable Utilities
  - Shared functions live in utility modules or base classes.
  - Avoid duplication — extract repeated logic into helpers.
- DRY Principle:
  - Centralize repeated logic in base classes or common modules.
  - Page actions should use reusable components.
