"""Validate the design artifact and synthetic specimens, not a workbench runtime."""
from pathlib import Path
import copy
import hashlib
import json
import math
import sys

try:
    from jsonschema import Draft202012Validator
except ImportError:
    print(json.dumps({'status':'error','code':'MISSING_DESIGN_DEPENDENCY','dependency':'jsonschema==4.26.0'}))
    sys.exit(1)

ROOT=Path(__file__).resolve().parents[1]
checks=[]

def strict_pairs(pairs):
    out={}
    for k,v in pairs:
        if k in out: raise ValueError('Duplicate JSON key: '+k)
        out[k]=v
    return out

def load(path):
    return json.loads((ROOT/path).read_text(encoding='utf-8'),object_pairs_hook=strict_pairs,
                      parse_constant=lambda x: (_ for _ in ()).throw(ValueError('Nonfinite number')))

def canonical(obj):
    return json.dumps(obj,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()

def digest(obj):return hashlib.sha256(canonical(obj)).hexdigest()

def record(id_,ok,detail):checks.append({'id':id_,'status':'pass' if ok else 'fail','detail':detail})

def valid(name,document):
    return not list(Draft202012Validator(load('schemas/'+name+'.schema.json')).iter_errors(document))

def hash_matches(plan):return plan['plan_id']==digest({k:v for k,v in plan.items() if k!='plan_id'})

def dag_valid(nodes):
    seen=set()
    for n in nodes:
        if n['node_id'] in seen or any(d not in seen for d in n['depends_on']):return False
        seen.add(n['node_id'])
    return True

def main():
    schemas=sorted((ROOT/'schemas').glob('*.schema.json'))
    for p in schemas:Draft202012Validator.check_schema(load(str(p.relative_to(ROOT))))
    record('D01',True,f'{len(schemas)} candidate schemas passed Draft 2020-12 metaschema validation.')
    contract=load('contract.json');cap=load('capability-map.json');profiles=load('stage-profiles.json')
    record('D02',valid('contract-candidate',contract),'Commission-derived contract shape; exact house v1 remains unverified.')
    record('D03',all((ROOT/e[k]).is_file() for e in contract['entry_points'].values() for k in ['input_schema','output_schema','reply_envelope']),'Every proposed verb references an existing candidate schema.')
    record('D04',valid('capability-map',cap),'Candidate map shape.')
    r={x['family_id']:x for x in cap['families']}
    record('D05',set(r)=={'RCI','SGI','TE','CE','SEI','CPR','PPR','EQA'} and len(cap['families'])==8,'Seven domain entries including absent CE, plus EQA.')
    record('D06',r['CE']['package'] is None and r['CE']['maturity']['presence']=='absent' and all('copyediting' not in r[x]['capabilities'] for x in ['SGI','TE']),'CE remains absent; no substitution.')
    record('D07',sum(x['evaluation']['rule_count'] or 0 for x in r.values())==199 and sum(x['evaluation']['fixture_count'] or 0 for x in r.values())==310,'Declared source counts preserved; no fixture execution claim.')
    hooks=load('open-hooks.json')['hooks']
    source_hooks=[]
    for family in r:
        if family=='CE':continue
        source=load('sources/families/'+family+'/02_RULES/decision_hooks.json')
        source_hooks.extend((family,x.get('hook_id') or x['id'],x) for x in source['hooks'])
    record('D08',len(hooks)==74 and len({x['hook_id'] for x in hooks})==74 and all(any(y['family_id']==f and y['hook_id']==i and y['source_record']==v and y['status']=='open' for y in hooks) for f,i,v in source_hooks),'All 74 original hooks retained verbatim as open source records.')
    record('D09',len(r['EQA']['evaluation']['critical_fixture_ids'])==9 and all(not r[x]['evaluation']['critical_fixture_ids'] for x in r if x!='EQA'),'No family critical fixture sets invented.')
    lock=load('sources/workbench/skills.lock.json')['skills']
    record('D10',all(r[f]['execution_pin']['value']==lock[repo] for f,repo in [('RCI','reference-citation-integrity'),('SEI','scholarly-editorial-integrity')]) and all(r[f]['execution_pin'] is None for f in r if f not in ['RCI','SEI']),'Inherited lock unchanged; no new execution pins.')
    record('D11',all(x['package']['version']=='0.1.0' and 'draft' in x['maturity']['package_status'] for x in r.values() if x['package']),'No family version or maturity promotion.')
    source_index=load('source-index.json')['sources']
    record('D12',all(hashlib.sha256((ROOT/x['path']).read_bytes()).hexdigest()==x['sha256'] for x in source_index),'All supplied evidence captures match their recorded byte hashes.')
    record('D13',valid('batch-request',load('examples/citation-request.json')) and valid('batch-request',load('examples/production-proof-request.json')),'Both caller requests are valid candidate shapes.')
    record('D14',not valid('batch-request',load('examples/invalid-caller-family-request.json')),'Caller family selector is rejected.')
    pp=[]
    for profile in profiles['profiles']:
        p=load('examples/'+profile['profile_id']+'-plan.json');pp.append(p)
        record('D15-'+profile['profile_id'],valid('stage-plan',p) and hash_matches(p),'Candidate plan shape and content digest.')
        record('D16-'+profile['profile_id'],dag_valid(p['nodes']),'All dependencies precede consumers; no cycle or missing node.')
        record('D17-'+profile['profile_id'],p['bindings']['capability_map']==digest(cap) and p['bindings']['profile']==digest({'profile':profile,'control_spine':profiles['control_spine']}),'Map, profile and control spine bound into plan.')
        record('D17b-'+profile['profile_id'],p['bindings']['manifest']==digest(load('examples/synthetic-manifest.json')) and all((p['bindings'][k] is not None)==(v=='known') for k,v in p['binding_states'].items()),'Manifest hash binds the supplied synthetic descriptor; unknown/not-applicable never receives an invented digest.')
        domain=[n['capability_id'] for n in p['nodes'] if n['family_id']!='EQA']
        record('D18-'+profile['profile_id'],set(domain)==set(profile['required_capabilities']) and len(domain)==len(set(domain)) and domain.index('citation_identity')<domain.index('scholarly_integrity'),'Every required capability represented once; RCI precedes SEI.')
        record('D19-'+profile['profile_id'],all(n['lane_class'] in ['offline_batch','internet','chat_reasoning','human'] for n in p['nodes']) and all(n['lane_class']=='human' and not n['dispatchable'] for n in p['nodes'] if n['kind']=='human'),'Lane vocabulary and nondispatchable human nodes.')
    p=pp[1];nodes={n['node_id']:n for n in p['nodes']}
    record('D20',nodes['copyediting']['operation']=='record_gap' and 'component_profile_approved' in nodes['component_readiness']['hard_preconditions'] and 'accepted_copyedited_baseline_receipt' in nodes['proof_survival']['hard_preconditions'],'CE gap and CPR/PPR hard requirements encoded.')
    record('D21',not valid('stage-plan',load('examples/invalid-model-approval-plan.json')),'Supplied model-approval plan is structurally inexpressible.')
    machine=copy.deepcopy(nodes['proof_survival'])
    for operation in ['approve_plan','record_edit_decision','resolve_policy','adjudicate_integrity','approve_release_package','authorize_publication']:
        bad=copy.deepcopy(machine);bad['operation']=operation
        record('D22-'+operation,not valid('stage-node',bad),'Reserved or publication action rejected in a machine node.')
    human=copy.deepcopy(nodes['human_acceptance']);human['dispatchable']=True
    record('D23',not valid('stage-node',human),'Even human-typed nodes cannot set dispatchable true.')
    bad=copy.deepcopy(p);bad['execution_authorized']=True
    record('D24',not valid('stage-plan',bad),'Candidate specimen cannot be relabeled execution-authorized.')
    altered=copy.deepcopy(p);altered['bindings']['proof']='f'*64
    record('D25',not hash_matches(altered),'Changing proof binding invalidates plan digest; this is a design hash check, not live stale-result enforcement.')
    altered=copy.deepcopy(p);altered['nodes'][0]['depends_on']=['human_acceptance']
    record('D26',not dag_valid(altered['nodes']),'A deliberately cyclic ordered plan fails design validation.')
    decision=load('examples/production-proof-release-decision.json');cov=decision['coverage']
    record('D27',valid('release-decision',decision) and decision['status']=='hold' and 'CE_REQUIRED_ABSENT' in decision['blockers'] and cov['known']+cov['unknown']+cov['not_applicable']==cov['total'],'Synthetic diagnostic decision retains CE/draft holds and coverage.')
    bad=copy.deepcopy(decision);bad['publication_authorized']=True
    record('D28',not valid('release-decision',bad),'Publication-authorized result is inexpressible.')
    stress=load('examples/mwm-100-chapter-stress.json');chapters=stress['chapters']
    record('D29',len(chapters)==100 and len({c['chapter_id'] for c in chapters})==100 and {c['volume_id'] for c in chapters}=={'SYN-V1','SYN-V2'},'100 unique synthetic chapter identities in two volumes.')
    record('D30',sum(c['size_assumption_bytes'] for c in chapters)==419430400<524288000 and 100*20971520>524288000,'Four-MiB illustration fits; twenty-MiB-per-chapter illustration does not.')
    record('D31',math.ceil(100/stress['review_budget_per_day'])==9 and stress['review_budget_per_day']==12,'Review-budget illustration preserves twelve per day.')
    suite=load('conformance/cases.json');ids=suite['critical_case_ids']
    record('D32',len(ids)==24 and len(set(ids))==24 and all(x['case_id'] in ids and x['critical'] and x['runtime_status']=='not_run' for x in suite['cases']),'24 named critical adapter/runtime obligations; all remain unrun.')
    record('D33',contract['extensions']['university_press']['house_conformance']['status']=='commission_shape_checked_exact_upstream_unverified','Exact house-schema gap remains explicit.')
    record('D34',all(not e['implemented'] for e in contract['entry_points'].values()),'No proposed CLI verb labeled implemented.')
    record('D35',all(x['runtime_targets'][surface]['live_canary']=='not_run' for x in r.values() for surface in ['codex','claude','hermes','gemini','glm']),'No live surface parity fabricated.')
    record('D36',all(x['parent_plan_id'] is None and x['proof_cycle']==0 and x['reuse_descriptors']==[] for x in pp),'Initial specimens claim no prior proof or authorized result reuse.')
    return {'schema':'university_press.design_verification.draft1','status':'pass' if all(c['status']=='pass' for c in checks) else 'fail','scope':'Candidate schemas, evidence preservation, data consistency and synthetic design specimens only',
      'checks_run':len(checks),'checks_passed':sum(c['status']=='pass' for c in checks),'checks':checks,
      'not_run':['Exact upstream house-v1 conformance','Any implemented upw CLI or dispatcher','Family editorial fixtures or model reviews','24 adapter/runtime critical conformance cases','Authenticated authority/receipt verifier','Live Codex/Claude/Hermes/Gemini/GLM parity','MWM sample or bulk execution','Nine local-tree/remote comparisons','Kata/Linear/Notion integration'],
      'production_ready':False,'promotion':'none'}

if __name__=='__main__':
    try:result=main()
    except Exception as exc:
        result={'status':'error','error':str(exc),'checks':checks,'production_ready':False}
    print(json.dumps(result,ensure_ascii=False,indent=2))
    sys.exit(0 if result['status']=='pass' else 1)
