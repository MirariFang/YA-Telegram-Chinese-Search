# Start the server a little differently, still from the `stanford-corenlp-full-2018-02-27 directory:
echo "Start the StanfordCoreNLPServer..."
cd stanford-corenlp-full-2018-02-27
java -Xmx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer \
-serverProperties StanfordCoreNLP-chinese.properties \
-preload tokenize,ssplit,pos,lemma,ner,parse \
-status_port 9001  -port 9001 -timeout 15000
