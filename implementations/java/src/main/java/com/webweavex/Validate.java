package com.webweavex;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;

import java.io.*;
import java.nio.file.*;
import java.util.*;

public class Validate {
    
    private static final Gson gson = new GsonBuilder()
        .setPrettyPrinting()
        .create();
    private static final JsonParser jsonParser = new JsonParser();
    
    public static void main(String[] args) throws Exception {
        String testCasesPath = "../../core/test_cases/test_cases.json";
        String outputDir = "../../test_output/java/";
        
        Path testCasesFile = Paths.get(testCasesPath).toAbsolutePath();
        Path outputPath = Paths.get(outputDir).toAbsolutePath();
        
        Files.createDirectories(outputPath);
        
        String jsonContent = new String(Files.readAllBytes(testCasesFile));
        JsonArray testCasesArray = jsonParser.parse(jsonContent).getAsJsonArray();
        
        List<String> testCaseNames = new ArrayList<>();
        
        WebWeaveX wx = new WebWeaveX();
        
        System.out.println("Exporting Java outputs...");
        System.out.println("==================================================");
        
        for (int i = 0; i < testCasesArray.size(); i++) {
            JsonObject tc = testCasesArray.get(i).getAsJsonObject();
            String name = tc.get("name").getAsString();
            String inputText = tc.get("input").getAsString();
            
            testCaseNames.add(name);
            
            System.out.println("Processing: " + name);
            
            Map<String, Object> result = wx.extract(inputText);
            String outputJson = gson.toJson(result);
            
            Path outputFile = outputPath.resolve(name + ".json");
            Files.write(outputFile, outputJson.getBytes());
            
            System.out.println("  Saved: " + outputFile);
        }
        
        System.out.println("==================================================");
        System.out.println("Exported " + testCasesArray.size() + " test cases to " + outputPath);
        
        JsonObject manifest = new JsonObject();
        manifest.addProperty("language", "java");
        JsonArray namesArray = new JsonArray();
        for (String n : testCaseNames) {
            namesArray.add(n);
        }
        manifest.add("test_cases", namesArray);
        Files.write(outputPath.resolve("manifest.json"), 
            gson.toJson(manifest).getBytes());
        System.out.println("Manifest: " + outputPath.resolve("manifest.json"));
    }
}
