**README FOR NLP PRE-PROCESSING MODULE**


---

1. This module consists of the basic tools to pre-process a query. The module runs the following tools in respective order: 

Enchant Spell Checker -> Stanford CoreNLP TrueCase* (truecase) -> Stanford CoreNLP Tokenizer (tokenize) -> Stanford CoreNLP Sentence Split (ssplit) -> Stanford CoreNLP POS Tagger (pos), Stanford CoreNLP Lemma (lemma) -> Stanford CoreNLP CRF NER (ner) -> Stanford CoreNLP REGEX NER (regexner) -> Stanford CoreNLP Parse (parse).

**INPUT:** "I want to buk a flight tikket from new york to bangalore between 21st june and 23rd june."

**SPELL and TRUECASE OUTPUT:** I want to book a flight ticket from New YORK TO BANGALORE between 21st June and 23rd June. 

**NER OUTPUT:** I want to book a flight ticket from New (LOCATION: YORK) TO (LOCATION: BANGALORE) between (DATE: 21st June) and (DATE: 23rd June. )

 Truecase requires tokenize -> ssplit -> pos -> lemma tools as to predict the truecase of a word.

2. The module uses following packages. The instructions for installing these packages are described here:
   >> cd path/to/genie directory
   >> mkdir /Tools
   
   The packages will be installed inside the 'Tools' directory. 
   a. - Download Enchant1.6.0 (enchant-1.6.0.tar.gz) from http://www.abisource.com/downloads/enchant/1.6.0/enchant-1.6.0.tar.gz
      - Install PyEnchant using 'sudo pip install pyenchant'

   b. Download Stanford CoreNLP 3.5.2 (stanford-corenlp-full-2015-04-20.zip) from http://nlp.stanford.edu/software/corenlp.shtml
      >> Upgrade Java to 1.8+
      This package is already build. 

      Use this command to run the Stanford CoreNLP
      java -cp '*' -Xmx2g edu.stanford.nlp.pipeline.StanfordCoreNLP -annotators tokenize,ssplit,pos,lemma,truecase -file <filename>

      where annotators are the "tools" to be run. 

      Use this page for further instructions: http://nlp.stanford.edu/software/corenlp.shtml

3.  The script textToDemand.py runs the preprocessing module.
