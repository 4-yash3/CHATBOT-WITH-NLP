import json
import yaml

# Load the JSON data
def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Convert JSON data to Rasa NLU format
def convert_to_rasa_nlu_format(json_data):
    nlu_data = {"version": "2.0", "nlu": []}
    intents = json_data.get("intents", [])
    for entry in intents:
        if isinstance(entry, dict) and "tag" in entry and "patterns" in entry:
            intent = entry["tag"]
            examples = [f"- {pattern}" for pattern in entry["patterns"]]
            nlu_data["nlu"].append({
                "intent": intent,
                "examples": "\n".join(examples)
            })
        else:
            print(f"Invalid entry format: {entry}")
    return nlu_data

# Create a basic stories and rules based on intents
def create_stories_and_rules(json_data):
    stories_data = {"version": "2.0", "stories": []}
    rules_data = {"version": "2.0", "rules": []}

    intents = json_data.get("intents", [])
    for entry in intents:
        if isinstance(entry, dict) and "tag" in entry and "responses" in entry:
            intent = entry["tag"]
            responses = entry["responses"]

            # Create a simple story
            stories_data["stories"].append({
                "story": f"{intent} story",
                "steps": [
                    {"intent": intent},
                    {"action": f"utter_{intent}"}
                ]
            })

            # Create a simple rule
            rules_data["rules"].append({
                "rule": f"Rule for {intent}",
                "steps": [
                    {"intent": intent},
                    {"action": f"utter_{intent}"}
                ]
            })

    return stories_data, rules_data

# Save data to YAML file
def save_to_yaml(filename, data):
    with open(filename, 'w') as file:
        yaml.dump(data, file, allow_unicode=True, default_flow_style=False)

# Main function
def main():
    json_file_path = r'D:\RASA\archive\intents.json'
    nlu_yaml_file_path = r'D:\RASA\src\data\nlu.yml'
    stories_yaml_file_path = r'D:\RASA\src\data\stories.yml'
    rules_yaml_file_path = r'D:\RASA\src\data\rules.yml'

    # Load JSON data
    json_data = load_json(json_file_path)
    
    # Check if the JSON data has the 'intents' key
    if "intents" in json_data:
        print("JSON data loaded successfully.")
    else:
        print("Error: JSON data does not contain 'intents' key.")
        return

    # Convert to Rasa NLU format
    nlu_data = convert_to_rasa_nlu_format(json_data)
    save_to_yaml(nlu_yaml_file_path, nlu_data)

    # Create stories and rules
    stories_data, rules_data = create_stories_and_rules(json_data)
    save_to_yaml(stories_yaml_file_path, stories_data)
    save_to_yaml(rules_yaml_file_path, rules_data)

    print("NLU, stories, and rules YAML files have been created successfully.")

if __name__ == "__main__":
    main()
