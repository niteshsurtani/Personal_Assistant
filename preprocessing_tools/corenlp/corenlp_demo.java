import java.io.*;
import java.util.*;

import java.util.List;
import java.util.Properties;
import java.util.Date;
import java.text.SimpleDateFormat;
import java.text.DateFormat;

import edu.stanford.nlp.time.*;
import edu.stanford.nlp.dcoref.CorefChain;
import edu.stanford.nlp.dcoref.CorefCoreAnnotations;
import edu.stanford.nlp.io.*;
import edu.stanford.nlp.ling.*;
import edu.stanford.nlp.pipeline.*;
import edu.stanford.nlp.semgraph.SemanticGraph;
import edu.stanford.nlp.semgraph.SemanticGraphCoreAnnotations;
import edu.stanford.nlp.trees.*;
import edu.stanford.nlp.util.*;

/** This class demonstrates building and using a Stanford CoreNLP pipeline. */
public class corenlp_demo {

  /** Usage: java -cp "*" StanfordCoreNlpDemo [inputFile [outputTextFile [outputXmlFile]]] */

  public static void main(String[] args) throws IOException {
    // set up optional output files
    PrintWriter out;
    if (args.length > 1) {
      out = new PrintWriter(args[1]);
    } else {
      out = new PrintWriter(System.out);
    }
    PrintWriter xmlOut = null;
    if (args.length > 2) {
      xmlOut = new PrintWriter(args[2]);
    }

    // Create a CoreNLP pipeline. Thn build a particular pipeline
    System.out.println(" ============== Start ================");
    Properties props = new Properties();
    props.put("annotators", "tokenize, ssplit, pos, lemma, parse");
    StanfordCoreNLP pipeline = new StanfordCoreNLP(props);
    System.out.println(" ============== End ================");
  
    Annotation annotation;
    annotation = new Annotation(IOUtils.slurpFileNoExceptions(args[0]));

    pipeline.annotate(annotation);
    // pipeline.prettyPrint(annotation, out);
    // if (xmlOut != null) {
    //   pipeline.xmlPrint(annotation, xmlOut);
    // }

    List<CoreMap> sentences = annotation.get(CoreAnnotations.SentencesAnnotation.class);
    if (sentences != null) {
      for (int i = 0, sz = sentences.size(); i < sz; i ++) {
        CoreMap sentence = sentences.get(i);

        String str = sentence.toString();
        // Run SUTime for each sentence
        // TimeTokens(str);
        Properties p = new Properties();
        AnnotationPipeline pipeline2 = new AnnotationPipeline();
        pipeline2.addAnnotator(new TokenizerAnnotator(true));
        pipeline2.addAnnotator(new WordsToSentencesAnnotator(true));
        pipeline2.addAnnotator(new POSTaggerAnnotator(true));
        pipeline2.addAnnotator(new TimeAnnotator("sutime", p));

        Annotation ann = new Annotation(str);
        Date dt = new Date();
        SimpleDateFormat ft = new SimpleDateFormat ("yyyy-MM-dd");
        
        ann.set(CoreAnnotations.DocDateAnnotation.class, ft.format(dt));
        // System.out.println(ann);
        pipeline2.annotate(ann);

        List<CoreMap> timexAnnsAll = ann.get(TimeAnnotations.TimexAnnotations.class);
        Integer[] start = new Integer[timexAnnsAll.size()];
        Integer[] end = new Integer[timexAnnsAll.size()];
        String[] value = new String[timexAnnsAll.size()];

        Integer count = 0;
        for (CoreMap cm : timexAnnsAll) {
          List<CoreLabel> tokens2 = cm.get(CoreAnnotations.TokensAnnotation.class);
          start[count] = Integer.parseInt(tokens2.get(0).toString().split("-")[1]);
          end[count] = Integer.parseInt(tokens2.get(tokens2.size()-1).toString().split("-")[1]);
          value[count] = cm.get(TimeExpression.Annotation.class).getTemporal().toString();
          count += 1;
        }
        Integer totalTimeExpr = count;
        List<CoreLabel> tokens = sentence.get(CoreAnnotations.TokensAnnotation.class);

        String[] tokenAnnotations = {
                "index", "word", "tag", "lemma" };

        count = 1;
        Integer index = 0;
        for (CoreLabel token: tokens) {
          // String s = token.toShorterString(tokenAnnotations);
          // if (count>=start[index] && count<=end[index]){
          // }
          System.out.print(token.index()+" "+token.word()+ " "+token.tag()+ " "+token.lemma()+" ");
          if(index<totalTimeExpr && count>=start[index] && count<=end[index]){
            // Time value
            String val = value[index];
            String type;
            if(val.contains("P")){
              type = "DURATION";
            }
            else if(val.contains("T")){
              type = "TIME";
            }
            else{
              type = "DATE";
            }

            System.out.print(type+ " " +val);
            if(count==end[index]){
              index += 1;
            }
          }
          else{          
            System.out.print("0 0");
          }
          System.out.println();
          count += 1;
        }
        Tree tree = sentence.get(TreeCoreAnnotations.TreeAnnotation.class);
        System.out.println("<parse>"+tree);
      }
    }
    IOUtils.closeIgnoringExceptions(out);
    // IOUtils.closeIgnoringExceptions(xmlOut);
  }
}
