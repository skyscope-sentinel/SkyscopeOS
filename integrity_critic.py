import ast
import json
import yaml

class IntegrityCritic:
    """
    A class to perform static analysis on code and configuration files.
    """

    def __init__(self):
        pass

    def validate_python_code(self, code: str) -> (bool, str):
        """
        Validates Python code by attempting to parse it into an Abstract Syntax Tree (AST).
        This checks for basic syntax errors without executing the code.
        """
        try:
            ast.parse(code)
            return (True, "Python code is syntactically valid.")
        except SyntaxError as e:
            return (False, f"Python syntax error: {e}")

    def validate_json(self, json_string: str) -> (bool, str):
        """Validates a JSON string."""
        try:
            json.loads(json_string)
            return (True, "JSON is valid.")
        except json.JSONDecodeError as e:
            return (False, f"JSON decode error: {e}")

    def validate_yaml(self, yaml_string: str) -> (bool, str):
        """Validates a YAML string."""
        try:
            yaml.safe_load(yaml_string)
            return (True, "YAML is valid.")
        except yaml.YAMLError as e:
            return (False, f"YAML error: {e}")

# Example usage:
if __name__ == '__main__':
    critic = IntegrityCritic()

    # Test Python validation
    valid_python = "def hello():\n    print('Hello, world!')"
    invalid_python = "def hello()\n    print('Hello, world!')"
    print(f"Valid Python: {critic.validate_python_code(valid_python)}")
    print(f"Invalid Python: {critic.validate_python_code(invalid_python)}")

    # Test JSON validation
    valid_json = '{"key": "value", "number": 123}'
    invalid_json = '{"key": "value", "number": 123,}'
    print(f"Valid JSON: {critic.validate_json(valid_json)}")
    print(f"Invalid JSON: {critic.validate_json(invalid_json)}")

    # Test YAML validation
    valid_yaml = "key: value\nnumber: 123"
    invalid_yaml = "key: value\n- number: 123"
    print(f"Valid YAML: {critic.validate_yaml(valid_yaml)}")
    print(f"Invalid YAML: {critic.validate_yaml(invalid_yaml)}")
