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
