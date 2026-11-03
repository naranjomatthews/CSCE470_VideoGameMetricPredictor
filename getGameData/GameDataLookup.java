import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

public class GameDataLookup {
    private static final String[] GAME_FIELDS = {
        "title",
        "description",
        "tags",
        "genres",
        "rating",
        "positive",
        "negative",
        "recommendations",
        "downloads"
    };

    public static List<Map<String, Object>> getGameData(
            List<String> docIDs,
            Map<String, Map<String, Object>> gameData) {

        List<Map<String, Object>> results = new ArrayList<>();

        for (String docID : docIDs) {
            Map<String, Object> game = gameData.get(docID);
            if (game == null) {
                continue;
            }
            
            Map<String, Object> selectedGame = new LinkedHashMap<>();

            selectedGame.put("docID", docID);

            for (String field : GAME_FIELDS) {
                selectedGame.put(field, game.get(field));
            }

            results.add(selectedGame);
        }

        return results;
    }
}