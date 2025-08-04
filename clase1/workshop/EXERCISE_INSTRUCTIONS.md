# Exercise: Antipattern Identification

## Objective
Identify and document the antipatterns present in the three provided systems. Estimated time: 30 minutes.

## Files to analyze:
1. **exercise_inventory_system.py** - Inventory management system
2. **exercise_banking_api.py** - Banking services API  
3. **exercise_course_platform.py** - Online course platform

## Instructions:

### 1. Analyze any file and look for the following common antipatterns:

- **God Object/God Class**: Classes that do too many things
- **Spaghetti Code**: Code with tangled logic that's hard to follow
- **Copy-Paste Programming**: Duplicated code
- **Magic Numbers/Strings**: Hardcoded values without context
- **Long Method**: Methods that are too long
- **Feature Envy**: Classes that excessively use data from other classes
- **Global State**: Excessive use of global variables
- **Singleton Abuse**: Misuse of the Singleton pattern

### 2. For each antipattern found, document:

- **Location**: File and line(s) where it's found
- **Antipattern type**: Name of the antipattern
- **Problem description**: Why it's problematic
- **Impact**: What problems it can cause
- **Possible solution**: How it could be refactored

### 3. Delivery format:

Create a document with your findings following this format:

```
## File: [filename.py]

### Antipattern 1: [Antipattern name]
- **Location**: Lines X-Y
- **Description**: [Problem explanation]
- **Impact**: [Consequences]
- **Proposed solution**: [How to improve it]

### Antipattern 2: ...
```

## Hints:

1. Pay attention to:
   - Classes with more than 10 attributes or methods
   - Methods with more than 50 lines
   - Code repeated more than 2 times
   - Shared global variables
   - Deeply nested conditionals
   - Classes that directly access other classes' data

2. Consider SOLID principles:
   - Single Responsibility Principle
   - Open/Closed Principle
   - Liskov Substitution Principle
   - Interface Segregation Principle
   - Dependency Inversion Principle

Good luck!