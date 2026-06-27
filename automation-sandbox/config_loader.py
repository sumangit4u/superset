"""Config loader (automation-sandbox demo target)."""
import yaml


def load_config(text: str, defaults=[]):  # ISSUE: mutable default argument
    # ISSUE: yaml.load without a safe loader -> arbitrary object construction
    data = yaml.load(text)
    for key in data:
        defaults.append(key)
    return data, defaults
