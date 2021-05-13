#!/bin/bash
# A sample Bash script, by Peiwen
echo Start to build requirement file
pip install -r requirements.txt

# Then download the necessary CoreNLP packages:
echo "Start to download the StanfordCoreNLP packages, it takes a while"
wget --no-check-certificate http://nlp.stanford.edu/software/stanford-corenlp-full-2018-02-27.zip
unzip stanford-corenlp-full-2018-02-27.zip
rm stanford-corenlp-full-2018-02-27.zip
cd tokenizer-server

# Get the Chinese model
echo "Start to download the Chinese language model, it takes a while"
wget --no-check-certificate http://nlp.stanford.edu/software/stanford-chinese-corenlp-2018-02-27-models.jar
wget --no-check-certificate https://raw.githubusercontent.com/stanfordnlp/CoreNLP/master/src/edu/stanford/nlp/pipeline/StanfordCoreNLP-chinese.properties

echo "Requirement setup successfully completed. Run ./start_server.sh in this directory."
