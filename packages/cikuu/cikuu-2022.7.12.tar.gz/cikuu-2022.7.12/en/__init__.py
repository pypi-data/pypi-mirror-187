# 2022.7.4 merge verbnet and terms code 
# 2022.5.28, redisgears's python is 3.7 , to be compatible 
# 2022.3.20, usage:  import en |  spacy.nlp("hello")   
import json,spacy,os,builtins,time,fileinput, sqlite3,traceback,sys
from spacy.tokens import DocBin,Doc,Token
from spacy.tokenizer import Tokenizer
from spacy.matcher import Matcher,DependencyMatcher
from spacy.lang.char_classes import ALPHA, ALPHA_LOWER, ALPHA_UPPER, CONCAT_QUOTES, LIST_ELLIPSES, LIST_ICONS
from spacy.util import compile_infix_regex

def custom_tokenizer(nlp): #https://stackoverflow.com/questions/58105967/spacy-tokenization-of-hyphenated-words
	infixes = (
		LIST_ELLIPSES
		+ LIST_ICONS
		+ [
			r"(?<=[0-9])[+\-\*^](?=[0-9-])",
			r"(?<=[{al}{q}])\.(?=[{au}{q}])".format(
				al=ALPHA_LOWER, au=ALPHA_UPPER, q=CONCAT_QUOTES
			),
			r"(?<=[{a}]),(?=[{a}])".format(a=ALPHA),
			#r"(?<=[{a}])(?:{h})(?=[{a}])".format(a=ALPHA, h=HYPHENS),
			r"(?<=[{a}0-9])[:<>=/](?=[{a}])".format(a=ALPHA),
		]
	)
	infix_re = compile_infix_regex(infixes)
	return Tokenizer(nlp.vocab, prefix_search=nlp.tokenizer.prefix_search,suffix_search=nlp.tokenizer.suffix_search,infix_finditer=infix_re.finditer,token_match=nlp.tokenizer.token_match,	rules=nlp.Defaults.tokenizer_exceptions)

def to_docbin(doc):
	doc_bin= spacy.tokens.DocBin()
	doc_bin.add(doc)
	return doc_bin.to_bytes()

def from_docbin(bs): 
	return list(spacy.tokens.DocBin().from_bytes(bs).get_docs(spacy.nlp.vocab))[0] if bs else None

if not hasattr(spacy, 'nlp'):
	spacy.nlp		= spacy.load(os.getenv('spacy_model','en_core_web_lg')) # 3.4.1
	spacy.tobs		= to_docbin # for old codes
	spacy.frombs	= from_docbin
	spacy.from_json = lambda arr: Doc(spacy.nlp.vocab).from_json(arr) # added 2022.8.19
	spacy.nlp.tokenizer = custom_tokenizer(spacy.nlp)	#nlp.tokenizer.infix_finditer = infix_re.finditer
	#print([t.text for t in nlp("It's 1.50, up-scaled haven't")]) # ['It', "'s", "'", '1.50', "'", ',', 'up-scaled', 'have', "n't"]

def refresh(): # to release spacy's memory , added 2023.1.20
	spacy.nlp = spacy.load(os.getenv('spacy_model','en_core_web_lg'))

def model(name:str='sm'):
	''' sm/md/lg, doc = en.model('lg')("hello world"),  2023.1.17 '''
	if not hasattr(model, name):  
		setattr(model, name, spacy.load(f'en_core_web_{name}') )
	return getattr(model, name) 
lookup	= lambda s, name='lg': model(name).vocab[s].text
fromjson= lambda jsons, name='lg': Doc(model(name).vocab).from_json(jsons)

def getdoc(snt, bs):  # execute("GET", f"bytes:{snt}") 
	return Doc(spacy.nlp.vocab).from_bytes(bs) if bs else spacy.nlp(snt) 

def phrase_matcher(name:str='pp', patterns:list=[[{'POS': 'ADP'},{"POS": {"IN": ["DET","NUM","ADJ",'PUNCT','CONJ']}, "OP": "*"},{"POS": {"IN": ["NOUN","PART"]}, "OP": "+"}]]):
	''' for name, ibeg,iend in matcher(doc) : print(spacy.nlp.vocab[name].text, doc[ibeg:iend].text) '''
	matcher = Matcher(spacy.nlp.vocab)
	matcher.add(name, patterns,  greedy ='LONGEST')
	return matcher

def sntbr(essay, trim:bool=False, with_pid:bool=False): 
	''' added 2022.5.28 '''
	from spacy.lang import en
	if not hasattr(sntbr, 'inst'): 
		sntbr.inst = en.English()
		sntbr.inst.add_pipe("sentencizer")

	doc = sntbr.inst(essay)
	if not with_pid: return [ snt.text.strip() if trim else snt.text for snt in  doc.sents]

	pid = 0 #spacy.sntpidoff	= lambda essay: (pid:=0, doc:=spacy.sntbr(essay), [ ( pid := pid + 1 if "\n" in snt.text else pid,  (snt.text, pid, doc[snt.start].idx))[-1] for snt in  doc.sents] )[-1]
	arr = []
	for snt in  doc.sents:
		if "\n" in snt.text: pid = pid + 1 
		arr.append( (snt.text, pid) ) 
	return arr 

#token_split	= lambda sent: re.findall(r"[\w']+|[.,!?;]", sent) # return list
def common_perc(snt="She has ready.", trans="She is ready."): 
	toks = set([t.text for t in spacy.nlp.tokenizer(snt)])
	return len([t for t in spacy.nlp.tokenizer(trans) if t.text in toks]) / (len(toks)+0.01)

merge_nps		= lambda : spacy.nlp.create_pipe("merge_noun_chunks")
new_matcher		= lambda : Matcher(spacy.nlp.vocab) # by exchunk
toks			= lambda doc:  [{'i':t.i, "head":t.head.i, 'lex':t.text, 'lem':t.lemma_, 'pos':t.pos_, 'tag':t.tag_, 'dep':t.dep_, "gpos":t.head.pos_, "glem":t.head.lemma_} for t in doc ] # JSONEachRow 
postag			= lambda doc:  "_^ " + " ".join([ f"{t.text}_{t.lemma_}_{t.pos_}_{t.tag_}" for t in doc]) + " _$"
non_root_verbs	= lambda doc:  [t for t in doc if t.pos_ == 'VERB' and t.dep_ != 'ROOT'] 
simple_sent		= lambda doc:  len([t for t in doc if t.pos_ == 'VERB' and t.dep_ != 'ROOT']) <= 0 # else is complex sent 
compound_snt	= lambda doc:  len([t for t in doc if t.dep_ == 'conj' and t.head.dep_ == 'ROOT']) > 0
snt_source		= lambda sid, doc: {'type':'snt', 'src': sid, 'snt':doc.text, 'pred_offset': pred_offset(doc), 
				'postag':'_^ ' + ' '.join([f"{t.text}_{t.lemma_}_{t.pos_}_{t.tag_}" if t.text == t.text.lower() else f"{t.text}_{t.text.lower()}_{t.lemma_}_{t.pos_}_{t.tag_}" for t in doc]) + ' _$',
			   'tc': len(doc)}

def pred_offset(doc):
	ar = [ t.i for t in doc if t.dep_ == "ROOT"]
	offset = ar[0] if len(ar) > 0 else 0
	return offset/( len(doc) + 0.1) 

def show(doc):
	''' used in the notebook, for debug '''
	import pandas as pd
	return pd.DataFrame({'word': [t.text for t in doc], 'tag': [t.tag_ for t in doc],'pos': [t.pos_ for t in doc],'head': [t.head.orth_ for t in doc],'dep': [t.dep_ for t in doc], 'lemma': [t.text.lower() if t.lemma_ == '-PRON-' else t.lemma_ for t in doc],
	'n_lefts': [ t.n_lefts for t in doc], 'left_edge': [ t.left_edge.text for t in doc], 
	'n_rights': [ t.n_rights for t in doc], 'right_edge': [ t.right_edge.text for t in doc],
	'subtree': str([ list(t.subtree) for t in doc]),'children': str([ list(t.children) for t in doc]),
	'morph': [ t.morph for t in doc],'ent_type': [ t.ent_type_ for t in doc],
	})

def parse(snt, merge_np= False):
	''' used in the notebook, for debug '''
	doc = spacy.nlp(snt)
	if merge_np : spacy.merge_nps(doc)
	return show(doc)

trp_rel		= lambda t:  f"{t.dep_}_{t.head.pos_}_{t.pos_}"  # dobj_VERB_NOUN
trp_reverse = set({"amod_NOUN_ADJ","nsubj_VERB_NOUN"})
trp_tok		= lambda doc, arr:  [ t for t in doc if [ t.dep_, t.head.pos_, t.pos_, t.head.lemma_, t.lemma_ ] == arr ] # arr is exactly 5 list 
gov_dep		= lambda rel, arr : (arr[0], arr[1]) if lemma_order.get(rel, True) else (arr[1], arr[0])  # open door
hit_trp		= lambda t, _rel, _gov_dep:   _rel == trp_rel(t) and _gov_dep == (t.head.lemma_, t.lemma_)
trp_high	= lambda doc, i, ihead :   "".join([ f"<b>{t.text_with_ws}</b>" if t.i in (i, ihead) else t.text_with_ws for t in doc ])
lem_high	= lambda doc, lem :   "".join([ f"<b>{t.text_with_ws}</b>" if t.lemma_ == lem else t.text_with_ws for t in doc ]) # highlight the first lemma 
vp_span		= lambda doc,ibeg,iend: doc[ibeg].lemma_ + " " + doc[ibeg+1:iend].text.lower()

def hyb(doc, start, pat): #l:lemma x:text, p:pos t:tag , e:ent_type 
	arr = []
	for i,c in enumerate(pat): 
		if c == 'l':	arr.append(doc[start +i].lemma_)
		elif c == 'p':	arr.append(doc[start +i].pos_)
		elif c == 't':	arr.append(doc[start +i].tag_)
		elif c == 'e':	arr.append(doc[start +i].ent_type_)
		elif c == 'x':	arr.append(doc[start +i].text.lower())
		else :			arr.append(doc[start +i].text.lower())
	return ' '.join(arr) 

def kp_span(doc, start, end, name):  # base:VERB:be_vbn_p:be based on   | lem, pos, type, chunk 
	if name.startswith('v'):		return (doc[start].lemma_,doc[start].pos_, name,vp_span(doc,start,end) )
	elif name.startswith("be_") :	return (doc[start+1].lemma_,doc[start+1].pos_,name,vp_span(doc,start,end))
	elif name in ('ap','pp','Vend'):return (doc[end-1].lemma_,doc[end-1].pos_,name,doc[start:end].text.lower())
	else:							return (doc[start].lemma_,doc[start].pos_,name,doc[start:end].text.lower())

kp_rules = {
"Vend":[[{"POS": {"IN": ["AUX","VERB"]}},{"POS": {"IN": ["ADV"]}, "OP": "*"}, {"POS": {"IN": ["ADJ","VERB"]}, "OP": "*"},{"POS": {"IN": ["PART","ADP","TO"]}, "OP": "*"},{"POS": 'VERB'}]], # could hardly wait to meet
"vp":  [[{'POS': 'VERB'},{"POS": {"IN": ["DET","ADP","ADJ"]}, "OP": "*"},{"POS": 'NOUN'}, {"POS": {"IN": ["ADP","TO"]}, "OP": "*"}], [{'POS': 'VERB'},{"POS": {"IN": ["DET","ADP","ADJ","TO","PART"]}, "OP": "*"},{"POS": 'VERB'}]], # wait to meet
"pp":  [[{'POS': 'ADP'},{"POS": {"IN": ["DET","NUM","ADJ",'PUNCT','CONJ']}, "OP": "*"},{"POS": {"IN": ["NOUN","PART"]}, "OP": "+"}]],    
"ap":  [[{"POS": {"IN": ["ADV"]}, "OP": "+"}, {"POS": 'ADJ'}]],  
"vprt":	[[{"POS": 'VERB', "TAG": {"NOT_IN": ["VBN"]}}, {"POS": {"IN": ["PREP", "ADP",'TO']}, "OP": "+"}]],   # look up /look up from,  computed twice
"vtov":	[[{"POS": 'VERB', "TAG": {"NOT_IN": ["VBN"]}}, {"TAG": 'TO'},{"TAG": 'VB'}]],   # plan to go
"vvbg":	[[{"POS": 'VERB', "TAG": {"NOT_IN": ["VBN"]}}, {"TAG": 'VBG'}]],   # consider going
"vpg":	[[{"POS": 'VERB', "TAG": {"NOT_IN": ["VBN"]}}, {"POS": {"IN": ["PREP", "ADP",'PART']}, "OP": "+"},{"TAG": 'VBG'}]],   # insisted on going
"be_vbn_p": [[{'LEMMA': 'be'},{"TAG": {"IN": ["VBN"]}}, {"POS": {"IN": ["PREP", "ADP",'PART']}}]],   # base:VERB:be_vbn_p:be based on   
"be_adj_p": [[{'LEMMA': 'be'},{"POS": {"IN": ["ADJ"]}}, {"POS": {"IN": ["PREP", "ADP",'PART']}}]],   # be angry with
} #for name, ibeg,iend in matcher(doc) : print(spacy.nlp.vocab[name].text, doc[ibeg:iend].text)

def kp_matcher(doc): #[('vend', 'consider going', 1, 3), ('vp', 'consider going', 1, 3), ('vvbg', 'consider going', 1, 3), ('vprt', 'going to', 2, 4)]
	if not hasattr(kp_matcher, 'matcher'): 
		kp_matcher.matcher = Matcher(spacy.nlp.vocab)
		[kp_matcher.matcher.add(name, patterns,  greedy ='LONGEST') for name, patterns in kp_rules.items() ]
	tups = set()  # remove the duplicated entries 
	[tups.add( kp_span(doc,ibeg,iend, spacy.nlp.vocab[name].text) ) for name, ibeg,iend in kp_matcher.matcher(doc)] 
	return tups

def ruler(snt, name:str='sm'):
	''' 2023.1.21 '''
	if not hasattr(ruler, name):  
		_nlp = spacy.load(f'en_core_web_{name}')
		setattr(ruler, name, _nlp )
		_ruler = _nlp.add_pipe("span_ruler")
		patterns = [{"label": "PP", "pattern": [{'POS': 'ADP'},{"POS": {"IN": ["DET","NUM","ADJ",'PUNCT','CONJ']}, "OP": "*"},{"POS": {"IN": ["NOUN","PART","PROPN"]}, "OP": "+"}]},
            {"label": "VP", "pattern": [{'POS': 'VERB'},{"POS": {"IN": ["DET","ADP","ADJ"]}, "OP": "*"},{"POS": 'NOUN'}, {"POS": {"IN": ["ADP","TO"]}, "OP": "*"}]},
			{"label": "Vend", "pattern": [{"POS": {"IN": ["AUX","VERB"]}},{"POS": {"IN": ["ADV"]}, "OP": "*"}, {"POS": {"IN": ["ADJ","VERB"]}, "OP": "*"},{"POS": {"IN": ["PART","ADP","TO"]}, "OP": "*"},{"POS": 'VERB'}]},
			{"label": "AP", "pattern": [{"POS": {"IN": ["ADV"]}, "OP": "+"}, {"POS": 'ADJ'}]},
			{"label": "vtov", "pattern": [{"POS": 'VERB', "TAG": {"NOT_IN": ["VBN"]}}, {"TAG": 'TO'},{"TAG": 'VB'}]},
			{"label": "vvbg", "pattern": [{"POS": 'VERB', "TAG": {"NOT_IN": ["VBN"]}}, {"TAG": 'VBG'}]},
			{"label": "vprt", "pattern": [{"POS": 'VERB', "TAG": {"NOT_IN": ["VBN"]}}, {"POS": {"IN": ["PREP", "ADP",'TO']}, "OP": "+"}]},
			{"label": "vpg", "pattern": [{"POS": 'VERB', "TAG": {"NOT_IN": ["VBN"]}}, {"POS": {"IN": ["PREP", "ADP",'PART']}, "OP": "+"},{"TAG": 'VBG'}]},# insisted on going
			{"label": "be_vbn_p", "pattern": [{'LEMMA': 'be'},{"TAG": {"IN": ["VBN"]}}, {"POS": {"IN": ["PREP", "ADP",'PART']}}]},# base:VERB:be_vbn_p:be based on   
			{"label": "be_adj_p", "pattern": [{'LEMMA': 'be'},{"POS": {"IN": ["ADJ"]}}, {"POS": {"IN": ["PREP", "ADP",'PART']}}]},# be angry with
			]
		_ruler.add_patterns(patterns)
	return getattr(ruler, name)(snt)  #print([(span.text, span.label_) for span in  doc.spans["ruler"] ])

# added 2022.7.25
post_np_rules = { # after np is merged 
"v_n_vbn": [[{"POS": 'VERB', "TAG": {"NOT_IN": ["VBN"]}},{"POS": {"IN": ["NOUN"]}}, {"TAG": {"IN": ["VBN"]}}]],   # leave the book opened 
"v_n_adj": [[{"POS": 'VERB', "TAG": {"NOT_IN": ["VBN"]}},{"POS": {"IN": ["NOUN"]}}, {"POS": {"IN": ["ADJ"]}}]],
} #for name, ibeg,iend in matcher(doc) : print(spacy.nlp.vocab[name].text, doc[ibeg:iend].text)
def post_np_matcher(doc): 
	if not hasattr(post_np_matcher, 'matcher'): 
		post_np_matcher.matcher = Matcher(spacy.nlp.vocab)
		[post_np_matcher.matcher.add(name, patterns,  greedy ='LONGEST') for name, patterns in post_np_rules.items() ]
	return [(spacy.nlp.vocab[name].text,ibeg,iend) for name, ibeg,iend in post_np_matcher.matcher(doc)] 

def new_matcher(patterns, name='pat'):
	matcher = Matcher(spacy.nlp.vocab)
	matcher.add(name, patterns, greedy ='LONGEST')
	return matcher
matchers = {  # for name,start,end in matchers['ap'](doc) :
"vend":new_matcher([[{"POS": {"IN": ["AUX","VERB"]}},{"POS": {"IN": ["ADV"]}, "OP": "*"}, {"POS": {"IN": ["ADJ","VERB"]}, "OP": "*"},{"POS": {"IN": ["PART","ADP","TO"]}, "OP": "*"},{"POS": 'VERB'}]]), # could hardly wait to meet
"vp":  new_matcher([[{'POS': 'VERB'},{"POS": {"IN": ["DET","ADP","ADJ"]}, "OP": "*"},{"POS": 'NOUN'}, {"POS": {"IN": ["ADP","TO"]}, "OP": "*"}], #He paid a close attention to the book. |He looked up from the side. | make use of
                     [{'POS': 'VERB'},{"POS": {"IN": ["DET","ADP","ADJ","TO","PART"]}, "OP": "*"},{"POS": 'VERB'}]]), # wait to meet
"pp":  new_matcher([[{'POS': 'ADP'},{"POS": {"IN": ["DET","NUM","ADJ",'PUNCT','CONJ']}, "OP": "*"},{"POS": {"IN": ["NOUN","PART"]}, "OP": "+"}]]),    
"ap":  new_matcher([[{"POS": {"IN": ["ADV"]}, "OP": "*"}, {"POS": 'ADJ'}]]),  
"vprt": new_matcher([[{"POS": 'VERB', "TAG": {"NOT_IN": ["VBN"]}}, {"POS": {"IN": ["PREP", "ADP",'TO']}, "OP": "+"}]]),   # look up /look up from,  computed twice
"vtov": new_matcher([[{"POS": 'VERB', "TAG": {"NOT_IN": ["VBN"]}}, {"TAG": 'TO'},{"TAG": 'VB'}]]),   # plan to go
"vvbg": new_matcher([[{"POS": 'VERB', "TAG": {"NOT_IN": ["VBN"]}}, {"TAG": 'VBG'}]]),   # consider going
"vpg":  new_matcher([[{"POS": 'VERB', "TAG": {"NOT_IN": ["VBN"]}}, {"POS": {"IN": ["PREP", "ADP",'PART']}, "OP": "+"},{"TAG": 'VBG'}]]),   # insisted on going
"vAp":  new_matcher([[{'LEMMA': 'be'},{"TAG": {"IN": ["VBN"]}}, {"POS": {"IN": ["PREP", "ADP",'PART']}}]]),   # be based on   
"vap":  new_matcher([[{'LEMMA': 'be'},{"POS": {"IN": ["ADJ"]}}, {"POS": {"IN": ["PREP", "ADP",'PART']}}]]),   # be angry with
} #for name, ibeg,iend in matcher(doc) : print(spacy.nlp.vocab[name].text, doc[ibeg:iend].text)

##
## from verbnet.py
##
def merge_np(doc):
	with doc.retokenize() as retokenizer:
		for np in doc.noun_chunks:
			attrs = {"tag": np.root.tag, "dep": np.root.dep, "ent_type": "NP", "lemma":doc[np.end-1].lemma} # , "lemma":doc[np.end-1].lemma | added 2022.7.26
			retokenizer.merge(np, attrs=attrs) 
	return doc

def skenp(doc, tag="_NP"): # added 2022.3.22, for skevec
	merge_np(doc) # transform doc , finally to be called 
	return " ".join([tag if t.ent_type_ == 'NP' else t.text for t in doc])

def merge_n_of_n(doc):
	if not hasattr(merge_n_of_n, 'matcher'):
		merge_n_of_n.matcher = Matcher(spacy.nlp.vocab)
		merge_n_of_n.matcher.add("n-of-n", [[{"ENT_TYPE": "NP"}, {"LEMMA":"of"},{"ENT_TYPE": "NP"}], [{"ENT_TYPE": "NP"}, {"LEMMA":"of"},{"POS": "NOUN"}]],  greedy ='LONGEST')
	with doc.retokenize() as retokenizer:
		for name, start, end in merge_n_of_n.matcher(doc):
			if end - start > 1: 
				try:
					i = doc[start].head.i
					attrs = {"pos": doc[i].pos, "tag": doc[i].tag, "dep": doc[i].dep, "lemma":doc[i].lemma, "ent_type": "NP"}
					retokenizer.merge(doc[start : end], attrs=attrs)
				except Exception as e:
					print ( "merge_n_of_n ex:", e , start, end)
	return doc

def merge_vp(doc):
	if not hasattr(merge_vp, 'matcher'):
		merge_vp.matcher = Matcher(spacy.nlp.vocab)
		merge_vp.matcher.add("vp", [[{"POS": {"IN":["AUX","PART"]}, "op": "*"}, {"POS":"VERB"},{"POS": "ADV", "op": "*"}]],  greedy ='LONGEST')
	with doc.retokenize() as retokenizer:
		for name, start, end in merge_vp.matcher(doc):
			if end - start > 1: 
				try:
					i = doc[start].head.i
					attrs = {"pos": doc[i].pos, "tag": doc[i].tag, "dep": doc[i].dep, "lemma":doc[i].lemma, "ent_type": "VP"}
					retokenizer.merge(doc[start : end], attrs=attrs)
				except Exception as e:
					print ( "merge_vp ex:", e , start, end)
	return doc

def merge_pp(doc): 
	if not hasattr(merge_pp, 'matcher'):
		merge_pp.matcher = Matcher(spacy.nlp.vocab)
		merge_pp.matcher.add("pp", [[{"POS": {"IN":["ADP"]}, "op": "+"}, {"ENT_TYPE":"NP", "op": "+"}]],  greedy ='LONGEST')
	with doc.retokenize() as retokenizer:
		for name, start, end in merge_pp.matcher(doc):
			if end - start > 1: 
				try:
					i = doc[start].head.i
					attrs = {"pos": doc[i].pos, "tag": doc[i].tag, "dep": doc[i].dep, "lemma":doc[i].lemma, "ent_type": "PP"}
					retokenizer.merge(doc[start : end], attrs=attrs)
				except Exception as e:
					print ( "merge_pp ex:", e , start, end)
	return doc

def skepp(doc, tag="_PP"): # added 2022.3.24,  | From the book, this is also difficult to .. 
	merge_pp(doc) # transform doc , finally to be called 
	return " ".join([tag if t.ent_type_ == 'PP' else t.text for t in doc])

def merge_clause(doc): # subtree of a verb is the clause , https://subscription.packtpub.com/book/data/9781838987312/2/ch02lvl1sec13/splitting-sentences-into-clauses
	with doc.retokenize() as retokenizer:
		for v in [t for t in doc if t.pos_ == 'VERB' and t.dep_ != 'ROOT' ] : # non-root
			try:
				children = list(v.subtree)
				start = children[0].i  	
				end = children[-1].i 
				attrs = {"pos": v.pos, "tag": v.tag, "dep": v.dep, "lemma":v.lemma, "ent_type": "S." + v.dep_ } # S.advcl ,  S.conj 
				retokenizer.merge(doc[start : end+1], attrs=attrs)
			except Exception as e:
				print ( "merge_clause ex:", e, v )
	return doc

NP_start = {"ENT_TYPE": "NP", "IS_SENT_START": True}
VERB	 = {"POS": {"IN": ["VERB"]}}
NOUN	 = {"POS": {"IN": ["NOUN","PRON","PROPN"]}}
PUNCT	 = {"IS_PUNCT": True}
_verbnet_rules = {  # :1 , verb's offset 
	"NP V:1": [[NP_start,VERB, PUNCT]], 
	"NP of NP V:3": [[ NP_start,{"LEMMA": "of"}, {"ENT_TYPE": "NP"}, VERB,PUNCT]], 
	"NP V NP:1": [[NOUN,VERB, NOUN,{"POS": {"IN": ["PUNCT"]}}]], 
	"NP V NP ADJ:1": [[NOUN,VERB, NOUN,{"POS": {"IN": ["ADJ"]}}]], 
	"NP V NP NP:1": [[NOUN,VERB, NOUN,NOUN]], 
	"NP V NP-Dative NP:1": [[NOUN,VERB, {"DEP": {"IN": ["dative"]}},NOUN]], 
	"NP V NP PP:1": [[NOUN,VERB, NOUN,{"DEP": {"IN": ["prep"]}}]], 
	"NP V NP PP PP:1": [[NOUN,VERB, NOUN,{"DEP": {"IN": ["prep"]}}, NOUN,{"DEP": {"IN": ["prep"]}}, NOUN]], 
	"NP V S_ING:1": [[NOUN,VERB, {"TAG": {"IN": ["VBG"]}}]], 
	"NP V whether/how S_INF:1": [[NOUN,VERB, {"LEMMA": {"IN": ["whether","how"]}}, {"LEMMA": {"IN": ["to"]}}, VERB]], 
	"NP V NP to be NP:1": [[NOUN,VERB, {"LEMMA": {"IN": ["to"]}}, {"LEMMA": {"IN": ["be"]}}, NOUN]], 
	"NP V that/how S:1": [[NOUN,VERB, {"LEMMA": {"IN": ["that","how"]}, "OP":"*"}, NOUN, {"POS": {"IN": ["AUX","PART"]}, "OP":"*"},{"DEP": {"IN": ["ccomp"]}}]],  #They considered that he was the professor.
	"NP V whether/if S:1": [[NOUN,VERB, {"LEMMA": {"IN": ["whether","if"]}}, NOUN,{"POS": {"IN": ["AUX","PART"]}, "OP":"*"}, {"DEP": {"IN": ["ccomp"]}}]],  #He considered whether he should come.
	"NP V what S:1": [[NOUN,VERB, {"LEMMA": {"IN": ["what"]}}, NOUN,{"POS": {"IN": ["AUX","PART"]}, "OP":"*"}, {"DEP": {"IN": ["ccomp"]}}]],  
	"NP V what S_INF:1": [[NOUN,VERB, {"LEMMA": {"IN": ["what"]}}, {"LEMMA": {"IN": ["to"]}},VERB]],
}
def verbnet_matcher(doc): 
	if not hasattr(verbnet_matcher, 'matcher'): 
		verbnet_matcher.matcher = Matcher(spacy.nlp.vocab)
		[ verbnet_matcher.matcher.add(name, patterns, greedy ='LONGEST')  for name, patterns in _verbnet_rules.items() ]
	merge_np(doc)
	merge_vp(doc)
	res = []
	for name, ibeg, iend in verbnet_matcher.matcher(doc):
		try:
			arr = spacy.nlp.vocab[name].text.split(':') 
			verb_i = ibeg + int(arr[-1]) 
			res.append( (verb_i, ibeg, iend, arr[0].strip()) ) 
		except Exception as e:
			print ('verbnet ex:', e, name, ibeg, iend)
	return res 

simple_sent		= lambda doc: len([t for t in doc if t.pos_ == 'VERB' and t.dep_ != 'ROOT']) <= 0 
complex_sent	= lambda doc: len([t for t in doc if t.pos_ == 'VERB' and t.dep_ != 'ROOT']) > 0
compound_sent	= lambda doc: len([t for t in doc if t.dep_ == 'conj' and t.head.dep_ == 'ROOT']) > 0  # S.conj 
stype			= lambda doc:	"simple_sent" if len([t for t in doc if t.pos_ == 'VERB' and t.dep_ != 'ROOT']) <= 0 else "complex_sent"
skeleton		= lambda doc:  " ".join([ t.ent_type_ if t.ent_type_ else t.text if t.is_punct or t.dep_ == 'ROOT' else t.pos_ for t in doc ])

def clause(doc):  # {'S.prep-0': {'type': 'S.prep', 'start': 0, 'end': 2, 'lem': 'consider', 'chunk': 'Considering the possibility'}, 'S.conj-9': {'type': 'S.conj', 'start': 9, 'end': 12, 'lem': 'be', 'chunk': 'she is ok .'}}
	arr = []
	for v in [t for t in doc if t.pos_ == 'VERB' and t.dep_ != 'ROOT' ] : # non-root
		children = list(v.subtree) #end = children[-1].i 	tag = "S." + v.dep_   # S.advcl ,  S.conj 
		start = children[0].i
		end = children[-1].i + 1 #"type":"cl", "kp": "S." + v.dep_,
		arr.append( (v, v.dep_, start, end, " ".join([c.text for c in v.subtree])) ) #last one is 'chunk'   lempos":v.lemma_ + "_" + v.pos_,"chunk": } #"lem":v.lemma_, NOT confuse with 'tok' 
	return arr 

_vp_rules = {
"vend":[[{"POS": {"IN": ["AUX","VERB"]}},{"POS": {"IN": ["ADV"]}, "OP": "*"}, {"POS": {"IN": ["ADJ","VERB"]}, "OP": "*"},{"POS": {"IN": ["PART","ADP","TO"]}, "OP": "*"},{"POS": 'VERB'}]], # could hardly wait to meet
"vp":  [[{'POS': 'VERB'},{"POS": {"IN": ["DET","ADP","ADJ"]}, "OP": "*"},{"POS": 'NOUN'}, {"POS": {"IN": ["ADP","TO"]}, "OP": "*"}], [{'POS': 'VERB'},{"POS": {"IN": ["DET","ADP","ADJ","TO","PART"]}, "OP": "*"},{"POS": 'VERB'}]], # wait to meet
"pp":  [[{'POS': 'ADP'},{"POS": {"IN": ["DET","NUM","ADJ",'PUNCT','CONJ']}, "OP": "*"},{"POS": {"IN": ["NOUN","PART"]}, "OP": "+"}]],    
"ap":  [[{"POS": {"IN": ["ADV"]}, "OP": "*"}, {"POS": 'ADJ'}]],  
"vprt":[[{"POS": 'VERB'}, {"POS": {"IN": ["PREP", "ADP",'TO']}, "OP": "+"}]],   # look up /look up from,  computed twice
"vtov":[[{"POS": 'VERB'}, {"TAG": 'TO'},{"TAG": 'VB'}]],   # plan to go
"vvbg":[[{"POS": 'VERB'}, {"TAG": 'VBG'}]],   # consider going
"vpg": [[{"POS": 'VERB'}, {"POS": {"IN": ["PREP", "ADP",'PART']}, "OP": "+"},{"TAG": 'VBG'}]],   # insisted on going
"vAp": [[{'LEMMA': 'be'},{"TAG": {"IN": ["VBN"]}}, {"POS": {"IN": ["PREP", "ADP",'PART']}}]],   # be based on   
"vap": [[{'LEMMA': 'be'},{"POS": {"IN": ["ADJ"]}}, {"POS": {"IN": ["PREP", "ADP",'PART']}}]],   # be angry with
} #for name, ibeg,iend in matcher(doc) : print(spacy.nlp.vocab[name].text, doc[ibeg:iend].text)

def vp_matcher(doc): #[('vend', 'consider going', 1, 3), ('vp', 'consider going', 1, 3), ('vvbg', 'consider going', 1, 3), ('vprt', 'going to', 2, 4)]
	if not hasattr(vp_matcher, 'matcher'): 
		vp_matcher.matcher = Matcher(spacy.nlp.vocab)
		[vp_matcher.matcher.add(name, patterns,  greedy ='LONGEST') for name, patterns in _vp_rules.items() ]
	#return [(spacy.nlp.vocab[name].text, vp_span(doc,ibeg,iend), ibeg, iend) for name, ibeg,iend in vp_matcher.matcher(doc)] 
	tups = set()  # remove the duplicated entries 
	[tups.add((spacy.nlp.vocab[name].text, vp_span(doc,ibeg,iend), ibeg, iend)) for name, ibeg,iend in vp_matcher.matcher(doc)] 
	return tups

_dep_rules = {
"svo":[ {"RIGHT_ID": "v",  "RIGHT_ATTRS": {"POS": "VERB"}}, {"LEFT_ID": "v", "REL_OP": ">", "RIGHT_ID": "subject", "RIGHT_ATTRS": {"DEP": "nsubj"}},{"LEFT_ID": "v", "REL_OP": ">", "RIGHT_ID": "object","RIGHT_ATTRS": {"DEP": "dobj"}  }], # [(4851363122962674176, [2, 0, 4])]
"sva":[ 
  {
    "RIGHT_ID": "v",
    "RIGHT_ATTRS": {"POS": "VERB"}
  },
  {
    "LEFT_ID": "v",
    "REL_OP": ">",
    "RIGHT_ID": "subject",
    "RIGHT_ATTRS": {"DEP": "nsubj"}
  },
  {
    "LEFT_ID": "v",
    "REL_OP": ">",
    "RIGHT_ID": "object",
    "RIGHT_ATTRS": {"DEP": "acomp"}
  }
], 
"svx":[  # plan to go , enjoy swimming 
  {
    "RIGHT_ID": "v",
    "RIGHT_ATTRS": {"POS": "VERB"}
  },
  {
    "LEFT_ID": "v",
    "REL_OP": ">",
    "RIGHT_ID": "subject",
    "RIGHT_ATTRS": {"DEP": "nsubj"}
  },
  {
    "LEFT_ID": "v",
    "REL_OP": ">",
    "RIGHT_ID": "object",
    "RIGHT_ATTRS": {"DEP": "xcomp"}
  }
], 
"svc":[  # I think it is right.
  {
    "RIGHT_ID": "v",
    "RIGHT_ATTRS": {"POS": "VERB"}
  },
  {
    "LEFT_ID": "v",
    "REL_OP": ">",
    "RIGHT_ID": "subject",
    "RIGHT_ATTRS": {"DEP": "nsubj"}
  },
  {
    "LEFT_ID": "v",
    "REL_OP": ">",
    "RIGHT_ID": "object",
    "RIGHT_ATTRS": {"DEP": "ccomp"}
  }
], 
"sattr":[  #She is  a girl.
  {
    "RIGHT_ID": "v",
    "RIGHT_ATTRS": {"LEMMA": "be"}
  },
  {
    "LEFT_ID": "v",
    "REL_OP": ">",
    "RIGHT_ID": "subject",
    "RIGHT_ATTRS": {"DEP": "nsubj"}
  },
  {
    "LEFT_ID": "v",
    "REL_OP": ">",
    "RIGHT_ID": "object",
    "RIGHT_ATTRS": {"DEP": "attr"}
  }
], 
"vpn":[ # turn off the light
  {
    "RIGHT_ID": "v",
    "RIGHT_ATTRS": {"POS": "VERB"}
  },
  {
    "LEFT_ID": "v",
    "REL_OP": ">",
    "RIGHT_ID": "subject",
    "RIGHT_ATTRS": {"DEP": "prt"}
  },
  {
    "LEFT_ID": "v",
    "REL_OP": ">",
    "RIGHT_ID": "object",
    "RIGHT_ATTRS": {"DEP": "dobj"}
  }
], 
"vap":[ # be happy with
  {
    "RIGHT_ID": "v",
    "RIGHT_ATTRS": {"POS": "VERB"}
  },
  {
    "LEFT_ID": "v",
    "REL_OP": ">",
    "RIGHT_ID": "acomp",
    "RIGHT_ATTRS": {"DEP": "acomp"}
  },
  {
    "LEFT_ID": "acomp",
    "REL_OP": ">",
    "RIGHT_ID": "prep",
    "RIGHT_ATTRS": {"DEP": "prep"}
  }
], 
"vdp":[ # be based on
  {
    "RIGHT_ID": "v",
    "RIGHT_ATTRS": {"TAG": "VBN"}
  },
  {
    "LEFT_ID": "v",
    "REL_OP": ">",
    "RIGHT_ID": "be",
    "RIGHT_ATTRS": {"LEMMA": "be"}
  },
  {
    "LEFT_ID": "v",
    "REL_OP": ">",
    "RIGHT_ID": "prep",
    "RIGHT_ATTRS": {"DEP": "prep"}
  }
], 
"vppn":[ # look up from phone
  {
    "RIGHT_ID": "v",
    "RIGHT_ATTRS": {"POS": "VERB"}
  },
  {
    "LEFT_ID": "v",
    "REL_OP": ">",
    "RIGHT_ID": "prt",
    "RIGHT_ATTRS": {"DEP": "prt"}
  },
  {
    "LEFT_ID": "v",
    "REL_OP": ">",
    "RIGHT_ID": "prep",
    "RIGHT_ATTRS": {"DEP": "prep"}
  },
  {
    "LEFT_ID": "prep",
    "REL_OP": ">",
    "RIGHT_ID": "object",
    "RIGHT_ATTRS": {"DEP": "pobj"}
  }
], 
"vpnpn":[ # vary from A to B
  {
    "RIGHT_ID": "v",
    "RIGHT_ATTRS": {"POS": "VERB"}
  },
  {
    "LEFT_ID": "v",
    "REL_OP": ">",
    "RIGHT_ID": "prep1",
    "RIGHT_ATTRS": {"DEP": "prep"}
  },
  {
    "LEFT_ID": "prep1",
    "REL_OP": ">",
    "RIGHT_ID": "object1",
    "RIGHT_ATTRS": {"DEP": "pobj"}
  },
  {
    "LEFT_ID": "v",
    "REL_OP": ">",
    "RIGHT_ID": "prep2",
    "RIGHT_ATTRS": {"DEP": "prep"}
  },
  {
    "LEFT_ID": "prep2",
    "REL_OP": ">",
    "RIGHT_ID": "object2",
    "RIGHT_ATTRS": {"DEP": "pobj"}
  }
], 
"vnp":[ # turn it down
  {
    "RIGHT_ID": "v",
    "RIGHT_ATTRS": {"POS": "VERB"}
  },
  {
    "LEFT_ID": "v",
    "REL_OP": ">",
    "RIGHT_ID": "object",
    "RIGHT_ATTRS": {"DEP": "dobj"}
  },
  {
    "LEFT_ID": "v",
    "REL_OP": ">",
    "RIGHT_ID": "subject",
    "RIGHT_ATTRS": {"DEP": "prt"}
  }
], 
"vnpn":[  # make use of books, take sth into account
  {
    "RIGHT_ID": "v",
    "RIGHT_ATTRS": {"POS": "VERB"}
  },
  {
    "LEFT_ID": "v",
    "REL_OP": ">",
    "RIGHT_ID": "object",
    "RIGHT_ATTRS": {"DEP": "dobj"}
  },
  {
    "LEFT_ID": "object",
    "REL_OP": ">",
    "RIGHT_ID": "prep",
    "RIGHT_ATTRS": {"DEP": "prep"}
  },
  {
    "LEFT_ID": "prep",
    "REL_OP": ">",
    "RIGHT_ID": "pobj",
    "RIGHT_ATTRS": {"DEP": "pobj"}
  }  
], 
} # for name, ar in depmatchers['svx'](doc) : print(doc[ar[1]], doc[ar[0]], doc[ar[2]])

def dep_matcher(doc): #[('svx', [1, 0, 2])]
	if not hasattr(dep_matcher, 'matcher'): 
		dep_matcher.matcher = DependencyMatcher(spacy.nlp.vocab)
		[dep_matcher.matcher.add(name, [pattern]) for name, pattern in _dep_rules.items() ]
	return [(spacy.nlp.vocab[name].text, ar) for name, ar in dep_matcher.matcher(doc)] 
	#for name, ar in depmatchers['svx'](doc) : print(doc[ar[1]], doc[ar[0]], doc[ar[2]])

es_toks = lambda sid, doc:  [ {'_id': f"{sid}-tok-{t.i}", '_source': {"type":"tok", "src":sid, 'i':t.i, "head":t.head.i, 'lex':t.text, 'lem':t.lemma_, 'pos':t.pos_, 'tag':t.tag_, 'dep':t.dep_, "gpos":t.head.pos_, "glem":t.head.lemma_ } } for t in doc ] 
def es_postag(doc): 
	from dic.oneself import oneself 
	return "_^ " + ' '.join([ f"_{t.pos_}_{t.tag_}" if t.pos_ in ('PROPN','NUM','X','SPACE') else f"{t.text if t.text in ('I') else t.text.lower()}_{t.lemma_}_{t.pos_}_{t.tag_}{oneself.get(t.text.lower(), '')}"  for t in doc]) # uniq by ana #,'PUNCT'

# added 2023.1.16, not tested yet
cl_root = lambda t: t.dep_ != 'ROOT' and ( (t.pos_ == 'VERB' and t.tag_ != 'VBN')  or (t.pos_ == 'AUX' and t.lemma_ == 'be') )
def mark_cl(doc):
    for t in doc: 
        if cl_root(t) : t.ent_id_ = 'cl_root'
leave_cl = lambda t: cl_root(t) and len([tr for tr in t.subtree if tr.ent_id_ == 'cl_root']) == 1
def merge_leave_cl(doc): #doc = spacy.nlp("While I was thrilled that it was ok, I worried that I would fail.")
	mark_cl(doc)
	with doc.retokenize() as retokenizer:
		for v in [t for t in doc if leave_cl(t) ] : # non-root
			try:
				children = list(v.subtree)
				start = children[0].i  	
				end = children[-1].i 
				attrs = {"pos": v.pos, "tag": v.tag, "dep": v.dep, "lemma":v.lemma, "ent_type": "S." + v.dep_ } # S.advcl ,  S.conj 
				if v.dep_ not in ('xcomp') and doc[start].lemma_ not in ('to') and doc[start].tag_ not in ('TO'): # skip to-clause  | He made the choice to give all his money away .
					retokenizer.merge(doc[start : end+1], attrs=attrs)
			except Exception as e:
				print ( "merge_leave_cl ex:", e, v )
	return doc 

def merge_ccomp(doc): #doc = spacy.nlp("While I was thrilled that it was ok, I worried that I would fail.")
	with doc.retokenize() as retokenizer:
		for v in [t for t in doc if t.pos_ == 'VERB' and t.dep_ == 'ccomp' and t.tag_ not in ('VBN') ] : # non-root
			try:
				children = list(v.subtree)
				start = children[0].i  	
				end = children[-1].i 
				attrs = {"pos": v.pos, "tag": v.tag, "dep": v.dep, "lemma":v.lemma, "ent_type": "S." + v.dep_ } # S.advcl ,  S.conj 
				retokenizer.merge(doc[start : end+1], attrs=attrs)
			except Exception as e:
				print ( "merge_ccomp ex:", e, v )
	return doc 

def es_skenp(doc):
	from dic.oneself import oneself 
	merge_ccomp(doc) # merge_leave_cl(doc) 
	merge_np(doc) # transform doc , finally to be called | f"_{t.lemma_}_{t.pos_}_{t.tag_}_cl_{t.dep_}"
	return "_^ " + ' '.join([ f"_{t.lemma_}_NP_{t.dep_}" if t.ent_type_ == 'NP' else f"_CL_{t.dep_}" if t.ent_type_.startswith("S.") else f"_{t.pos_}_{t.tag_}_{t.dep_}" if t.pos_ in ('PROPN','NUM','X','SPACE') else f"{t.text if t.text in ('I') else t.text.lower()}_{t.lemma_}_{t.pos_}_{t.tag_}{oneself.get(t.text.lower(), '')}_{t.dep_}"  for t in doc]) # uniq by ana #,'PUNCT'

def merge_prt(doc): 
	'''I turn off the radio. => turn_off , added 2023.1.13'''
	if not hasattr(merge_prt, 'matcher'):
		merge_prt.matcher = Matcher(spacy.nlp.vocab)
		merge_prt.matcher.add("prt", [[{"POS":"VERB"}, {"POS":"ADP", "DEP":"prt"}]], greedy ='LONGEST')
	with doc.retokenize() as retokenizer:
		for name, start, end in merge_prt.matcher(doc):
			try:
				attrs = {"pos": doc[start].pos, "tag": doc[start].tag, "dep": doc[start].dep, "lemma":doc[start].lemma_ + "_" + doc[start+1].lemma_, "ent_type": "vprt"}
				retokenizer.merge(doc[start : end], attrs=attrs)
			except Exception as e:
				print ( "merge_prt ex:", e , start, end)
	return doc

def merged(doc): 
	if not hasattr(merged, 'matcher'):
		merged.matcher = Matcher(spacy.nlp.vocab)
		merged.matcher.add("vprt", [[{"POS":"VERB"}, {"POS":"ADP", "DEP":"prt"}]], greedy ='LONGEST')
		merged.matcher.add("vtov", [[{"POS":"VERB"},{"LEMMA":"to", "TAG":"TO"}, {"TAG":"VB"}]], greedy ='LONGEST')        
		merged.matcher.add("vvbg", [[{"POS":"VERB"},{"DEP":"xcomp","TAG":"VBG"}]], greedy ='LONGEST')                
	with doc.retokenize() as retokenizer:
		for name, start, end in merged.matcher(doc):
			try:
				attrs = {"pos": doc[start].pos, "tag": doc[start].tag, "dep": doc[start].dep, "lemma":"_".join([doc[i].lemma_ if i == start else doc[i].text for i in range(start,end)]), "ent_type": "merged_" + spacy.nlp.vocab[name].text}
				retokenizer.merge(doc[start : end], attrs=attrs)
			except Exception as e:
				print ( "merged ex:", e , start, end)
	return doc

def depmatch(): #from spacy.matcher import Matcher,DependencyMatcher
	''' 2023.1.6 '''
	if not hasattr(depmatch,'matcher'): 
		depmatch.matcher = DependencyMatcher(spacy.nlp.vocab)
		pattern = {
			# advcl-acomp worry be thrilled | "While I was thrilled that it was ok, I worried that she is happy."
			"advcl-acomp": [ {"RIGHT_ID": "v", "RIGHT_ATTRS": {"POS": "VERB"}},  { "LEFT_ID": "v", "REL_OP": ">", "RIGHT_ID": "advcl", "RIGHT_ATTRS": {"DEP": "advcl"} }, { "LEFT_ID": "advcl", "REL_OP": ">","RIGHT_ID": "object", "RIGHT_ATTRS": {"DEP": "acomp"} }] , 
			# She is happy. | nsubj-acomp be she happy
			"nsubj-acomp": [ { "RIGHT_ID": "v",   "RIGHT_ATTRS": {"LEMMA": "be"}},{ "LEFT_ID": "v", "REL_OP":">", "RIGHT_ID": "subject", "RIGHT_ATTRS": {"DEP": "nsubj"} }, {  "LEFT_ID": "v", "REL_OP": ">",  "RIGHT_ID": "object",    "RIGHT_ATTRS": {"DEP": "acomp"}}], 
			#She is  a girl. | nsubj-attr be she girl
			"nsubj-attr": [  {"RIGHT_ID": "v", "RIGHT_ATTRS": {"LEMMA": "be"}}, { "LEFT_ID": "v", "REL_OP": ">","RIGHT_ID": "subject", "RIGHT_ATTRS": {"DEP": "nsubj"} }, {    "LEFT_ID": "v", "REL_OP": ">", "RIGHT_ID": "object", "RIGHT_ATTRS": {"DEP": "attr"} }],
			#  enjoy swimming | nsubj-xcomp enjoy I swimming
			"nsubj-xcomp": [  {"RIGHT_ID": "v", "RIGHT_ATTRS": {"POS": "VERB"}},{"LEFT_ID": "v", "REL_OP": ">", "RIGHT_ID": "subject", "RIGHT_ATTRS": {"DEP": "nsubj"} }, { "LEFT_ID": "v", "REL_OP": ">", "RIGHT_ID": "object",  "RIGHT_ATTRS": {"DEP": "xcomp"} }],
			# plan to go , | xcomp-to plan go to
			"xcomp-to": [  {"RIGHT_ID": "v", "RIGHT_ATTRS": {"POS": "VERB"}}, { "LEFT_ID": "v", "REL_OP": ">", "RIGHT_ID": "object",  "RIGHT_ATTRS": {"DEP": "xcomp"} }, {"LEFT_ID": "object", "REL_OP": ";", "RIGHT_ID": "to", "RIGHT_ATTRS": {"LEMMA": "to"} },],
			# turn off the light | prt-dobj turn off light
			"dobj-prt": [  {"RIGHT_ID": "v","RIGHT_ATTRS": {"POS": "VERB"}},  { "LEFT_ID": "v", "REL_OP": ">", "RIGHT_ID": "subject", "RIGHT_ATTRS": {"DEP": "prt"} }, { "LEFT_ID": "v", "REL_OP": ">", "RIGHT_ID": "object", "RIGHT_ATTRS": {"DEP": "dobj"} }],
			# Some of the Republican policies have left feminists dismayed and aghast. | dobj-acl leave feminist dismayed
			"dobj-acl":[ {"RIGHT_ID": "v","RIGHT_ATTRS": {"POS": "VERB"}}, { "LEFT_ID": "v","REL_OP": ">","RIGHT_ID": "dobj","RIGHT_ATTRS": {"DEP": "dobj"}},{  "LEFT_ID": "dobj", "REL_OP": ">", "RIGHT_ID": "prep", "RIGHT_ATTRS": {"DEP": "acl"}}],
			# be happy with | nsubj-acomp be I happy
			"acomp-prep":[ {"RIGHT_ID": "v","RIGHT_ATTRS": {"POS": "VERB"}}, { "LEFT_ID": "v","REL_OP": ">","RIGHT_ID": "acomp","RIGHT_ATTRS": {"DEP": "acomp"}},{  "LEFT_ID": "acomp", "REL_OP": ">", "RIGHT_ID": "prep", "RIGHT_ATTRS": {"DEP": "prep"}}],
			# be based on | be-vbn-prep base be on
			"be-vbn-prep":[ {"RIGHT_ID": "v", "RIGHT_ATTRS": {"TAG": "VBN"}}, {"LEFT_ID": "v", "REL_OP": ">","RIGHT_ID": "be","RIGHT_ATTRS": {"LEMMA": "be"} }, { "LEFT_ID": "v", "REL_OP": ">", "RIGHT_ID": "prep", "RIGHT_ATTRS": {"DEP": "prep"}  }],
			}
		for name,pat in pattern.items(): depmatch.matcher.add(name, [pat])
	return depmatch.matcher 
	#doc = spacy.nlp("I turn off the light, and it is based on the table.")
	#for name, ar in matcher(doc) : print(spacy.nlp.vocab[name].text, doc[ar[0]].lemma_, doc[ar[1]].lemma_, doc[ar[2]]) # worry be thrilled

def trpx(doc, vocab): # spacy.nlp.vocab, 2023.1.21
	from spacy.matcher import DependencyMatcher
	if not hasattr(trpx,'matcher'): 
		trpx.matcher = DependencyMatcher(vocab)
		pattern = {
			# advcl-acomp worry be thrilled | "While I was thrilled that it was ok, I worried that she is happy."
			"advcl-acomp": [ {"RIGHT_ID": "v", "RIGHT_ATTRS": {"POS": "VERB"}},  { "LEFT_ID": "v", "REL_OP": ">", "RIGHT_ID": "advcl", "RIGHT_ATTRS": {"DEP": "advcl"} }, { "LEFT_ID": "advcl", "REL_OP": ">","RIGHT_ID": "object", "RIGHT_ATTRS": {"DEP": "acomp"} }] , 
			# She is happy. | nsubj-acomp be she happy
			"nsubj-acomp": [ { "RIGHT_ID": "v",   "RIGHT_ATTRS": {"LEMMA": "be"}},{ "LEFT_ID": "v", "REL_OP":">", "RIGHT_ID": "subject", "RIGHT_ATTRS": {"DEP": "nsubj"} }, {  "LEFT_ID": "v", "REL_OP": ">",  "RIGHT_ID": "object",    "RIGHT_ATTRS": {"DEP": "acomp"}}], 
			#She is  a girl. | nsubj-attr be she girl
			"nsubj-attr": [  {"RIGHT_ID": "v", "RIGHT_ATTRS": {"LEMMA": "be"}}, { "LEFT_ID": "v", "REL_OP": ">","RIGHT_ID": "subject", "RIGHT_ATTRS": {"DEP": "nsubj"} }, {    "LEFT_ID": "v", "REL_OP": ">", "RIGHT_ID": "object", "RIGHT_ATTRS": {"DEP": "attr"} }],
			#  enjoy swimming | nsubj-xcomp enjoy I swimming
			"nsubj-xcomp": [  {"RIGHT_ID": "v", "RIGHT_ATTRS": {"POS": "VERB"}},{"LEFT_ID": "v", "REL_OP": ">", "RIGHT_ID": "subject", "RIGHT_ATTRS": {"DEP": "nsubj"} }, { "LEFT_ID": "v", "REL_OP": ">", "RIGHT_ID": "object",  "RIGHT_ATTRS": {"DEP": "xcomp"} }],
			# plan to go , | xcomp-to plan go to
			"xcomp-to": [  {"RIGHT_ID": "v", "RIGHT_ATTRS": {"POS": "VERB"}}, { "LEFT_ID": "v", "REL_OP": ">", "RIGHT_ID": "object",  "RIGHT_ATTRS": {"DEP": "xcomp"} }, {"LEFT_ID": "object", "REL_OP": ";", "RIGHT_ID": "to", "RIGHT_ATTRS": {"LEMMA": "to"} },],
			# turn off the light | prt-dobj turn off light
			"dobj-prt": [  {"RIGHT_ID": "v","RIGHT_ATTRS": {"POS": "VERB"}},  { "LEFT_ID": "v", "REL_OP": ">", "RIGHT_ID": "subject", "RIGHT_ATTRS": {"DEP": "prt"} }, { "LEFT_ID": "v", "REL_OP": ">", "RIGHT_ID": "object", "RIGHT_ATTRS": {"DEP": "dobj"} }],
			# Some of the Republican policies have left feminists dismayed and aghast. | dobj-acl leave feminist dismayed
			"dobj-acl":[ {"RIGHT_ID": "v","RIGHT_ATTRS": {"POS": "VERB"}}, { "LEFT_ID": "v","REL_OP": ">","RIGHT_ID": "dobj","RIGHT_ATTRS": {"DEP": "dobj"}},{  "LEFT_ID": "dobj", "REL_OP": ">", "RIGHT_ID": "prep", "RIGHT_ATTRS": {"DEP": "acl"}}],
			# be happy with | nsubj-acomp be I happy
			"acomp-prep":[ {"RIGHT_ID": "v","RIGHT_ATTRS": {"POS": "VERB"}}, { "LEFT_ID": "v","REL_OP": ">","RIGHT_ID": "acomp","RIGHT_ATTRS": {"DEP": "acomp"}},{  "LEFT_ID": "acomp", "REL_OP": ">", "RIGHT_ID": "prep", "RIGHT_ATTRS": {"DEP": "prep"}}],
			# be based on | be-vbn-prep base be on
			"be-vbn-prep":[ {"RIGHT_ID": "v", "RIGHT_ATTRS": {"TAG": "VBN"}}, {"LEFT_ID": "v", "REL_OP": ">","RIGHT_ID": "be","RIGHT_ATTRS": {"LEMMA": "be"} }, { "LEFT_ID": "v", "REL_OP": ">", "RIGHT_ID": "prep", "RIGHT_ATTRS": {"DEP": "prep"}  }],
			}
		for name,pat in pattern.items(): trpx.matcher.add(f"trpx:{name}", [pat])
	for name, ar in trpx.matcher(doc) :
		doc.spans[vocab[name].text] = [ doc[ar[0]:ar[0]+1], doc[ar[1]:ar[1]+1], doc[ar[2]:ar[2]+1] ]
	return doc 

def toktrp(doc): # basic for sqlsi 
	arr = [f"*:sntnum"]
	for t in doc:
		[arr.append(s) for s in  ("*:LEX","*:LEM", f"*:{t.pos_}", f"*:{t.tag_}",f"*:{t.dep_}",f"*:~{t.dep_}") ]
		if t.pos_ in ("VERB","NOUN","ADJ","ADV") : 
			arr.append( f"{t.tag_}:{t.text.lower()}")  # VBD :  made , added 2022.12.10

		if not t.pos_ in ('PROPN','X', 'PUNCT',"SPACE") and t.is_alpha:
			arr.extend([f"{t.lemma_}:{t.pos_}",f"{t.lemma_}:LEX:{t.text.lower()}",f"LEM:{t.lemma_.lower()}",f"LEX:{t.text.lower()}",f"{t.pos_}:{t.lemma_.lower()}",f"{t.lemma_.lower()}:{t.pos_}:{t.tag_}",f"*:{t.pos_}:{t.tag_}"]) 
		if t.pos_ not in ("PROPN","PUNCT","SPACE") and t.is_alpha and t.head.is_alpha:
			arr.extend([f"{t.head.lemma_}:{t.head.pos_}:{t.dep_}:{t.pos_}:{t.lemma_}", f"{t.head.lemma_}:{t.head.pos_}:{t.dep_}:{t.pos_}",f"{t.head.lemma_}:{t.head.pos_}:{t.dep_}", f"*:{t.head.pos_}:{t.dep_}", f"*:{t.head.pos_}:{t.dep_}:{t.pos_}:{t.head.lemma_}"])
			if t.dep_ not in ('ROOT'): 
				arr.extend([f"{t.lemma_}:{t.pos_}:~{t.dep_}:{t.head.pos_}:{t.head.lemma_}", f"{t.lemma_}:{t.pos_}:~{t.dep_}:{t.head.pos_}", f"{t.lemma_}:{t.pos_}:~{t.dep_}", f"*:{t.pos_}:~{t.dep_}", f"*:{t.pos_}:~{t.dep_}:{t.head.pos_}:{t.lemma_}"])

	for name, ar in depmatch()(doc): # trpx
		t0,t1,t2 = doc[ar[0]],doc[ar[1]],doc[ar[2]]
		name =  spacy.nlp.vocab[name].text 
		if name in ( "nsubj-acomp", "nsubj-attr"):  
			arr.extend([f"{t1.lemma_}:{t1.pos_}:{name}:{t2.pos_}:{t2.lemma_}",f"{t1.lemma_}:{t1.pos_}:{name}:{t2.pos_}",f"{t1.lemma_}:{t1.pos_}:{name}"])
			arr.extend([f"{t2.lemma_}:{t2.pos_}:~{name}:{t1.pos_}:{t1.lemma_}", f"{t2.lemma_}:{t2.pos_}:~{name}:{t1.pos_}", f"{t2.lemma_}:{t2.pos_}:~{name}"])
		elif name in ("advcl-acomp","acomp-prep") : 	
			arr.extend([f"{t0.lemma_}:{t0.pos_}:{name}:{t2.pos_}:{t2.lemma_}",f"{t0.lemma_}:{t0.pos_}:{name}:{t2.pos_}",f"{t0.lemma_}:{t0.pos_}:{name}"])
			arr.extend([f"{t2.lemma_}:{t2.pos_}:~{name}:{t0.pos_}:{t0.lemma_}",f"{t2.lemma_}:{t2.pos_}:~{name}:{t0.pos_}",f"{t2.lemma_}:{t2.pos_}:~{name}"])
		elif name in ("dobj-prt") and t2.pos_ not in ('PROPN'): 	
			arr.append(f"{t0.lemma_}_{t1.lemma_}:{t0.pos_}:dobj:{t2.pos_}:{t2.lemma_}")
			arr.append(f"{t2.lemma_}:{t2.pos_}:~dobj:{t0.pos_}:{t0.lemma_}_{t1.lemma_}")
		elif name in ("be-vbn-prep") : 	#base:VERB:be-vbn-prep:be based on
			arr.extend([f"{t0.lemma_}:{t0.pos_}:{name}:{t1.lemma_} {t0.text.lower()} {t2.text.lower()}",f"{t0.lemma_}:{t0.pos_}:{name}"])
			
	for sp in doc.noun_chunks: #book:NOUN:np:a book
		arr.extend([f"{sp.root.lemma_.lower()}:{sp.root.pos_}:np:{sp.text.lower()}", f"{sp.root.lemma_.lower()}:{sp.root.pos_}:np", f"*:{sp.root.pos_}:np", f"*:np"])
	for lem, pos, type, chunk in kp_matcher(doc): #brink:NOUN:pp:on the brink  	# [('pp', 'on the brink', 2, 5), ('ap', 'very happy', 9, 11)]
		arr.extend([f"{lem}:{pos}:{type}:{chunk}", f"{lem}:{pos}:{type}", f"*:{pos}:{type}", f"*:{type}"])
	for trpx, row in dep_matcher(doc): #[('svx', [1, 0, 2])] ## consider:VERB:vnpn:**** 
		verbi = row[0] #consider:VERB:be_vbn_p:be considered as
		arr.extend([f"{doc[verbi].lemma_}:{doc[verbi].pos_}:{trpx}", f"*:{doc[verbi].pos_}:{trpx}", f"*:{trpx}"]) #consider:VERB:svx
		if trpx == 'sva' and doc[row[0]].lemma_ == 'be': # fate is sealed, added 2022.7.25
			arr.extend([f"{doc[row[1]].lemma_}:{doc[row[1]].pos_}:sbea:{doc[row[2]].pos_}:{doc[row[2]].lemma_}", f"{doc[row[1]].lemma_}:{doc[row[1]].pos_}:sbea", f"*:{doc[row[1]].pos_}:sbea"])
			arr.extend([f"{doc[row[2]].lemma_}:{doc[row[2]].pos_}:~sbea:{doc[row[1]].pos_}:{doc[row[1]].lemma_}", f"{doc[row[2]].lemma_}:{doc[row[2]].pos_}:~sbea", f"*:{doc[row[2]].pos_}:~sbea"])
	for row in verbnet_matcher(doc): #[(1, 0, 3, 'NP V S_ING')] # last to be called, since NP is merged
		if len(row) == 4: 
			verbi, ibeg, iend, chunk = row
			if doc[verbi].lemma_.isalpha() : 
				arr.append(f"{doc[verbi].lemma_}:{doc[verbi].pos_}:verbnet:{chunk}") #consider:VERB:verbnet:NP V S_ING
	for name,ibeg,iend in post_np_matcher(doc): #added 2022.7.25
		if name in ('v_n_vbn','v_n_adj'): 
			arr.extend([f"{doc[ibeg].lemma_}:{doc[ibeg].pos_}:{name}:{doc[ibeg].lemma_} {doc[ibeg+1].lemma_} {doc[ibeg+2].text}", f"{doc[ibeg].lemma_}:{doc[ibeg].pos_}:{name}", f"*:{doc[ibeg].pos_}:{name}"])
	return arr 

def sqlconn(outfile, sqls:str=["create table if not exists si( s varchar(64) not null primary key, i int not null default 0) without rowid","create table if not exists st( s varchar(64) not null primary key, t text, cnt int not null default 0) without rowid"]):
	conn  =	sqlite3.connect(outfile, check_same_thread=False) 
	for sql in sqls: conn.execute(sql)
	conn.execute('PRAGMA synchronous=OFF')
	conn.execute('PRAGMA case_sensitive_like = 1') #conn.execute("PRAGMA cache_size = -512")  		conn.execute('PRAGMA cache_size = 2000000')  # 2 Gb
	conn.commit()
	return conn 

def sqlsi(infile, func:str='toktrp', outfile:str=None,batch=1000,): #ibeg:int=0, iend:int=1000000,
	''' data for mynac, func must exist , func=trpx '''
	if outfile is None or not outfile: outfile = infile.split('.')[0] + f".sqlsi"
	print(f"started: [batch={batch}]", infile, outfile , func , flush=True)
	func = globals()[func] 
	start = time.time()
	conn = sqlconn(outfile) 
	for sid, line in enumerate(fileinput.input(infile,openhook=fileinput.hook_compressed)): 
		try: #if sid < ibeg : continue |	if sid >= iend: break 
			arr = json.loads(line.strip()) 
			doc = spacy.from_json(arr)  
			for t in doc:  
				if not t.pos_ in ('PROPN','X', 'PUNCT',"SPACE",'ROOT','NUM') and not t.head.pos_ in ('PROPN','X', 'PUNCT',"SPACE",'ROOT','NUM') and t.is_alpha and t.head.is_alpha:
					trp = f"{t.head.lemma_}:{t.head.pos_}:{t.dep_}:{t.pos_}:{t.lemma_}"
					conn.execute(f"INSERT OR IGNORE INTO st(s,t) VALUES(?,?)", (trp,doc.text))
			for s in func(doc):  
				conn.execute(f"INSERT INTO si(s,i) VALUES(?,?) ON CONFLICT(s) DO UPDATE SET i = i + 1", (s,1))
			if (sid) % batch == 0 : 
				print (f"sid = {sid}, \t| using(s): ", round(time.time() - start,1), flush=True)
				conn.commit() #conn.close()  #del conn			#conn = sqlconn(outfile) 		#spacy.nlp	= spacy.load('en_core_web_lg')
				refresh() 
		except Exception as e:
			print ("ex:", e, sid, line) 
			exc_type, exc_value, exc_obj = sys.exc_info() 	
			traceback.print_tb(exc_obj)
	conn.commit()
	conn.execute(f"update st set cnt = (select i from si where si.s = st.s)")
	conn.commit()
	print("sqlsi finished:", infile)

def test(): 
	doc = spacy.nlp("It is based on the book.") # "While I was thrilled that it was ok, I worried that she is happy."
	for name, ar in depmatch()(doc) : 
		print(spacy.nlp.vocab[name].text, doc[ar[0]].lemma_, doc[ar[1]].lemma_, doc[ar[2]])
	print ( es_skenp(doc)) 

def es_submit(infile, index:str=None, batch=200000, recreate:bool=True, host='172.17.0.1',port=9200): 
	''' python3 -m api.sntjson-es gzjc.jsonlg.3.4.1.gz'''
	from elasticsearch import Elasticsearch,helpers
	import so
	es	 = Elasticsearch([ f"http://{host}:{port}" ])  
	if index is None : index = infile.split('.')[0]
	print(f">>load started: host={host}, index={index} " , infile, index, flush=True )
	if recreate or not es.indices.exists(index=index): 
		if es.indices.exists(index=index):es.indices.delete(index=index)
		es.indices.create(index=index, body=so.config) 

	actions=[]
	def add(source):  
		actions.append( {'_op_type':'index', '_index':index, '_id': source['id'], '_source': source } )
	for sid, line in enumerate(fileinput.input(infile,openhook=fileinput.hook_compressed)): 
		try:
			doc = Doc(spacy.nlp.vocab).from_json(json.loads(line.strip())) # add skenp 
			for t in doc: 	add({"type":"tok", "id": f"{sid}-tok-{t.i}", "sid":sid, 'lex':t.text, 'lem':t.lemma_, 'pos':t.pos_, 'tag':t.tag_, 'dep':t.dep_, "gpos":t.head.pos_, "glem":t.head.lemma_ , "gtag":t.head.tag_ }) #'i':t.i, "head":t.head.i,
			for sp in doc.noun_chunks: 	add({"type":"np", "id": f"{sid}-NP-{sp.start}", "sid":sid, 'chunk':sp.text, 'lem':doc[sp.end-1].lemma_ })
			for lem, pos, type, chunk in kp_matcher(doc): #brink:NOUN:pp:on the brink # [('pp', 'on the brink', 2, 5), ('ap', 'very happy', 9, 11)]
				add({"type":type, "id": f"{sid}-{type}-{chunk}", "sid":sid,  'chunk':chunk, 'lem':lem , "pos":pos}) #"src": doc.text,
			for name, ar in depmatch()(doc) : 
				type = spacy.nlp.vocab[name].text # worry be thrilled
				lem = doc[ar[0]].lemma_
				add({"type":type, "id": f"{sid}-{type}-{lem}", "sid":sid,  'lem':lem,  'tag':doc[ar[0]].tag_, 'lem1':doc[ar[1]].lemma_, 'lem2':doc[ar[2]].lemma_ , 'tag1':doc[ar[1]].tag_ , 'tag2':doc[ar[2]].tag_ }) 
			# merged NP must be finally called 
			add( {'type':'snt',  "id":sid,  'snt':doc.text, 'postag': es_postag(doc), 'tc': len(doc), 'skenp': es_skenp(doc) }  ) #, 
			if len(actions) >= batch: 
				helpers.bulk(client=es,actions=actions, raise_on_error=False)
				print ( sid, actions[-1], flush=True)
				actions = []
				refresh() # 2022.1.20 
		except Exception as e:
			print("ex:", e, sid)	
			exc_type, exc_value, exc_obj = sys.exc_info() 	
			traceback.print_tb(exc_obj)
	if actions : helpers.bulk(client=es,actions=actions, raise_on_error=False)
	print(">>load finished:" , infile, index )

[setattr(builtins, k, v) for k, v in globals().items() if not k.startswith("_") and not '.' in k and not hasattr(builtins,k) ] #setattr(builtins, "spacy", spacy)
if __name__	== '__main__': 
	#es_submit("gzjc.jsonlg.3.4.1.gz", host='hw13.jukuu.com')
	import fire
	fire.Fire({"sqlsi":sqlsi, "test":test, "es_submit":es_submit })

def kps(doc): 
	''' doc is of single sent, 2022.9.8 '''
	_kps = []
	[ _kps.append(f"{t.pos_}:{t.lemma_}") for t in doc]  # VERB:book
	[ _kps.append(f"_{t.lemma_}:{t.text.lower()}") for t in doc]  # _book:booked,  added 2022.8.21
	[ _kps.append(f"{t.tag_}:{t.pos_}_{t.lemma_}") for t in doc]  # VBD:VERB_book,  added 2022.8.25
	[ _kps.append(f"{t.dep_}:{t.head.pos_}_{t.head.lemma_}:{t.pos_}_{t.lemma_}") for t in doc if t.pos_ not in ('PUNCT')]  # 
	[ _kps.append(f"~{t.dep_}:{t.pos_}_{t.lemma_}:{t.head.pos_}_{t.head.lemma_}") for t in doc if t.pos_ not in ('PUNCT')]  # 
	[ _kps.append(f"NP:{doc[sp.end-1].pos_}_{doc[sp.end-1].lemma_}:{sp.text.lower()}") for sp in doc.noun_chunks ]
	_kps.append( f"stype:" +  "simple_snt" if simple_sent(doc) else "complex_snt" )
	if compound_snt(doc) : _kps.append("stype:compound_snt")

	# [('pp', 'on the brink', 2, 5), ('ap', 'very happy', 9, 11)]
	for lem, pos, type, chunk in kp_matcher(doc): #brink:NOUN:pp:on the brink
		_kps.append(f"{type}:{pos}_{lem}:{chunk}")
	for trpx, row in dep_matcher(doc): #[('svx', [1, 0, 2])] ## consider:VERB:vnpn:**** 
		verbi = row[0] #consider:VERB:be_vbn_p:be considered as
		_kps.append(f"{trpx}:{doc[verbi].pos_}_{doc[verbi].lemma_}")
		if trpx == 'sva' and doc[row[0]].lemma_ == 'be': # fate is sealed, added 2022.7.25   keep sth. stuck
			_kps.append(f"sbea:{doc[row[1]].pos_}_{doc[row[1]].lemma_}:{doc[row[2]].pos_}_{doc[row[2]].lemma_}")
		
	# last to be called, since NP is merged
	for row in verbnet_matcher(doc): #[(1, 0, 3, 'NP V S_ING')]
		if len(row) == 4: 
			verbi, ibeg, iend, chunk = row
			if doc[verbi].lemma_.isalpha() : 
				_kps.append(f"verbnet:{doc[verbi].pos_}_{doc[verbi].lemma_}:{chunk}")

	for name,ibeg,iend in post_np_matcher(doc): #added 2022.7.25
		if name in ('v_n_vbn','v_n_adj'): 
			_kps.append(f"{name}:{doc[ibeg].pos_}_{doc[ibeg].lemma_}:{doc[ibeg].lemma_} {doc[ibeg+1].lemma_} {doc[ibeg+2].text}")
	return _kps

#print(sntbr("[\u8bd1\u6587]The 55-kilometre Hong Kong Zhuhai-Macau Bridge is an extraordinary engineering. It is the world's longest sea-crossing transportation system combining bridges and tunnels, which joins the three cities of Hong Kong Zhuhai and Macao, cutting the travelling time among them from 3 hours to 30 minutes. The reinforced concrete bridge with huge spans fully not only proves that China has the ability to complete the record-breaking mega-construction, but also will enhance the regional integration and boost the economic growth. It plays a crucial role in the overall plan to develop China’s Great Bay Area, which China intends to turn into one rivaling those of San Francisco, New York and Tokyo in terms of technological innovation and economic prosperity.", with_pid=True))
#c:\users\zhang\appdata\local\programs\python\python38\lib\site-packages  
#/home/ubuntu/.local/lib/python3.8/site-packages/en

'''
>>> model('lg').vocab
<spacy.vocab.Vocab object at 0x0000013459154A60>
>>> len(model('lg').vocab)
768
>>> len(model('sm').vocab)
767
'''