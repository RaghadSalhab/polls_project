import ast, re
from pathlib import Path

# Patterns for unstructured resources
UNSTRUCTURED_PATTERNS = {
    'sqs': [r'["\']([a-zA-Z0-9\-_]+queue[a-zA-Z0-9\-_]*)["\']'],
    'sns': [r'arn:aws:sns:[^"\']*:([^"\']+)'],
    's3': [r's3://([a-zA-Z0-9\-_]+)'],
    'lambda': [r'arn:aws:lambda:[^"\']*:function:([^"\']+)'],
    'dynamodb': [r'["\']([a-zA-Z0-9\-_]+table[a-zA-Z0-9\-_]*)["\']'],
    'kinesis': [r'["\']([a-zA-Z0-9\-_]+stream[a-zA-Z0-9\-_]*)["\']'],
    'events': [r'["\']([a-zA-Z0-9\-_]+rule[a-zA-Z0-9\-_]*)["\']'],
}

def deep_extract_values(obj):
    results = []
    if isinstance(obj, dict):
        for v in obj.values():
            results.extend(deep_extract_values(v))
    elif isinstance(obj, (list, tuple, set)):
        for v in obj:
            results.extend(deep_extract_values(v))
    elif isinstance(obj, str):
        results.append(obj)
    return results

def parse_structured_resources(path):
    content = Path(path).read_text(encoding='utf-8')
    tree = ast.parse(content)
    found = {}
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    name = target.id.upper()
                    try:
                        value = ast.literal_eval(node.value)
                    except Exception:
                        value = None
                    if value is not None:
                        found[name] = value
    return found

def heuristic_scan(content):
    found = {k: set() for k in UNSTRUCTURED_PATTERNS.keys()}
    found['other_arns'] = set()

    # Extract ARNs
    arns = re.findall(r'arn:aws:[^"\']+', content)
    for arn in arns:
        if ':sns:' in arn: 
            found['sns'].add(arn.split(':')[-1])
        elif ':lambda:' in arn: 
            found['lambda'].add(arn.split(':')[-1])
        elif ':dynamodb:' in arn:
            found['dynamodb'].add(arn.split(':')[-1])
        elif ':kinesis:' in arn:
            found['kinesis'].add(arn.split(':')[-1])
        else: 
            found['other_arns'].add(arn)

    # Scan for unstructured patterns, ignoring keys in ALL CAPS
    for svc, patterns in UNSTRUCTURED_PATTERNS.items():
        for pat in patterns:
            matches = re.findall(pat, content, re.IGNORECASE)
            for m in matches:
                if isinstance(m, tuple): 
                    m = m[0]
                # Ignore strings that are all uppercase (likely keys)
                if not m.isupper():
                    found[svc].add(m)
    return found

def extract_resources(settings_path):
    content = Path(settings_path).read_text(encoding='utf-8')
    structured = parse_structured_resources(settings_path)
    resources = {k: set() for k in UNSTRUCTURED_PATTERNS.keys()}
    resources['other_arns'] = set()

    aws = structured.get('AWS', {})
    for svc_key, svc_val in aws.items():
        k = svc_key.lower()
        vals = deep_extract_values(svc_val)
        if k in resources: 
            resources[k].update(vals)
        else:
            for v in vals:
                if isinstance(v, str) and v.startswith('arn:aws:'):
                    if ':sns:' in v: 
                        resources['sns'].add(v.split(':')[-1])
                    elif ':lambda:' in v: 
                        resources['lambda'].add(v.split(':')[-1])
                    elif ':dynamodb:' in v:
                        resources['dynamodb'].add(v.split(':')[-1])
                    elif ':kinesis:' in v:
                        resources['kinesis'].add(v.split(':')[-1])
                    else: 
                        resources['other_arns'].add(v)

    heur = heuristic_scan(content)
    for k, v in heur.items():
        resources.setdefault(k, set()).update(v)

    # Return as dict of lists
    return {k: list(v) for k, v in resources.items() if v}
