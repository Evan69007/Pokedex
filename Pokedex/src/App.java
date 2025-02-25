import org.json.simple.JSONObject;

public class App {
    public static void main(String[] args) throws Exception {
		JSONObject obj = new JSONObject();
		obj.put("name", "Toto");
		obj.put("birth", "Oct-13th");
        System.out.println(obj);
    }
}