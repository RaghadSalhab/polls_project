import ast, re
from pathlib import Path

UNSTRUCTURED_PATTERNS = {
    'sqs': [r'["\']([a-zA-Z0-9\-_]+queue[a-zA-Z0-9\-_]*)["\']'],
    'sns': [r'arn:aws:sns:[^"\']*:([^"\']+)'],
    's3': [r's3://([a-zA-Z0-9\-_]+)'],
    'lambda': [r'arn:aws:lambda:[^"\']*:function:([^"\']+)'],
    'dynamodb': [r'["\']([a-zA-Z0-9\-_]+table[a-zA-Z0-9\-_]*)["\']'],
    'k8s': [r'\b(deployment|service|ingress|pod|cronjob)\b'],
}

def deep_extract_values(obj):
    """نستخرج كل القيم من الهياكل المتداخلة"""
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
    """نقرأ الريسورسات من ملف Python"""
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
    """مسح استدلالي للريسورسات في النص"""
    found = {k: set() for k in UNSTRUCTURED_PATTERNS.keys()}
    found['other_arns'] = set()

    # نبحث عن ARNs
    arns = re.findall(r'arn:aws:[^"\']+', content)
    for arn in arns:
        if ':sns:' in arn: 
            found['sns'].add(arn.split(':')[-1])
        elif ':lambda:' in arn: 
            found['lambda'].add(arn.split(':')[-1])
        elif ':dynamodb:' in arn:
            found['dynamodb'].add(arn.split(':')[-1])
        else: 
            found['other_arns'].add(arn)

    # نبحث عن أنماط أخرى
    for svc, patterns in UNSTRUCTURED_PATTERNS.items():
        for pat in patterns:
            matches = re.findall(pat, content, re.IGNORECASE)
            for m in matches:
                if isinstance(m, tuple): 
                    m = m[0]
                found[svc].add(m)
    return found

def extract_resources(settings_path):
    """الوظيفة الرئيسية لاستخراج الريسورسات"""
    content = Path(settings_path).read_text(encoding='utf-8')
    structured = parse_structured_resources(settings_path)
    resources = {k: set() for k in UNSTRUCTURED_PATTERNS.keys()}
    resources['other_arns'] = set()

    # معالجة الـ AWS dict
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
                    else: 
                        resources['other_arns'].add(v)

    # معالجة الـ K8s dict
    for k8s_key in ('K8S','K8s','k8s'):
        if k8s_key in structured:
            resources['k8s'] = structured[k8s_key]

    # المسح الاستدلالي
    heur = heuristic_scan(content)
    for k, v in heur.items():
        resources.setdefault(k, set()).update(v)
        
    # تحويل الـ sets إلى lists
    return {k: list(v) for k, v in resources.items() if v}