import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class bm25Ranker{
    
    //general weights for different fields
    //primary fields
    double nameWeight = 0.9;
    double genreWeight = 0.9;
    double ctgryWeight = 0.9;
    double tagWeight = 0.9;
    double devWeight = 0.9;
    double pubWeight = 0.9;

    //secondary fields
    double lngDesWeight = 0.1;
    double shrtDesWeight = 0.1;
    double aboutWeight = 0.1;
    double reviewWeight = 0.1;

    //BM25-specific weights for different fields
    double k1 = 0.5;
    
    //primary fields
    double bName = 0.5;
    double bGenre = 0.5;
    double bCtgry = 0.5;
    double bTag = 0.5;
    double bDev = 0.5;
    double bPub = 0.5;

    //secondary fields
    double bLngDes = 0.5;
    double bShrtDes = 0.5;
    double bAbout = 0.5;
    double bReview = 0.5;

    //non-textual features

    double positiveLambda = 0.5;
    double positiveLambdaPrime = 0.5;
    double negativeLambda = 0.5;
    double negativeLambdaPrime = 0.5;
    double recLambda = 0.5;
    double recLambdaPrime = 0.5;
    double userScoreLambda = 0.5;
    double userScoreLambdaPrime = 0.5;

    // game ID -> field -> length
    Map<String,Map<String,Double>> lengths;
    
    Map<String,Double> avgLengths;

    private void calcAverageLengths(){

    }

    private void normalizeTFs(){
        
    }
    
    private void createRanking(){
        
    }

    public static void main(String[] args){
        System.out.println("Test");
    }
}

