#!/usr/bin/env python3
"""Read-only structural check. Does not execute nodes or prove runtime safety."""
import argparse,json,re,sys
from pathlib import Path
SECRET_KEYS={'password','access_token','refresh_token','client_secret','apikey','api_key','authorization'}
def check(workflow):
    errors=[]
    if not isinstance(workflow,dict):return ['Workflow must be a JSON object.']
    if workflow.get('active') is not False:errors.append('Shareable workflow must explicitly set active=false.')
    nodes=workflow.get('nodes')
    if not isinstance(nodes,list) or not nodes:return errors+['nodes must be a nonempty array.']
    names=set();ids=set()
    for i,n in enumerate(nodes):
        if not isinstance(n,dict):errors.append(f'Node {i} must be an object.');continue
        for key,seen in [('name',names),('id',ids)]:
            v=n.get(key)
            if not isinstance(v,str) or not v.strip():errors.append(f'Node {i} needs {key}.')
            elif v in seen:errors.append(f'Duplicate node {key}.')
            else:seen.add(v)
        if not isinstance(n.get('type'),str) or not n['type']:errors.append(f'Node {i} needs a type.')
        v=n.get('typeVersion')
        if isinstance(v,bool) or not isinstance(v,(int,float)) or v<=0:errors.append(f'Node {i} needs a positive typeVersion.')
        if not isinstance(n.get('parameters'),dict):errors.append(f'Node {i} needs a parameters object.')
        if n.get('credentials'):errors.append(f'Node {i} contains credential bindings; strip them from a public example.')
    edges=workflow.get('connections')
    if not isinstance(edges,dict):errors.append('connections must be an object.');edges={}
    for source,ports in edges.items():
        if source not in names:errors.append('Connection starts at an unknown node.')
        if not isinstance(ports,dict):errors.append('Connection ports must be an object.');continue
        for groups in ports.values():
            if not isinstance(groups,list):errors.append('Connection output groups must be arrays.');continue
            for group in groups:
                if not isinstance(group,list):errors.append('Connection output must be an array.');continue
                for edge in group:
                    if not isinstance(edge,dict):errors.append('Connection target must be an object.');continue
                    if edge.get('node') not in names:errors.append('Connection points at an unknown node.')
                    index=edge.get('index')
                    if isinstance(index,bool) or not isinstance(index,int) or index<0:errors.append('Connection target index must be a nonnegative integer.')
                    if not isinstance(edge.get('type'),str) or not edge['type']:errors.append('Connection target needs a type.')
    def scan(value):
        if isinstance(value,dict):
            for k,v in value.items():
                if k.lower() in SECRET_KEYS and isinstance(v,str) and v and not v.startswith('={{'):errors.append('Possible embedded secret field; inspect locally (value withheld).')
                if k.lower()=='name' and isinstance(v,str) and v.lower() in SECRET_KEYS and isinstance(value.get('value'),str) and value['value'] and not value['value'].startswith('={{'):errors.append('Possible embedded secret header (value withheld).')
                scan(v)
        elif isinstance(value,list):
            for item in value:scan(item)
        elif isinstance(value,str) and re.search(r'-----BEGIN [A-Z ]*PRIVATE KEY-----|\b(?:sk-(?:proj-)?|gh[pousr]_)[A-Za-z0-9_-]{20,}',value):errors.append('Possible credential pattern (value withheld).')
    scan(workflow)
    return list(dict.fromkeys(errors))
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('workflow',type=Path);a=p.parse_args()
    try:errors=check(json.loads(a.workflow.read_text()))
    except (OSError,ValueError):errors=['Cannot read a valid JSON workflow.']
    print(json.dumps({'structurally_valid':not errors,'errors':errors,'runtime_verified':False},indent=2));return bool(errors)
if __name__=='__main__':sys.exit(main())
