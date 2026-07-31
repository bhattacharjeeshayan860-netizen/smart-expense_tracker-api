# AI Assistance Notes

## Overview
I used AI (GitHub Copilot) as a pair programmer throughout this project, but I maintained full control over architectural decisions, code quality, and testing strategy. Below are specific examples of how AI assisted and where I intervened.

## AI-Generated Code (with my review/modifications)

### Storage Layer (`src/storage.py`)
- **AI suggestion**: Initial implementation used a global dictionary in memory for storage
- **My modification**: Rejected this suggestion because the assignment implied persistence ("JSON file is slightly more 'real'"). I implemented file-based storage using JSON with proper date serialization/deserialization.
- **AI assistance**: Helped with the basic JSON read/write patterns and date conversion logic after I specified the requirement.
- **Further refinement**: After initial tests failed due to Pydantic model mismatch, I separated `ExpenseCreate` (without id) and `Expense` (with id) models, and updated the storage layer to handle the conversion properly.

### Models (`src/models.py`)
- **AI suggestion**: Generated a single `Expense` model with all fields including id
- **My modification**: Created separate `ExpenseBase`, `ExpenseCreate`, and `Expense` models to properly handle input validation (id should not be provided on creation) and ORM-like usage.
- **Reason**: Following best practices for separating input/output models in APIs.

### Endpoints (`src/main.py`)
- **AI suggestion**: Generated basic CRUD endpoint skeletons with correct HTTP methods and status codes
- **My modifications**: 
  - Added proper HTTPException handling for 404 cases (delete/filter with no matches)
  - Implemented the totals endpoint with category-based aggregation logic
  - Added response_model parameters for automatic documentation
  - Changed endpoint to accept `ExpenseCreate` instead of `Expense` for POST operations
  - Added docstrings and endpoint descriptions

### Tests (`tests/test_expenses.py`)
- **AI suggestion**: Generated basic test structure for POST and GET endpoints
- **My modifications**:
  - Added comprehensive setup/teardown with `setup_function()` to isolate tests
  - Created tests for all edge cases: negative amounts, missing fields, wrong types, non-existent IDs
  - Added validation tests to confirm FastAPI's automatic 422 responses
  - Implemented tests for the totals endpoint and category filtering
  - Added test for deleting non-existent resources
  - Fixed test issues that arose from model changes (separating ExpenseCreate and Expense)

## Specific Examples Where I Overrode AI Suggestions

1. **Storage Architecture**: 
   - AI suggested: Simple global list/dict with in-memory storage
   - I chose: File-based JSON persistence with proper ID generation and data loading/saving
   - Reason: The assignment hinted that JSON persistence would be "slightly more real" and barely more work, and I wanted to demonstrate ability to make thoughtful architectural decisions.

2. **Error Handling**:
   - AI suggestion: Return None or empty lists for not-found cases
   - I chose: Proper HTTPException with 404 status codes for DELETE and category filtering when no matches found
   - Reason: Following REST conventions and ensuring clients receive appropriate status codes.

3. **Testing Scope**:
   - AI suggestion: Basic happy-path tests for each endpoint
   - I chose: Comprehensive test suite including validation, edge cases, error conditions, and isolation between tests
   - Reason: To thoroughly verify correctness and demonstrate testing proficiency.

4. **Model Separation**:
   - AI suggestion: Single model for both input and output
   - I chose: Separate `ExpenseCreate` (input) and `Expense` (output) models
   - Reason: To prevent clients from specifying IDs on creation and to clearly separate concerns.

## What I Wrote/Modified Myself

- **Architecture decisions**: Chose file-based JSON storage over in-memory
- **Model design**: Created separate input/output models for proper validation
- **Error handling**: Implemented proper 404 responses for missing resources
- **Business logic**: Created the totals calculation with category-based aggregation
- **Test completeness**: Wrote all edge case tests and validation scenarios
- **Code review**: Refactored AI-generated storage methods to properly handle date serialization and model conversion
- **Documentation**: Wrote README and API descriptions from scratch

## Learning Outcomes Demonstrated

1. **Ability to evaluate AI suggestions**: Critically assessed in-memory vs persistent storage trade-offs
2. **Security awareness**: Implemented proper input validation through Pydantic (separating input/output models)
3. **Testing mindset**: Went beyond basic tests to include error conditions and edge cases
4. **API design**: Followed REST conventions with appropriate status codes and response formats
5. **Persistence concerns**: Handled data serialization complexities (dates, IDs) correctly
6. **Debugging skills**: Identified and fixed issues arising from model mismatches between layers

This approach ensured that while I leveraged AI for productivity, the final code reflects my understanding and meets the assignment's goals of demonstrating judgment and clean implementation.